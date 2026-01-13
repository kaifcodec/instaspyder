# instaspyder/core/face_engine.py
import face_recognition
import httpx
import json
import os
import gc
from instaspyder.utils.colors import G, R, Y, C, X
from instaspyder.core.config_manager import CACHE_DIR, USER_HOME

async def run_face_recognition(seed_username, target_image_path):
    cache_file = os.path.join(CACHE_DIR, f"metadata_{seed_username}.json")
    progress_file = os.path.join(CACHE_DIR, f"progress_{seed_username}.json")
    match_log_file = os.path.join(CACHE_DIR, f"matches_{seed_username}.json")
    
    temp_dir = USER_HOME / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = str(temp_dir / "current_face.jpg")

    if not os.path.exists(cache_file):
        print(f"{R}[-] No cache found for @{seed_username}.{X}")
        return


    try:
        target_img = face_recognition.load_image_file(target_image_path)
        target_encoding = face_recognition.face_encodings(target_img)[0]
    except Exception as e:
        print(f"{R}[-] Target Error: {e}{X}")
        return

    with open(cache_file, "r") as f:
        candidates = json.load(f)

    processed_ids = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            processed_ids = set(json.load(f))

    all_potential_matches = []
    if os.path.exists(match_log_file):
        with open(match_log_file, "r") as f:
            all_potential_matches = json.load(f)

        print(f"{G}[+] Resuming scan. Found {len(all_potential_matches)} previous matches:{X}")
        for m in all_potential_matches:
            print(f"    {C}[PREVIOUS MATCH] @{m['username']} ({m['confidence']:.2f}% similarity){X}")

    print(f"\n{Y}[i] Total: {len(candidates)} | Remaining: {len(candidates) - len(processed_ids)}{X}\n")

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        for i, user in enumerate(candidates, 1):
            user_id = str(user.get("pk") or user.get("id"))
            if user_id in processed_ids:
                continue

            url = user.get("hd_pic_url") or user.get("profile_pic_url")
            if not url: continue

            print(f"\r{X}[{i}/{len(candidates)}] Testing @{user['username']}... ", end="", flush=True)

            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    with open(temp_path, "wb") as tmp:
                        tmp.write(resp.content)

                    unknown_img = face_recognition.load_image_file(temp_path)
                    unknown_encs = face_recognition.face_encodings(unknown_img)

                    if unknown_encs:
                        dist = face_recognition.face_distance([target_encoding], unknown_encs[0])[0]
                        if dist <= 0.55:
                            conf = max(0, (1 - dist / 0.6) * 100)
                            new_match = {
                                "username": user['username'],
                                "full_name": user.get('full_name'),
                                "distance": dist,
                                "confidence": conf
                            }
                            all_potential_matches.append(new_match)

                            with open(match_log_file, "w") as f:
                                json.dump(all_potential_matches, f, indent=4)

                            print(f"\n{G}[LIVE MATCH] @{user['username']} ({conf:.2f}% similarity){X}")


                    processed_ids.add(user_id)
                    with open(progress_file, "w") as f:
                        json.dump(list(processed_ids), f)

                del unknown_img
                gc.collect()
            except KeyboardInterrupt:
                print(f"\n{Y}[!] Pausing scan. State saved.{X}")
                return
            except:
                continue


    if os.path.exists(temp_path): os.remove(temp_path)

    print("\n" + "="*60)
    print(f"{Y}   FINAL REPORT (Sorted by Probability)   {X}")
    print("="*60)

    sorted_matches = sorted(all_potential_matches, key=lambda x: x['confidence'], reverse=True)
    for match in sorted_matches:
        color = G if match['confidence'] > 50 else Y
        print(f"{color}[{match['confidence']:.2f}%]{X} @{match['username']} - {match['full_name']}")


    if os.path.exists(progress_file): os.remove(progress_file)
    if os.path.exists(match_log_file): os.remove(match_log_file)

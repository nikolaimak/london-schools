#!/usr/bin/env python3
import json, urllib.request, time, os

with open("/tmp/london_postcodes.json") as f:
    all_postcodes = json.load(f)

print(f"Total postcodes: {len(all_postcodes):,}", flush=True)
pc_to_msoa = {}

progress_file = "/tmp/pc_to_msoa_progress.json"
if os.path.exists(progress_file):
    with open(progress_file) as f:
        pc_to_msoa = json.load(f)
    print(f"Resuming from {len(pc_to_msoa):,}", flush=True)

remaining = [pc for pc in all_postcodes if pc not in pc_to_msoa]
print(f"Remaining: {len(remaining):,}", flush=True)

BATCH_SIZE = 100
total_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE
errors = 0
not_found = 0

for batch_idx in range(0, len(remaining), BATCH_SIZE):
    batch = remaining[batch_idx:batch_idx + BATCH_SIZE]
    batch_num = batch_idx // BATCH_SIZE + 1
    if batch_num % 100 == 0:
        print(f"Batch {batch_num}/{total_batches}, mapped: {len(pc_to_msoa):,}", flush=True)
    payload = json.dumps({"postcodes": batch}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.postcodes.io/postcodes",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    data = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            break
        except Exception as e:
            if attempt == 2:
                errors += 1
                print(f"ERROR batch {batch_num}: {e}", flush=True)
            else:
                time.sleep(1)
    if data and data.get("result"):
        for item in data["result"]:
            pc = item["query"]
            result = item.get("result")
            if result:
                codes = result.get("codes", {})
                msoa_code = codes.get("msoa") or codes.get("msoa21")
                msoa_name = result.get("msoa21") or result.get("msoa11") or result.get("msoa")
                if msoa_code:
                    pc_to_msoa[pc] = {"msoa_code": msoa_code, "msoa_name": msoa_name}
                else:
                    not_found += 1
            else:
                not_found += 1
    if batch_num % 200 == 0:
        with open(progress_file, "w") as f:
            json.dump(pc_to_msoa, f)
        print(f"  Saved progress: {len(pc_to_msoa):,}", flush=True)
    time.sleep(0.03)

with open(progress_file, "w") as f:
    json.dump(pc_to_msoa, f)
with open("/tmp/pc_to_msoa.json", "w") as f:
    json.dump(pc_to_msoa, f)
print(f"Done! Mapped: {len(pc_to_msoa):,}, not found: {not_found}, errors: {errors}", flush=True)
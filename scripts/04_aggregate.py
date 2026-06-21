#!/usr/bin/env python3
import json
from collections import defaultdict

with open("/tmp/pc_prices.json") as f:
    pc_prices = json.load(f)
with open("/tmp/pc_to_msoa.json") as f:
    pc_to_msoa = json.load(f)

print(f"Loaded {len(pc_prices):,} postcodes with prices", flush=True)
print(f"Loaded {len(pc_to_msoa):,} postcode->MSOA mappings", flush=True)

msoa_prices = defaultdict(list)
msoa_names = {}
unmapped = 0

for pc, prices in pc_prices.items():
    if pc in pc_to_msoa:
        info = pc_to_msoa[pc]
        code = info["msoa_code"]
        name = info["msoa_name"]
        msoa_prices[code].extend(prices)
        if name and code not in msoa_names:
            msoa_names[code] = name
    else:
        unmapped += 1

print(f"Unique MSOAs: {len(msoa_prices):,}", flush=True)
print(f"Unmapped postcodes: {unmapped}", flush=True)

msoa_list = []
for code, prices in sorted(msoa_prices.items()):
    sp = sorted(prices)
    n = len(sp)
    median = sp[n//2] if n%2==1 else (sp[n//2-1]+sp[n//2])//2
    entry = {}
    entry["code"] = code
    entry["name"] = msoa_names.get(code, "")
    entry["median_price"] = median
    entry["sales_count"] = n
    msoa_list.append(entry)

output = {}
output["msoas"] = msoa_list
output["source"] = "Land Registry Price Paid 2025-2026"
output["period"] = "Jan 2025 - Jun 2026"
output["total_transactions"] = sum(len(v) for v in msoa_prices.values())
output["msoa_count"] = len(msoa_list)

with open("/tmp/london-msoa-prices.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(msoa_list)} MSOAs to /tmp/london-msoa-prices.json", flush=True)
pv = [m["median_price"] for m in msoa_list]
print(f"Price range: {min(pv):,} - {max(pv):,}", flush=True)
print(f"Median of medians: {sorted(pv)[len(pv)//2]:,}", flush=True)
for m in msoa_list[:3]:
    print(f"  {m[chr(99)+chr(111)+chr(100)+chr(101)]}: {m[chr(110)+chr(97)+chr(109)+chr(101)]} - {m[chr(109)+chr(101)+chr(100)+chr(105)+chr(97)+chr(110)+chr(95)+chr(112)+chr(114)+chr(105)+chr(99)+chr(101)]:,} ({m[chr(115)+chr(97)+chr(108)+chr(101)+chr(115)+chr(95)+chr(99)+chr(111)+chr(117)+chr(110)+chr(116)]} sales)", flush=True)

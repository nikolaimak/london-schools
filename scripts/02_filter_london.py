#!/usr/bin/env python3
import csv
import json
from collections import defaultdict

LONDON_OUTCODES = set([
    'E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','E13','E14','E15','E16','E17','E18',
    'EC1A','EC1M','EC1N','EC1R','EC1V','EC1Y',
    'EC2A','EC2M','EC2N','EC2R','EC2V','EC2Y',
    'EC3A','EC3M','EC3N','EC3P','EC3R','EC3V',
    'EC4A','EC4M','EC4N','EC4P','EC4R','EC4V','EC4Y',
    'N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','N12','N13','N14','N15','N16','N17','N18','N19','N20','N21','N22',
    'NW1','NW2','NW3','NW4','NW5','NW6','NW7','NW8','NW9','NW10','NW11',
    'SE1','SE2','SE3','SE4','SE5','SE6','SE7','SE8','SE9','SE10','SE11','SE12','SE13','SE14','SE15','SE16','SE17','SE18','SE19','SE20','SE21','SE22','SE23','SE24','SE25','SE26','SE27','SE28',
    'SW1A','SW1E','SW1H','SW1P','SW1V','SW1W','SW1X','SW1Y',
    'SW2','SW3','SW4','SW5','SW6','SW7','SW8','SW9','SW10','SW11','SW12','SW13','SW14','SW15','SW16','SW17','SW18','SW19','SW20',
    'W1A','W1B','W1C','W1D','W1F','W1G','W1H','W1J','W1K','W1S','W1T','W1U','W1W',
    'W2','W3','W4','W5','W6','W7','W8','W9','W10','W11','W12','W13','W14',
    'WC1A','WC1B','WC1E','WC1H','WC1N','WC1R','WC1V','WC1X',
    'WC2A','WC2B','WC2E','WC2H','WC2N','WC2R',
    'BR1','BR2','BR3','BR4','BR5','BR6','BR7','BR8',
    'CR0','CR2','CR3','CR4','CR5','CR6','CR7','CR8','CR9',
    'DA1','DA2','DA3','DA4','DA5','DA6','DA7','DA8','DA9','DA10','DA11','DA12','DA13','DA14','DA15','DA16','DA17','DA18',
    'EN1','EN2','EN3','EN4','EN5','EN6','EN7','EN8','EN9',
    'HA0','HA1','HA2','HA3','HA4','HA5','HA6','HA7','HA8','HA9',
    'IG1','IG2','IG3','IG4','IG5','IG6','IG7','IG8','IG9','IG10','IG11',
    'KT1','KT2','KT3','KT4','KT5','KT6','KT7','KT8','KT9','KT10','KT11','KT12','KT13','KT14','KT15','KT16','KT17','KT18','KT19','KT20','KT21','KT22',
    'RM1','RM2','RM3','RM4','RM5','RM6','RM7','RM8','RM9','RM10','RM11','RM12','RM13','RM14','RM15','RM16','RM17','RM18','RM19','RM20',
    'SM1','SM2','SM3','SM4','SM5','SM6','SM7',
    'TW1','TW2','TW3','TW4','TW5','TW6','TW7','TW8','TW9','TW10','TW11','TW12','TW13','TW14','TW15','TW16','TW17','TW18','TW19','TW20',
    'UB1','UB2','UB3','UB4','UB5','UB6','UB7','UB8','UB9','UB10','UB11',
    'WD17','WD18','WD19','WD23','WD24','WD25',
])

def normalize_postcode(pc):
    pc = pc.strip().upper().replace(' ', '')
    if len(pc) >= 5:
        return pc[:-3] + ' ' + pc[-3:]
    return pc

def get_outcode(pc):
    if ' ' in pc:
        return pc.split(' ')[0]
    return pc[:-3] if len(pc) >= 5 else pc

def is_london_postcode(pc):
    return get_outcode(pc) in LONDON_OUTCODES

print("Processing Price Paid CSVs...", flush=True)
pc_prices = defaultdict(list)
total_rows = 0
london_rows = 0

for fname in ['/tmp/pp-2025.csv', '/tmp/pp-2026.csv']:
    print(f"Processing {fname}...", flush=True)
    count = 0
    london_count = 0
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 4:
                continue
            total_rows += 1
            count += 1
            try:
                price = int(row[1])
                postcode = row[3].strip().strip('"')
                if not postcode:
                    continue
                postcode = normalize_postcode(postcode)
                if is_london_postcode(postcode):
                    pc_prices[postcode].append(price)
                    london_rows += 1
                    london_count += 1
            except Exception:
                continue
    print(f"  Rows: {count:,}, London: {london_count:,}", flush=True)

print(f"Total rows: {total_rows:,}", flush=True)
print(f"Total London transactions: {london_rows:,}", flush=True)
print(f"Total unique London postcodes: {len(pc_prices):,}", flush=True)

with open('/tmp/pc_prices.json', 'w') as f:
    json.dump(dict(pc_prices), f)

unique_pcs = sorted(pc_prices.keys())
with open('/tmp/london_postcodes.json', 'w') as f:
    json.dump(unique_pcs, f)

print(f"Saved {len(unique_pcs):,} unique postcodes", flush=True)
print("Sample:", unique_pcs[:5])

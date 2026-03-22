import csv
import os

local_skills = set()
with open('skills_manifest.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        local_skills.add(row['slug'])

skills_sh_top200 = []
with open('docs/data/skills_sh_all_time_top600.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 200:
            break
        skills_sh_top200.append(row['skillId'])

top200_set = set(skills_sh_top200)

in_top200_not_local = top200_set - local_skills
in_local_not_top200 = local_skills - top200_set

print(f"Total curated skills in manifest: {len(local_skills)}")
print(f"Top 200 skills.sh skills missing from curated manifest: {len(in_top200_not_local)}")
print(f"Curated skills NOT in skills.sh Top 200: {len(in_local_not_top200)}")

missing_sorted = [s for s in skills_sh_top200 if s in in_top200_not_local]
print("\nTop 50 missing from curated (by skills.sh rank):")
for s in missing_sorted[:50]:
    print(f"- {s}")

{\rtf1\ansi\ansicpg1252\cocoartf2862
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import csv\
import random\
import math\
from collections import defaultdict\
\
# CONFIGURABLE\
GROUP_SIZE_MIN = 10\
GROUP_SIZE_MAX = 12\
NUM_WEEKS = 8\
HOST_NAME = "Your Name"\
HOST_EMAIL = "your@email.com"\
INPUT_CSV = "people.csv"\
OUTPUT_CSV = "dinner_groups.csv"\
\
def extract_last_name(full_name):\
    return full_name.strip().split()[-1].lower()\
\
def load_people(filename):\
    people = []\
    with open(filename, newline='') as csvfile:\
        reader = csv.DictReader(csvfile)\
        for row in reader:\
            name = row['name'].strip()\
            email = row['email'].strip()\
            last_name = extract_last_name(name)\
            people.append(\{'name': name, 'email': email, 'family': last_name\})\
    return people\
\
def group_families(people):\
    families = defaultdict(list)\
    for person in people:\
        families[person['family']].append(person)\
    return list(families.values())\
\
def distribute_into_groups(families):\
    random.shuffle(families)\
    groups = []\
    current_group = []\
    current_size = 0\
\
    for family in families:\
        family_size = len(family)\
        if current_size + family_size > GROUP_SIZE_MAX:\
            if current_size >= GROUP_SIZE_MIN:\
                groups.append(current_group)\
                current_group = []\
                current_size = 0\
        current_group.extend(family)\
        current_size += family_size\
\
    if current_group:\
        groups.append(current_group)\
\
    return groups\
\
def assign_weeks(groups):\
    week_assignments = []\
    for i, group in enumerate(groups):\
        week = (i % NUM_WEEKS) + 1\
        week_assignments.append((week, group))\
    return week_assignments\
\
def add_host_to_groups(groups_with_weeks):\
    final_groups = []\
    for week, group in groups_with_weeks:\
        full_group = [\{'name': HOST_NAME, 'email': HOST_EMAIL\}] + group\
        final_groups.append((week, full_group))\
    return final_groups\
\
def save_to_csv(groups_with_weeks, filename):\
    with open(filename, 'w', newline='') as csvfile:\
        fieldnames = ['week', 'group_id', 'name', 'email']\
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)\
        writer.writeheader()\
\
        for i, (week, group) in enumerate(groups_with_weeks, start=1):\
            for person in group:\
                writer.writerow(\{\
                    'week': week,\
                    'group_id': f"Group \{i\}",\
                    'name': person['name'],\
                    'email': person['email']\
                \})\
\
def main():\
    people = load_people(INPUT_CSV)\
    families = group_families(people)\
    groups = distribute_into_groups(families)\
    week_groups = assign_weeks(groups)\
    final_groups = add_host_to_groups(week_groups)\
    save_to_csv(final_groups, OUTPUT_CSV)\
    print(f"\\n\uc0\u9989  Done! Groups saved to: \{OUTPUT_CSV\}\\n")\
\
if __name__ == "__main__":\
    main()\
}
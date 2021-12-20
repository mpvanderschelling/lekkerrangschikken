#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 15:07:46 2020

@author: Davey Struijk
"""

import os
import csv
import random
from elo import rate_1vs1

CSV_FILENAME = 'keldertoplijst2021.csv'
fieldnames = ['Artiest', 'Nummer', 'Youtube-link', 'Rating']

# Load from CSV
with open(CSV_FILENAME) as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=fieldnames, restval='1000.0')
    next(reader) # skip header
    tracks = [row for row in reader]

# Comparison loop (Press Ctrl+C to exit)
while True:
    try:
        w = os.get_terminal_size().columns
        a, b = random.sample(range(len(tracks)), 2)
        print("=" * w)
        print("(1)".center(w))
        print("{Artiest} - {Nummer}".format(**tracks[a]).center(w))
        print("{Youtube-link}".format(**tracks[a]).center(w))
        print("")
        print("(2)".center(w))
        print("{Artiest} - {Nummer}".format(**tracks[b]).center(w))
        print("{Youtube-link}".format(**tracks[b]).center(w))
        print("=" * w)
        choice = input("> ")
        if choice.lower() == '1':
            tracks[a]['Rating'], tracks[b]['Rating'] = rate_1vs1(
                    float(tracks[a]['Rating']), float(tracks[b]['Rating']))
        elif choice.lower() == '2':
            tracks[b]['Rating'], tracks[a]['Rating'] = rate_1vs1(
                    float(tracks[b]['Rating']), float(tracks[a]['Rating']))
        else:
            print('Invalid choice')
        print("")
    except KeyboardInterrupt:
        break

# Save to CSV
with open(CSV_FILENAME, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tracks)

# Print ratings
for track in sorted(tracks, key=lambda t: float(t['Rating'])):
    print("[{Rating}] {Artiest} - {Nummer}".format(**track))


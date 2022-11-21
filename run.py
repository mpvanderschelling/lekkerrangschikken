#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 15:07:46 2020

@author: Davey Struijk
"""

import csv
import os
import random

CSV_FILENAME = "keldertoplijst2022.csv"
fieldnames = ["Artiest", "Nummer", "Youtube-link", "Rating"]


def expect(rating, other_rating):
    """The "E" function in Elo. It calculates the expected score of the
    first rating by the second rating.
    """
    # http://www.chess-mind.com/en/elo-system
    diff = other_rating - rating
    return 1.0 / (1 + 10 ** (diff / 400))


def calc_elo(rating, other_rating, K=10):
    return (rating + K * (1 - expect(rating, other_rating)), other_rating + K * (0 - expect(other_rating, rating)))


# Load from CSV
with open(CSV_FILENAME) as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=fieldnames, restval="1000.0")
    next(reader)  # skip header
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
        if choice.lower() == "1":
            tracks[a]["Rating"], tracks[b]["Rating"] = calc_elo(float(tracks[a]["Rating"]), float(tracks[b]["Rating"]))
        elif choice.lower() == "2":
            tracks[b]["Rating"], tracks[a]["Rating"] = calc_elo(float(tracks[b]["Rating"]), float(tracks[a]["Rating"]))
        else:
            print("Invalid choice")
        print("")
    except KeyboardInterrupt:
        break

# Save to CSV
with open(CSV_FILENAME, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sorted(tracks, key=lambda t: float(t["Rating"]), reverse=True))

# Print ratings
for track in sorted(tracks, key=lambda t: float(t["Rating"]), reverse=True):
    print("[{Rating}] {Artiest} - {Nummer}".format(**track))

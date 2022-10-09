#!/usr/bin/env python3

from collections import defaultdict
import warnings
import icalendar
import icalendar.prop
import argparse
import requests
import pathlib
import datetime
import re
import recurring_ical_events

# Load arguments
argp = argparse.ArgumentParser(description="_")
argp.add_argument("srcs", nargs="+", default=[], help="Source files, either as URL or ical file.")
argp.add_argument("--from", type=str, default="-1week!", help="Evaluate events from. Relative times allowed. Exclamation mark rounds down.")
argp.add_argument("--until", type=str, default="now", help="Evaluate events until. See above.")
args = argp.parse_args()

eval_from = datetime.date.today() - datetime.timedelta(days=7)
eval_until = datetime.date.today()

tagcount = defaultdict(datetime.timedelta)

for src in args.srcs:
    if src[:4] == "http":
        s = requests.get(src).text
    elif pathlib.Path(src).suffix in (".ics", ".ical"):
        with open(src, "r") as f:
            s = f.read()
    else: 
        raise ValueError("Source file not supported.")
    cal = icalendar.Calendar.from_ical(s)

    for event in recurring_ical_events.of(cal).between(eval_from, eval_until):
        #print(event.get("SUMMARY"))

        try:
            duration = event.get("DTEND").dt - event.get("DTSTART").dt
        except AttributeError:
            warnings.warn("Not implemented, I am lazy!")
            continue
        
        sometag = False
        for tagspace in re.findall(r'\[(.*?)\]',str(event.get("SUMMARY"))):
            sometag = True
            for tag_1 in tagspace.split(","):
                for tag in tag_1.split("*"):
                    if tag not in "xX":
                        tagcount[tag] += duration
        if not sometag:
            tagcount["???"] += duration

for t, k in sorted([(v, k) for k, v in tagcount.items()]):
    print(f"{k:10}: {str(t)}")

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
from yaml import safe_load

# Load arguments
argp = argparse.ArgumentParser(description="_")
argp.add_argument("srcs", nargs="+", default=[], help="Source files, either as URL or ical file.")
argp.add_argument("--since", type=str, default=(datetime.date.today() - datetime.timedelta(days=7)).isoformat(), help="Evaluate events from. Relative times allowed. Exclamation mark rounds down.")
argp.add_argument("--until", type=str, default=datetime.date.today().isoformat(), help="Evaluate events until. See above.")
argp.add_argument("--tag", "-t", nargs="+", type=str, default=None, help="Evaluate only given tags.")
argp.add_argument("--cache", "-c", action="store_true")
args = argp.parse_args()

eval_from = datetime.date.fromisoformat(args.since)
eval_until = datetime.date.fromisoformat(args.until)

print(f"Events from {eval_from.isoformat()} to {eval_until.isoformat()}")

icals_loaded = []

for src in args.srcs:
    if src[:4] == "http":
        icals_loaded.append((pathlib.Path(src).stem, requests.get(src).text, {}))
    elif pathlib.Path(src).suffix.lower() in (".ics", ".ical"):
        with open(src, "r") as f:
            s = f.read()
        icals_loaded.append((pathlib.Path(src).stem, s, {}))
    elif pathlib.Path(src).suffix.lower() in (".yaml", "yml"):
        with open(src, "r") as f:
            confs = safe_load(f)
        for name, conf in confs.items():
            cachefile = pathlib.Path(src).parent.parent / "cache" / name
            if args.cache and not cachefile.exists() or not args.cache:
                s = requests.get(conf["url"]).text
                with open(cachefile, "w") as f:
                    f.write(s)
            else:
                with open(cachefile, "r") as f:
                    s = f.read()

            icals_loaded.append((name, s, conf["tagrules"] if "tagrules" in conf else {}))
    else: 
        raise ValueError("Source file not supported.")

tagcount = defaultdict(datetime.timedelta)
untagged_events = datetime.timedelta(seconds=0)

for ical_name, ical_text, ical_tagrules in icals_loaded:
    #print(f"Processing calendar {ical_name}.")
    cal = icalendar.Calendar.from_ical(ical_text)

    for event in recurring_ical_events.of(cal).between(eval_from, eval_until):
        #print(event.get("SUMMARY"))

        try:
            duration = event.get("DTEND").dt - event.get("DTSTART").dt
        except AttributeError:
            warnings.warn("Not implemented, I am lazy!")
            continue
        
        sometag = False
        tagspaces = re.findall(r'\[(.*?)\]',str(event.get("SUMMARY")))
        for tagrule, tag in ical_tagrules.items():
            if event.get("SUMMARY").strip() == tagrule:
                tagspaces.append(tag)
        for tagspace in tagspaces:
            sometag = True
            for tag_1 in tagspace.split(","):
                for tag in tag_1.split("*"):
                    if tag in "xX":
                        continue
                    elif args.tag is None:
                        tagcount[tag] += duration
                    elif tag in args.tag:
                        tagcount[tag] += duration
                        print(event.get("SUMMARY"))
        if not sometag:
            untagged_events += duration

for t, k in sorted([(v, k) for k, v in tagcount.items()]):
    print(f"{k:10}: {str(t)}")

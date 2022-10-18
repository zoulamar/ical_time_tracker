# ical_time_tracker

How to track time spend on different things? 
Use dedicated apps which force you to insert what you actually did even tough you have your schedule known in `ical`?
Don't that seem duplicate?

This assumes, that the "summaries" of the events, i.e., the event names, are tagged by bracket-enclosed tags.
For each tag a timecount is gathered by simply summing corresponding durations. 

# Features:

- [x] Aggregate time spent in individual tags.
- [ ] Add default tag (event which counts if no other event is present.)
- [ ] Add YAML config to allow automatization of cal download via private links.
  - [ ] Each calendar may have default tag to insert to untagged events.
- [ ] Overlapping event detection.
- [ ] Use [ical Events](https://icalevents.readthedocs.io/en/latest/), which is originally supported instead of recurring_events_whatewer_lib.

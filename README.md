# ical_time_tracker

How to track time spend on different things? 
Use dedicated apps which force you to insert what you actually did even tough you have your schedule known in `ical`?
Don't that seem duplicate?

This assumes, that the "summaries" of the events, i.e., the event names, are tagged by bracket-enclosed tags.
For each tag a timecount is gathered by simply summing corresponding durations. 

# Features

- [ ] Use [ical Events](https://icalevents.readthedocs.io/en/latest/), which is originally supported instead of recurring_events_whatewer_lib.
- [ ] Yaml config file.
  - Sets up watched URLs
  - Sets up overlapping event resolution policy.
- [ ] Tag properties: Yaml-level defined properties for particular tags. E.g. `Kafe` is equivalent to `Coffee`, `Káva` etc. Also, its duration shall be subtracted from overlapping event.
- [ ] Subtags: E.g. `NTK.dilna` to denote particular activity unique for a tag.

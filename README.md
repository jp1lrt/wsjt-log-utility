WSJT Log Utility v0.11
=====================

LoTW-friendly log recovery and ADIF splitting utility.

Normally, QSOs are already saved in wsjtx_log.adi.
However, in cases where wsjtx_log.adi has been lost (e.g. system failure,
disk crash, OS reinstall), only wsjtx.log may remain.

WSJT Log Utility is intended for such situations: it can reconstruct QSOs
from wsjtx.log and export them to ADIF for LoTW upload. It can also split
an existing wsjtx_log.adi (or any ADIF file) by date/time range so that
multiple operating locations (multiple grids) can be uploaded correctly
using TQSL Station Locations.

Typical use cases
-----------------
- wsjtx_log.adi was lost, but wsjtx.log still exists
- Multiple grid locations were used on the same PC
- QSOs need to be split by date/time for correct Station Location
- Historical logs need partial recovery (e.g. 6m or selected periods)
- Portable / special operations where you want clear output filenames

How to use
----------
1) Run wsjt_log_utility.py (or a built EXE)
2) Select an input file:
   - wsjtx.log      (CSV-style text)
   - wsjtx_log.adi  (ADIF)
3) Enter Start/End UTC: YYYY-MM-DD HH:MM:SS
4) (Optional) Fill filename metadata (grid, /P, POTA, SOTA, etc.)
5) Click "Convert / Split"
6) An ADIF file will be created in the selected output folder

Uploading to LoTW
-----------------
- Open TQSL
- Sign and upload the generated ADIF file
- Select the correct Station Location (grid) in TQSL

IMPORTANT:
This tool does NOT write your own grid locator into the ADIF.
Station Location in TQSL must be used to assign the correct grid.

Notes & limitations
-------------------
- All times are handled strictly in UTC
- wsjtx.log does NOT contain your own grid locator
- If multiple grids were used, logs must be split by date/time based on
  the operator’s knowledge
- The tool does not guess or infer grid locations
- Designed for reliability and LoTW compatibility

Security
--------
- If distributed as an EXE, include a SHA-256 checksum
- Users are encouraged to scan before running

------------------------------------------------------------
Author and License
------------------------------------------------------------

Author:
Yoshiharu (JP1LRT)

This tool was developed collaboratively by the author and ChatGPT.

WSJT Log Utility is free software.
It may be redistributed freely, with or without modification.
No warranty is provided.

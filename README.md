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

WSJT Log Utility v0.11
=====================

LoTW 対応ログ復旧・ADIF 分割ユーティリティ

通常、交信データは wsjtx_log.adi に保存されています。
しかし、PCトラブルやディスク障害、OS再インストール等により
wsjtx_log.adi が失われ、wsjtx.log だけが残る場合があります。

WSJT Log Utility はそのような状況を想定し、wsjtx.log に残っている
情報を元に交信記録を ADIF として再構築し、LoTW へアップロード
できるようにするためのツールです。

また、wsjtx_log.adi（ADIF）が残っている場合でも、同一PCで複数の
グリッド・ロケーターから運用していたケースでは、日時を基準に
ADIF を分割してから、それぞれを正しい Station Location で TQSL
署名・アップロードする必要があります。本ツールはその分割にも対応します。

使い方
------
1) wsjt_log_utility.py（またはビルド済み EXE）を起動します
2) 入力ファイルを選択します
   - wsjtx.log      （CSV形式のテキスト）
   - wsjtx_log.adi  （ADIF）
3) 抽出したい期間の開始・終了日時（UTC）を入力します
   形式：YYYY-MM-DD HH:MM:SS
4) （任意）ファイル名用のメタ情報（グリッド、/P、POTA、SOTA等）を入力します
5) 「Convert / Split」を押します
6) 指定したフォルダに ADIF が作成されます

LoTW へのアップロードについて
----------------------------
- TQSL を起動します
- 作成された ADIF ファイルを署名・アップロードします
- 正しい Station Location（自局グリッド）を選択してください

重要：
本ツールは ADIF に自局のグリッド・ロケーターを「書き込みません」。
LoTW では Station Location によって自局情報（グリッド）を管理するため、
この設計は意図的なものです。

注意事項・制限
--------------
- 日時はすべて UTC として扱われます
- wsjtx.log には自局グリッド情報は含まれていません
- 複数グリッド運用の場合、オペレーター自身が日時を基準に分割する必要があります
- 本ツールはグリッドを自動推測することはありません
- LoTW 互換性と安全性を最優先に設計されています

------------------------------------------------------------
作者およびライセンス
------------------------------------------------------------

作者：
Yoshiharu（JP1LRT）

本ツールは作者と ChatGPT による共同検討・設計をもとに開発されました。

WSJT Log Utility は完全にフリーなソフトウェアです。
改変・再配布は自由に行えます。
本ソフトウェアは無保証です。


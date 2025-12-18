# WSJT Log Utility v0.13
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

## New in v0.13

- Band filter support (HF / VHF / UHF up to 23cm)
- Convert or split logs for a specific band only
- Useful for VHF/UHF, microwave, or contest log management
- Band detection based on frequency (MHz)

How to use
----------
1) Run wsjt_log_utility.py (or a built EXE)
2) Select an input file:
   - wsjtx.log      (CSV-style text)
   - wsjtx_log.adi  (ADIF)
3. Enter Start/End UTC: YYYY-MM-DD HH:MM:SS
4. (Optional) Select a band filter (ALL / 160m ... 23cm)
5. (Optional) Fill filename metadata (grid, /P, POTA, SOTA, etc.)
6. Click "Convert / Split"
7) An ADIF file will be created in the selected output folder

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

WSJT Log Utility v0.13
=====================
LoTW 対応ログ復旧・ADIF 分割ユーティリティ
通常、QSO は  wsjtx_log.adi に保存されています。
しかし、システム障害・ディスククラッシュ・OS再インストールなどにより wsjtx_log.adi が失われた場合、wsjtx.log のみが残ることがあります。
WSJT Log Utility は、そうした状況でのログ復旧を目的としたツールです。
wsjtx.log から QSO を再構築し、LoTW へのアップロード用に ADIF 形式で出力できます。
また、既存の wsjtx_log.adi（または任意の ADIF ファイル）を日付・時刻で分割し、TQSL の Station Location に応じたアップロードを可能にします。

主な用途
• 	wsjtx_log.adi を紛失したが、 wsjtx.log は残っている
• 	同一 PC で複数のグリッドロケーターを使用した
• 	Station Location に応じて QSO を日付・時刻で分割したい
• 	過去のログから一部期間のみ復旧したい（例：6m シーズン）
• 	移動運用・特別運用で、出力ファイル名を明確にしたい

v0.13 の新機能
• 	バンドフィルター対応（HF / VHF / UHF ～ 23cm）
• 	特定バンドのみを変換・分割可能
• 	VHF/UHF・マイクロ波・コンテストログ管理に有用
• 	周波数（MHz）に基づくバンド自動判定

使い方
1. 	wsjt_log_utility.py（またはビルド済み EXE）を起動
2. 	入力ファイルを選択：
• 	   wsjtx.log　（CSV形式テキスト）
• 	   wsjtx_log.adi（ADIF形式）
3. 	UTC で開始・終了日時を入力（YYYY-MM-DD HH:MM:SS）
4. 	（任意）バンドフィルターを選択（ALL / 160m ～ 23cm）
5. 	（任意）ファイル名用メタデータを入力（Grid, /P, POTA, SOTA など）
6. 	「変換 / 分割」ボタンをクリック
7. 	指定した出力フォルダに ADIF ファイルが生成されます

LoTW へのアップロード
1. 	TQSL を起動
2. 	生成された ADIF ファイルを署名・アップロード
3. 	TQSL で正しい Station Location（グリッド）を選択
⚠️ 重要：
このツールは 自局のグリッドロケーターを ADIF に書き込みません。
TQSL 側で Station Location を正しく設定してください。

注意事項・制限
• 	すべての時刻は UTC で処理されます
• 	 には自局のグリッド情報は含まれません
• 	複数のグリッドを使用した場合、オペレータの判断でログを分割する必要があります
• 	グリッドロケーターの推定や補完は行いません
• 	LoTW 互換性と信頼性を重視して設計されています

セキュリティについて
• 	EXE 形式で配布する場合は SHA-256 チェックサムを添付してください
• 	実行前にウイルススキャンを推奨します

著者とライセンス
著者：
Yoshiharu（JP1LRT）
本ツールは、著者と ChatGPT による共同開発により設計・実装されました。
WSJT Log Utility はフリーソフトウェアです。
改変の有無を問わず、自由に再配布可能です。
無保証で提供されます。


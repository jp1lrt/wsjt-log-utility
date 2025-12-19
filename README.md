# WSJT Log Utility v0.13

<img width="822" height="652" alt="WSJT Log Utility v0.13 main screen" src="https://github.com/user-attachments/assets/bd43a497-0b23-4a6c-b959-f1476fcc7760" />

A small Windows GUI tool primarily for WSJT-X / JTDX users, designed to help prepare and split ADIF logs for correct electronic uploads.
Although often used with digital mode logs, the utility itself is not limited to any specific operating mode.

Have you ever lost `wsjtx_log.adi` after a PC crash or reinstall?
WSJT Log Utility helps you recover QSOs from `wsjtx.log`,
split ADIF files by date/time, and prepare clean uploads for LoTW.

While the tool is commonly used with FT8 / FT4 logs, the ADIF splitting
function itself is mode-agnostic and can also be used to split ADIF files
generated from CW, SSB, or mixed-mode operations when preparing uploads.

Normally, QSOs are already saved in wsjtx_log.adi.
However, in cases where wsjtx_log.adi has been lost (e.g. system failure,
disk crash, OS reinstall), only wsjtx.log may remain.

WSJT Log Utility is intended for such situations: it can reconstruct QSOs
from wsjtx.log and export them to ADIF for LoTW upload. It can also split
an existing wsjtx_log.adi (or any ADIF file) by date/time range so that
multiple operating locations (multiple grids) can be uploaded correctly
using TQSL Station Locations.

## Download

Get the latest release here:
https://github.com/jp1lrt/wsjt-log-utility/releases

Recommended for most users:
- `wsjt_log_utility.exe` (single EXE, no installation required)


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
3. Enter Start/End UTC: YYYY-MM-DD HH:MM:SS
4. (Optional) Select a band filter (ALL / 160m ... 23cm)
5. (Optional) Fill filename metadata (grid, /P, POTA, SOTA, etc.)
6. Click "Convert / Split"
7) An ADIF file will be created in the selected output folder

## New in v0.13

- Band filter support (HF / VHF / UHF up to 23cm)
- Convert or split logs for a specific band only
- Useful for VHF/UHF, microwave, or contest log management
- Band detection based on frequency (MHz)

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

---

## 日本語説明 / Japanese description
WSJT-X / JTDX ユーザー向けの、Windows 用 GUI ユーティリティです。

PC クラッシュや OS 再インストールなどで  
`wsjtx_log.adi` を失ってしまったことはありませんか？

**WSJT Log Utility** は、`wsjtx.log` から QSO データを復元し、  
LoTW へ正しくアップロードできる ADIF ファイルを作成するためのツールです。  
また、日付・時刻で ADIF ファイルを分割することで、  
移動運用や複数グリッド運用のログ整理にも対応します。

通常、QSO は `wsjtx_log.adi` に保存されていますが、  
システム障害・ディスク障害・OS 再インストールなどの状況では  
`wsjtx.log` だけが残るケースがあります。

本ツールは、そのような状況を想定して設計されています。

---

## ダウンロード

最新版はこちらから入手できます：  
https://github.com/jp1lrt/wsjt-log-utility/releases

通常は以下をダウンロードしてください：

- **wsjt_log_utility.exe**  
  （単体 EXE ファイル・インストール不要）

---

## 主な利用シーン

- `wsjtx_log.adi` は失われたが、`wsjtx.log` は残っている
- 同一 PC で複数のグリッドロケーターから運用していた
- 過去ログの一部だけを復元・整理したい
- 移動運用・特別運用で、出力ファイル名を明確にしたい

---

## v0.13 の新機能

- バンドフィルター対応（HF / VHF / UHF ～ 23cm）
- 特定バンドのみを対象に変換・分割が可能
- VHF/UHF、マイクロ波、コンテストログ整理に便利
- 周波数（MHz）に基づく自動バンド判定

---

## 使い方

1. `wsjt_log_utility.exe`（または Python 版）を起動
2. 入力ファイルを選択  
   - `wsjtx.log`（CSV 形式テキスト）  
   - `wsjtx_log.adi`（ADIF 形式）
3. 開始・終了日時（UTC）を入力（YYYY-MM-DD HH:MM:SS）
4. （任意）バンドフィルターを指定（ALL / 160m ～ 23cm）
5. （任意）ファイル名用メタデータを入力（Grid / POTA / SOTA など）
6. 「Convert / Split」をクリック
7. 指定した出力フォルダに ADIF ファイルが生成されます

---

## LoTW へのアップロード

1. TQSL を起動
2. 生成された ADIF ファイルを署名・アップロード
3. TQSL で正しい Station Location（グリッド）を選択

**重要**  
本ツールは ADIF に自局のグリッドロケーターを書き込みません。  
必ず TQSL の Station Location を使って正しいグリッドを指定してください。

---

## 注意点・制限事項

- すべての時刻は UTC で処理されます
- ADIF には自局グリッドは含まれません
- 複数グリッド運用時は、オペレーターの判断で日時分割してください
- LoTW 互換性と信頼性を重視して設計されています

---

## セキュリティ

- EXE 配布時には SHA-256 チェックサムを提供しています
- 実行前にウイルススキャンを行うことを推奨します

---

## 作者・ライセンス

Author: Yoshiharu (JP1LRT)

本ツールはフリーソフトウェアです。  
改変の有無にかかわらず再配布可能です。  
本ソフトウェアの使用によって生じたいかなる損害についても、作者は責任を負いません。


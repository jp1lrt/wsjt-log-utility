# WSJT Log Utility v0.13
# LoTW-friendly log recovery and ADIF splitting utility.
#
# Author: Yoshiharu (JP1LRT)
# Developed collaboratively by the author and ChatGPT.
#
# Supports:
#   - wsjtx.log (CSV-style text) -> ADIF export with date/time filter (+ optional band filter)
#   - wsjtx_log.adi (ADIF) -> ADIF split by date/time filter (+ optional band filter)
#
# Notes:
#   - All times are treated as UTC.
#   - This tool does NOT write your own grid into ADIF. Use TQSL Station Location.

import csv
import datetime as dt
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

APP_NAME = "WSJT Log Utility"
APP_VERSION = "0.13"
AUTHOR = "Yoshiharu (JP1LRT)"


def _about_en() -> str:
    return f"""WSJT Log Utility
Version {APP_VERSION}

LoTW-friendly log recovery and ADIF splitting utility.

Author:
Yoshiharu (JP1LRT)

Developed collaboratively by the author and ChatGPT.

WSJT Log Utility helps amateur radio operators recover and split
WSJT-X / JTDX logs when wsjtx_log.adi is missing, or when operating
from multiple grid locations, portable operations, or special events.

This software is provided free of charge.
No warranty is given, and user support may not be available.
Future updates may be released if circumstances allow.

73 and enjoy!
"""


def _about_ja() -> str:
    return f"""WSJT Log Utility
Version {APP_VERSION}

LoTW 対応ログ復旧・ADIF 分割ユーティリティ

作者：
Yoshiharu（JP1LRT）

本ツールは作者と ChatGPT による共同検討・設計に基づき開発されています。

WSJT Log Utility は、wsjtx_log.adi が失われた場合や、
複数のグリッド・ロケーター、移動運用、特別運用などにおいて、
WSJT-X / JTDX のログを正しく LoTW へ反映させることを目的としています。

本ソフトウェアは完全にフリーで提供されます。
無保証であり、サポートは行えない場合があります。
将来的なアップデートは状況により行われる可能性があります。

73 & Enjoy!
"""


# -------------------------
# i18n
# -------------------------

TEXT = {
    "EN": {
        "menu_help": "Help",
        "menu_language": "Language",
        "lang_en": "English",
        "lang_ja": "日本語",
        "about": "About",
        "about_en": "About (English)",
        "about_ja": "About (日本語)",

        "input": "Input",
        "input_file": "Input file (wsjtx.log or wsjtx_log.adi):",
        "browse": "Browse…",
        "no_file": "(no file)",
        "select_input_title": "Select wsjtx.log or wsjtx_log.adi",

        "det_adif": "Detected input type: ADIF (wsjtx_log.adi or ADIF)",
        "det_log": "Detected input type: wsjtx.log (CSV-style text)",
        "det_unknown": "Detected input type: Unknown (will try best effort)",

        "time_filter": "Date/Time filter (UTC)",
        "start": "Start (YYYY-MM-DD HH:MM:SS):",
        "end": "End (YYYY-MM-DD HH:MM:SS):",

        "options": "Options",
        "grid_precision": "Remote grid precision (4/6/8):",
        "include_off": "Include QSO_DATE_OFF / TIME_OFF (wsjtx.log only)",
        "band_filter": "Band filter:",
        "band_all": "All bands",

        "meta": "Output naming metadata (optional)",
        "station_call": "Station callsign (for filename):",
        "grid": "Grid locator (for filename):",
        "pota": "POTA:",
        "sota": "SOTA:",
        "iota": "IOTA:",
        "wwff": "WWFF:",
        "flags": "Flags:",

        "output": "Output",
        "output_folder": "Output folder:",
        "preview": "Preview:",
        "select_out_title": "Select output folder",

        "convert": "Convert / Split",
        "quit": "Quit",

        "err_missing_input_title": "Missing input",
        "err_missing_input": "Please select an input file.",
        "err_invalid_time_title": "Invalid time range",
        "err_missing_out_title": "Missing output folder",
        "err_missing_out": "Please select a valid output folder.",

        "preview_invalid_range": "(invalid time range)",
        "preview_hint": "(enter Start/End in UTC: YYYY-MM-DD HH:MM:SS)",

        "done_title": "Done",
        "done_adif": "Input type: ADIF\nTotal records scanned: {total}\nRecords exported: {kept}\n\nSaved:\n{path}",
        "done_log": "Input type: wsjtx.log\nLines scanned: {total}\nQSOs exported: {kept}\n\nSaved:\n{path}",
        "failed_title": "Failed",
    },
    "JA": {
        "menu_help": "ヘルプ",
        "menu_language": "言語",
        "lang_en": "English",
        "lang_ja": "日本語",
        "about": "このソフトについて",
        "about_en": "このソフトについて（English）",
        "about_ja": "このソフトについて（日本語）",

        "input": "入力",
        "input_file": "入力ファイル（wsjtx.log / wsjtx_log.adi）：",
        "browse": "参照…",
        "no_file": "（未選択）",
        "select_input_title": "wsjtx.log / wsjtx_log.adi を選択",

        "det_adif": "入力種別：ADIF（wsjtx_log.adi または ADIF）",
        "det_log": "入力種別：wsjtx.log（CSV形式テキスト）",
        "det_unknown": "入力種別：不明（可能な範囲で処理します）",

        "time_filter": "日時フィルタ（UTC）",
        "start": "開始（YYYY-MM-DD HH:MM:SS）：",
        "end": "終了（YYYY-MM-DD HH:MM:SS）：",

        "options": "オプション",
        "grid_precision": "相手局グリッド精度（4/6/8）：",
        "include_off": "QSO終了時刻を含める（wsjtx.log のみ）",
        "band_filter": "バンド指定：",
        "band_all": "すべて",

        "meta": "出力ファイル名メタデータ（任意）",
        "station_call": "自局コールサイン（ファイル名用）：",
        "grid": "グリッドロケータ（ファイル名用）：",
        "pota": "POTA：",
        "sota": "SOTA：",
        "iota": "IOTA：",
        "wwff": "WWFF：",
        "flags": "フラグ：",

        "output": "出力",
        "output_folder": "出力フォルダ：",
        "preview": "プレビュー：",
        "select_out_title": "出力フォルダを選択",

        "convert": "変換 / 分割",
        "quit": "終了",

        "err_missing_input_title": "入力ファイルなし",
        "err_missing_input": "入力ファイルを選択してください。",
        "err_invalid_time_title": "日時範囲エラー",
        "err_missing_out_title": "出力フォルダなし",
        "err_missing_out": "有効な出力フォルダを選択してください。",

        "preview_invalid_range": "（日時範囲が不正です）",
        "preview_hint": "（UTCで開始/終了を入力：YYYY-MM-DD HH:MM:SS）",

        "done_title": "完了",
        "done_adif": "入力種別：ADIF\n総レコード数：{total}\n出力レコード数：{kept}\n\n保存先：\n{path}",
        "done_log": "入力種別：wsjtx.log\n総行数：{total}\n出力QSO数：{kept}\n\n保存先：\n{path}",
        "failed_title": "失敗",
    }
}

DEFAULT_LANG = "EN"  # start in English


# 23cmまで
BAND_CODES = ["ALL", "160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","2m","1.25m","70cm","33cm","23cm"]


# -------------------------
# Utilities
# -------------------------

def parse_utc_datetime(s: str) -> dt.datetime:
    return dt.datetime.strptime(s.strip(), "%Y-%m-%d %H:%M:%S")

def fmt_date(d: dt.datetime) -> str:
    return d.strftime("%Y%m%d")

def fmt_time(d: dt.datetime) -> str:
    return d.strftime("%H%M%S")

def mhz_to_band(mhz: float) -> str:
    if 1.8 <= mhz < 2.0: return "160m"
    if 3.5 <= mhz < 4.0: return "80m"
    if 5.0 <= mhz < 5.5: return "60m"
    if 7.0 <= mhz < 7.3: return "40m"
    if 10.1 <= mhz < 10.15: return "30m"
    if 14.0 <= mhz < 14.35: return "20m"
    if 18.068 <= mhz < 18.168: return "17m"
    if 21.0 <= mhz < 21.45: return "15m"
    if 24.89 <= mhz < 24.99: return "12m"
    if 28.0 <= mhz < 29.7: return "10m"
    if 50.0 <= mhz < 54.0: return "6m"
    if 144.0 <= mhz < 148.0: return "2m"
    if 222.0 <= mhz < 225.0: return "1.25m"
    if 420.0 <= mhz < 450.0: return "70cm"
    if 902.0 <= mhz < 928.0: return "33cm"
    if 1240.0 <= mhz < 1300.0: return "23cm"
    return ""

def sanitize_token(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[^A-Za-z0-9_\-\/]+", "", s)
    return s

def build_output_filename(station_call: str, start_dt: dt.datetime, end_dt: dt.datetime, grid: str,
                          portable_flags: list[str], pota: str, sota: str, iota: str, wwff: str,
                          suffix: str = ".adi") -> str:
    call = sanitize_token(station_call) or "OUTPUT"
    start_s = start_dt.strftime("%Y-%m-%d")
    end_s = end_dt.strftime("%Y-%m-%d")
    parts = [call, f"{start_s}-{end_s}"]
    g = sanitize_token(grid)
    if g:
        parts.append(g.upper())
    tags = []
    for f in portable_flags:
        if f:
            tags.append(sanitize_token(f).replace("/", ""))
    if pota.strip():
        tags.append("POTA-" + sanitize_token(pota).upper())
    if sota.strip():
        tags.append("SOTA-" + sanitize_token(sota).upper())
    if iota.strip():
        tags.append("IOTA-" + sanitize_token(iota).upper())
    if wwff.strip():
        tags.append("WWFF-" + sanitize_token(wwff).upper())
    if tags:
        parts.append("_".join(tags))
    return "_".join(parts) + suffix


def default_output_dir() -> str:
    """Prefer the folder where the exe/script is located."""
    try:
        if getattr(sys, "frozen", False) and hasattr(sys, "executable"):
            return os.path.dirname(os.path.abspath(sys.executable))
    except Exception:
        pass
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        return os.path.expanduser("~")


# -------------------------
# wsjtx.log (CSV) -> ADIF
# -------------------------

def detect_wsjtx_csv(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.count(",") < 5:
                    return False
                first = line.split(",")[0].strip()
                return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", first))
    except Exception:
        return False
    return False

def convert_wsjtx_log_to_adif(csv_path: str, out_path: str, start_dt: dt.datetime, end_dt: dt.datetime,
                             grid_digits: int = 8, include_time_off: bool = True, band_filter: str = "ALL") -> tuple[int, int]:
    total = 0
    written = 0
    with open(csv_path, "r", encoding="utf-8", errors="replace", newline="") as f_in, \
         open(out_path, "w", encoding="utf-8", newline="") as f_out:
        reader = csv.reader(f_in)
        f_out.write(f"Generated by {APP_NAME} v{APP_VERSION}\n")
        f_out.write("<ADIF_VER:5>3.1.4\n<EOH>\n")
        for row in reader:
            if not row or len(row) < 9:
                continue
            s_date = row[0].strip()
            s_time = row[1].strip()
            e_date = row[2].strip() if len(row) > 2 else ""
            e_time = row[3].strip() if len(row) > 3 else ""
            call = row[4].strip() if len(row) > 4 else ""
            rgrid = row[5].strip() if len(row) > 5 else ""
            freq = row[6].strip() if len(row) > 6 else ""
            mode = row[7].strip() if len(row) > 7 else ""
            rst_s = row[8].strip() if len(row) > 8 else ""
            rst_r = row[9].strip() if len(row) > 9 else ""

            try:
                t_on = dt.datetime.strptime(f"{s_date} {s_time}", "%Y-%m-%d %H:%M:%S")
            except Exception:
                continue

            total += 1
            if not (start_dt <= t_on < end_dt):
                continue

            band = ""
            try:
                mhz = float(freq) if freq else 0.0
                band = mhz_to_band(mhz)
            except Exception:
                band = ""

            if band_filter and band_filter != "ALL":
                if band != band_filter:
                    continue

            rgrid = (rgrid or "").strip()
            if rgrid and grid_digits in (4, 6, 8):
                rgrid = rgrid[:grid_digits]

            rec = []
            def add(tag: str, val: str):
                if val is None:
                    return
                val = str(val)
                if val == "":
                    return
                rec.append(f"<{tag}:{len(val)}>{val}")

            add("CALL", call)
            add("QSO_DATE", fmt_date(t_on))
            add("TIME_ON", fmt_time(t_on))
            if include_time_off and e_date and e_time:
                try:
                    t_off = dt.datetime.strptime(f"{e_date} {e_time}", "%Y-%m-%d %H:%M:%S")
                    add("QSO_DATE_OFF", fmt_date(t_off))
                    add("TIME_OFF", fmt_time(t_off))
                except Exception:
                    pass
            add("FREQ", freq)
            add("BAND", band)
            add("MODE", mode)
            add("RST_SENT", rst_s)
            add("RST_RCVD", rst_r)
            add("GRIDSQUARE", rgrid)
            rec.append("<EOR>")
            f_out.write("".join(rec) + "\n")
            written += 1
    return total, written


# -------------------------
# ADIF splitting (preserve records)
# -------------------------

_EOR_RE = re.compile(r"<\s*eor\s*>", re.IGNORECASE)
_FIELD_RE = re.compile(r"<\s*([A-Za-z0-9_]+)\s*:\s*(\d+)(?:\s*:[^>]*)?\s*>", re.IGNORECASE)

def detect_adif(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read(4096)
        low = txt.lower()
        return ("<eoh" in low) or ("<adif_ver" in low) or ("<eor" in low)
    except Exception:
        return False

def extract_field_value(text: str, field_name: str):
    field_name = field_name.lower()
    i = 0
    while True:
        m = _FIELD_RE.search(text, i)
        if not m:
            return None
        name = m.group(1).lower()
        length = int(m.group(2))
        val_start = m.end()
        val_end = val_start + length
        val = text[val_start:val_end]
        if name == field_name:
            return val.strip()
        i = val_end

def record_time_on_utc(record_text: str):
    qso_date = extract_field_value(record_text, "QSO_DATE")
    time_on = extract_field_value(record_text, "TIME_ON")
    if not qso_date or not time_on:
        return None
    qso_date = qso_date.strip()
    time_on = time_on.strip()
    if len(time_on) == 4:
        time_on = time_on + "00"
    if len(time_on) != 6:
        return None
    try:
        return dt.datetime.strptime(qso_date + time_on, "%Y%m%d%H%M%S")
    except Exception:
        return None

def split_adif_by_datetime(adif_path: str, out_path: str, start_dt: dt.datetime, end_dt: dt.datetime, band_filter: str = "ALL"):
    with open(adif_path, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()

    lower = txt.lower()
    eoh_idx = lower.find("<eoh>")
    header = ""
    records_blob = txt
    if eoh_idx != -1:
        header = txt[:eoh_idx + len("<EOH>")]
        records_blob = txt[eoh_idx + len("<EOH>"):]

    parts = _EOR_RE.split(records_blob)
    total = 0
    kept = 0

    with open(out_path, "w", encoding="utf-8", newline="") as f_out:
        f_out.write(f"Generated by {APP_NAME} v{APP_VERSION}\n")
        adif_ver = extract_field_value(header, "ADIF_VER") if header else None
        if not adif_ver:
            adif_ver = "3.1.4"
        f_out.write(f"<ADIF_VER:{len(adif_ver)}>{adif_ver}\n<EOH>\n")

        for p in parts:
            rec = p.strip()
            if not rec:
                continue
            total += 1
            t_on = record_time_on_utc(rec)
            if t_on is None:
                continue

            if band_filter and band_filter != "ALL":
                band = extract_field_value(rec, "BAND")
                if not band:
                    freq = extract_field_value(rec, "FREQ")
                    try:
                        band = mhz_to_band(float(freq)) if freq else ""
                    except Exception:
                        band = ""
                if band != band_filter:
                    continue

            if start_dt <= t_on < end_dt:
                f_out.write(rec)
                if not rec.endswith("\n"):
                    f_out.write("\n")
                f_out.write("<EOR>\n")
                kept += 1
    return total, kept


# -------------------------
# GUI
# -------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.option_add("*Font", ("Yu Gothic UI", 9))

        self.lang = tk.StringVar(value=DEFAULT_LANG)

        self.in_path = tk.StringVar()
        self.out_dir = tk.StringVar(value=default_output_dir())
        self.detected_type = tk.StringVar(value="")

        self.start_str = tk.StringVar(value="2025-01-01 00:00:00")
        self.end_str   = tk.StringVar(value="2026-01-01 00:00:00")

        self.grid_digits = tk.IntVar(value=8)
        self.include_time_off = tk.BooleanVar(value=True)

        # band filter: store code
        self.band_code = tk.StringVar(value="ALL")

        self.station_call = tk.StringVar(value="")
        self.grid_locator = tk.StringVar(value="")
        self.pota = tk.StringVar(value="")
        self.sota = tk.StringVar(value="")
        self.iota = tk.StringVar(value="")
        self.wwff = tk.StringVar(value="")
        self.flag_p = tk.BooleanVar(value=False)
        self.flag_m = tk.BooleanVar(value=False)
        self.flag_mm = tk.BooleanVar(value=False)
        self.flag_am = tk.BooleanVar(value=False)

        self.preview_name = tk.StringVar(value="")

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("820x600")

        self._build_ui()
        self._detect_input_type()
        self._update_preview()

        self.lang.trace_add("write", lambda *_: self._apply_language())

    def t(self, key: str) -> str:
        return TEXT.get(self.lang.get(), TEXT["EN"]).get(key, key)

    def _build_menus(self):
        menubar = tk.Menu(self)

        langmenu = tk.Menu(menubar, tearoff=0)
        langmenu.add_radiobutton(label=TEXT["EN"]["lang_en"], variable=self.lang, value="EN")
        langmenu.add_radiobutton(label=TEXT["JA"]["lang_ja"], variable=self.lang, value="JA")
        menubar.add_cascade(label=self.t("menu_language"), menu=langmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label=self.t("about_en"), command=lambda: messagebox.showinfo(self.t("about"), _about_en()))
        helpmenu.add_command(label=self.t("about_ja"), command=lambda: messagebox.showinfo(self.t("about"), _about_ja()))
        menubar.add_cascade(label=self.t("menu_help"), menu=helpmenu)

        self.config(menu=menubar)

    def _build_ui(self):
        self._build_menus()
        pad = {"padx": 10, "pady": 6}

        # Input
        self.frm_in = tk.LabelFrame(self, text=self.t("input"))
        self.frm_in.pack(fill="x", **pad)
        self.lbl_in = tk.Label(self.frm_in, text=self.t("input_file"))
        self.lbl_in.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_in = tk.Entry(self.frm_in, textvariable=self.in_path, width=88)
        self.ent_in.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.btn_in = tk.Button(self.frm_in, text=self.t("browse"), command=self._browse_in)
        self.btn_in.grid(row=1, column=1, padx=8, pady=6)
        self.lbl_det = tk.Label(self.frm_in, textvariable=self.detected_type)
        self.lbl_det.grid(row=2, column=0, sticky="w", padx=8, pady=2)

        # Time
        self.frm_time = tk.LabelFrame(self, text=self.t("time_filter"))
        self.frm_time.pack(fill="x", **pad)
        self.lbl_start = tk.Label(self.frm_time, text=self.t("start"))
        self.lbl_start.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_start = tk.Entry(self.frm_time, textvariable=self.start_str, width=24)
        self.ent_start.grid(row=0, column=1, sticky="w", padx=8, pady=6)
        self.lbl_end = tk.Label(self.frm_time, text=self.t("end"))
        self.lbl_end.grid(row=0, column=2, sticky="w", padx=8, pady=6)
        self.ent_end = tk.Entry(self.frm_time, textvariable=self.end_str, width=24)
        self.ent_end.grid(row=0, column=3, sticky="w", padx=8, pady=6)

        # Options
        self.frm_opt = tk.LabelFrame(self, text=self.t("options"))
        self.frm_opt.pack(fill="x", **pad)

        self.lbl_gridprec = tk.Label(self.frm_opt, text=self.t("grid_precision"))
        self.lbl_gridprec.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.spn_grid = tk.Spinbox(self.frm_opt, from_=4, to=8, increment=2, textvariable=self.grid_digits, width=5)
        self.spn_grid.grid(row=0, column=1, sticky="w", padx=8, pady=6)

        self.chk_off = tk.Checkbutton(self.frm_opt, text=self.t("include_off"), variable=self.include_time_off)
        self.chk_off.grid(row=0, column=2, sticky="w", padx=8, pady=6)

        # Band filter UI (THIS WAS MISSING in your pasted code)
        self.lbl_band = tk.Label(self.frm_opt, text=self.t("band_filter"))
        self.lbl_band.grid(row=1, column=0, sticky="w", padx=8, pady=6)

        self.cmb_band = ttk.Combobox(self.frm_opt, state="readonly", width=12)
        self.cmb_band.grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.cmb_band.bind("<<ComboboxSelected>>", lambda _e: self._on_band_selected())
        self._refresh_band_choices()

        # Metadata
        self.frm_meta = tk.LabelFrame(self, text=self.t("meta"))
        self.frm_meta.pack(fill="x", **pad)

        r = 0
        self.lbl_station = tk.Label(self.frm_meta, text=self.t("station_call"))
        self.lbl_station.grid(row=r, column=0, sticky="w", padx=8, pady=4)
        self.ent_station = tk.Entry(self.frm_meta, textvariable=self.station_call, width=20)
        self.ent_station.grid(row=r, column=1, sticky="w", padx=8, pady=4)
        self.lbl_grid = tk.Label(self.frm_meta, text=self.t("grid"))
        self.lbl_grid.grid(row=r, column=2, sticky="w", padx=8, pady=4)
        self.ent_grid = tk.Entry(self.frm_meta, textvariable=self.grid_locator, width=16)
        self.ent_grid.grid(row=r, column=3, sticky="w", padx=8, pady=4)

        r += 1
        self.lbl_pota = tk.Label(self.frm_meta, text=self.t("pota"))
        self.lbl_pota.grid(row=r, column=0, sticky="w", padx=8, pady=4)
        self.ent_pota = tk.Entry(self.frm_meta, textvariable=self.pota, width=20)
        self.ent_pota.grid(row=r, column=1, sticky="w", padx=8, pady=4)
        self.lbl_sota = tk.Label(self.frm_meta, text=self.t("sota"))
        self.lbl_sota.grid(row=r, column=2, sticky="w", padx=8, pady=4)
        self.ent_sota = tk.Entry(self.frm_meta, textvariable=self.sota, width=16)
        self.ent_sota.grid(row=r, column=3, sticky="w", padx=8, pady=4)

        r += 1
        self.lbl_iota = tk.Label(self.frm_meta, text=self.t("iota"))
        self.lbl_iota.grid(row=r, column=0, sticky="w", padx=8, pady=4)
        self.ent_iota = tk.Entry(self.frm_meta, textvariable=self.iota, width=20)
        self.ent_iota.grid(row=r, column=1, sticky="w", padx=8, pady=4)
        self.lbl_wwff = tk.Label(self.frm_meta, text=self.t("wwff"))
        self.lbl_wwff.grid(row=r, column=2, sticky="w", padx=8, pady=4)
        self.ent_wwff = tk.Entry(self.frm_meta, textvariable=self.wwff, width=16)
        self.ent_wwff.grid(row=r, column=3, sticky="w", padx=8, pady=4)

        r += 1
        self.lbl_flags = tk.Label(self.frm_meta, text=self.t("flags"))
        self.lbl_flags.grid(row=r, column=0, sticky="w", padx=8, pady=4)
        self.flags_frame = tk.Frame(self.frm_meta)
        self.flags_frame.grid(row=r, column=1, columnspan=3, sticky="w", padx=8, pady=4)
        tk.Checkbutton(self.flags_frame, text="/P", variable=self.flag_p).pack(side="left")
        tk.Checkbutton(self.flags_frame, text="/M", variable=self.flag_m).pack(side="left")
        tk.Checkbutton(self.flags_frame, text="/MM", variable=self.flag_mm).pack(side="left")
        tk.Checkbutton(self.flags_frame, text="/AM", variable=self.flag_am).pack(side="left")

        # Output
        self.frm_out = tk.LabelFrame(self, text=self.t("output"))
        self.frm_out.pack(fill="x", **pad)
        self.lbl_out = tk.Label(self.frm_out, text=self.t("output_folder"))
        self.lbl_out.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_out = tk.Entry(self.frm_out, textvariable=self.out_dir, width=72)
        self.ent_out.grid(row=0, column=1, sticky="w", padx=8, pady=6)
        self.btn_out = tk.Button(self.frm_out, text=self.t("browse"), command=self._browse_out_dir)
        self.btn_out.grid(row=0, column=2, padx=8, pady=6)

        self.lbl_prev = tk.Label(self.frm_out, text=self.t("preview"))
        self.lbl_prev.grid(row=1, column=0, sticky="w", padx=8, pady=2)
        self.ent_prev = tk.Entry(self.frm_out, textvariable=self.preview_name, width=88, state="readonly")
        self.ent_prev.grid(row=1, column=1, columnspan=2, sticky="w", padx=8, pady=2)

        # Actions
        self.frm_act = tk.Frame(self)
        self.frm_act.pack(fill="x", **pad)
        self.btn_run = tk.Button(self.frm_act, text=self.t("convert"), command=self._run)
        self.btn_run.pack(side="left", padx=8, pady=10)
        self.btn_quit = tk.Button(self.frm_act, text=self.t("quit"), command=self.destroy)
        self.btn_quit.pack(side="left", padx=8, pady=10)

        # Preview updates
        for var in [self.in_path, self.out_dir, self.start_str, self.end_str, self.station_call, self.grid_locator,
                    self.pota, self.sota, self.iota, self.wwff]:
            var.trace_add("write", lambda *_: self._update_preview())
        for var in [self.flag_p, self.flag_m, self.flag_mm, self.flag_am]:
            var.trace_add("write", lambda *_: self._update_preview())

    def _refresh_band_choices(self):
        all_label = self.t("band_all")
        self._band_display_to_code = {all_label: "ALL"}
        choices = [all_label] + [b for b in BAND_CODES if b != "ALL"]
        for b in choices[1:]:
            self._band_display_to_code[b] = b
        self.cmb_band.configure(values=choices)

        code = self.band_code.get() or "ALL"
        if code == "ALL":
            self.cmb_band.set(all_label)
        else:
            self.cmb_band.set(code)

    def _on_band_selected(self):
        val = self.cmb_band.get()
        self.band_code.set(self._band_display_to_code.get(val, "ALL"))

    def _apply_language(self):
        self._build_menus()

        self.frm_in.config(text=self.t("input"))
        self.lbl_in.config(text=self.t("input_file"))
        self.btn_in.config(text=self.t("browse"))

        self.frm_time.config(text=self.t("time_filter"))
        self.lbl_start.config(text=self.t("start"))
        self.lbl_end.config(text=self.t("end"))

        self.frm_opt.config(text=self.t("options"))
        self.lbl_gridprec.config(text=self.t("grid_precision"))
        self.chk_off.config(text=self.t("include_off"))
        self.lbl_band.config(text=self.t("band_filter"))
        self._refresh_band_choices()

        self.frm_meta.config(text=self.t("meta"))
        self.lbl_station.config(text=self.t("station_call"))
        self.lbl_grid.config(text=self.t("grid"))
        self.lbl_pota.config(text=self.t("pota"))
        self.lbl_sota.config(text=self.t("sota"))
        self.lbl_iota.config(text=self.t("iota"))
        self.lbl_wwff.config(text=self.t("wwff"))
        self.lbl_flags.config(text=self.t("flags"))

        self.frm_out.config(text=self.t("output"))
        self.lbl_out.config(text=self.t("output_folder"))
        self.btn_out.config(text=self.t("browse"))
        self.lbl_prev.config(text=self.t("preview"))

        self.btn_run.config(text=self.t("convert"))
        self.btn_quit.config(text=self.t("quit"))

        self._detect_input_type()
        self._update_preview()

    def _browse_in(self):
        p = filedialog.askopenfilename(
            title=self.t("select_input_title"),
            filetypes=[("WSJT logs", "*.log *.adi *.txt *.csv"), ("All files", "*.*")]
        )
        if p:
            self.in_path.set(p)
            self._detect_input_type()
            self._update_preview()

    def _browse_out_dir(self):
        p = filedialog.askdirectory(title=self.t("select_out_title"))
        if p:
            self.out_dir.set(p)
            self._update_preview()

    def _detect_input_type(self):
        path = self.in_path.get().strip()
        if not path or not os.path.isfile(path):
            self.detected_type.set(self.t("no_file"))
            return
        if detect_adif(path) and not detect_wsjtx_csv(path):
            self.detected_type.set(self.t("det_adif"))
        elif detect_wsjtx_csv(path):
            self.detected_type.set(self.t("det_log"))
        else:
            self.detected_type.set(self.t("det_unknown"))

    def _update_preview(self):
        try:
            start_dt = parse_utc_datetime(self.start_str.get())
            end_dt = parse_utc_datetime(self.end_str.get())
            if end_dt <= start_dt:
                self.preview_name.set(self.t("preview_invalid_range"))
                return
            flags = []
            if self.flag_p.get(): flags.append("/P")
            if self.flag_m.get(): flags.append("/M")
            if self.flag_mm.get(): flags.append("/MM")
            if self.flag_am.get(): flags.append("/AM")
            name = build_output_filename(
                station_call=self.station_call.get(),
                start_dt=start_dt,
                end_dt=end_dt,
                grid=self.grid_locator.get(),
                portable_flags=flags,
                pota=self.pota.get(),
                sota=self.sota.get(),
                iota=self.iota.get(),
                wwff=self.wwff.get(),
                suffix=".adi"
            )
            self.preview_name.set(name)
        except Exception:
            self.preview_name.set(self.t("preview_hint"))

    def _run(self):
        in_path = self.in_path.get().strip()
        if not in_path or not os.path.isfile(in_path):
            messagebox.showerror(self.t("err_missing_input_title"), self.t("err_missing_input"))
            return

        try:
            start_dt = parse_utc_datetime(self.start_str.get())
            end_dt = parse_utc_datetime(self.end_str.get())
            if end_dt <= start_dt:
                raise ValueError("End must be after Start.")
        except Exception as e:
            messagebox.showerror(self.t("err_invalid_time_title"), str(e))
            return

        out_dir = self.out_dir.get().strip()
        if not out_dir or not os.path.isdir(out_dir):
            messagebox.showerror(self.t("err_missing_out_title"), self.t("err_missing_out"))
            return

        flags = []
        if self.flag_p.get(): flags.append("/P")
        if self.flag_m.get(): flags.append("/M")
        if self.flag_mm.get(): flags.append("/MM")
        if self.flag_am.get(): flags.append("/AM")

        out_name = build_output_filename(
            station_call=self.station_call.get(),
            start_dt=start_dt,
            end_dt=end_dt,
            grid=self.grid_locator.get(),
            portable_flags=flags,
            pota=self.pota.get(),
            sota=self.sota.get(),
            iota=self.iota.get(),
            wwff=self.wwff.get(),
            suffix=".adi",
        )
        out_path = os.path.join(out_dir, out_name)

        band_filter = self.band_code.get() or "ALL"

        try:
            is_adif = detect_adif(in_path) and not detect_wsjtx_csv(in_path)
            if is_adif:
                total, kept = split_adif_by_datetime(in_path, out_path, start_dt, end_dt, band_filter=band_filter)
                msg = self.t("done_adif").format(total=total, kept=kept, path=out_path)
                messagebox.showinfo(self.t("done_title"), msg)
            else:
                total, kept = convert_wsjtx_log_to_adif(
                    in_path, out_path, start_dt, end_dt,
                    grid_digits=int(self.grid_digits.get()),
                    include_time_off=bool(self.include_time_off.get()),
                    band_filter=band_filter
                )
                msg = self.t("done_log").format(total=total, kept=kept, path=out_path)
                messagebox.showinfo(self.t("done_title"), msg)
        except Exception as e:
            messagebox.showerror(self.t("failed_title"), f"{e}")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

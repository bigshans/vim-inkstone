#!/usr/bin/env python3
"""Regenerate the palettes in autoload/inkstone.vim from the upstream VS Code theme.

The highlight rules in autoload/inkstone.vim are hand-maintained; only the data
block between the `{{{ palettes` / `}}} palettes` markers is rewritten.

Usage:
    # unpack the extension first
    unzip Konata9.inkstone-0.3.4.vsix -d /tmp/inkstone
    python3 tools/build.py --themes /tmp/inkstone/extension/themes

    # or point it at a checkout of github.com/Konata9/inkstone
    python3 tools/build.py --themes packages/vscode/themes

Requires only the Python 3 standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

VARIANTS = [
    ("xuanmo", "玄墨 Xuanmo"),
    ("xuanmo-dimmed", "玄墨 Dimmed"),
    ("canghai", "沧海 Canghai"),
    ("xuanzhi", "宣纸 Xuanzhi"),
    ("xuanzhi-dimmed", "宣纸 Dimmed"),
    ("qingci", "青瓷 Qingci"),
]

BEGIN = "{{{ palettes"
END = "}}} palettes"

# ---------------------------------------------------------------- colour helpers


def hex6(value: str) -> str:
    """'#AABBCC' / '#AABBCCDD' -> 'aabbcc' (alpha dropped)."""
    return value.lstrip("#")[:6].lower()


def rgb(value: str) -> list[int]:
    value = value.lstrip("#")
    return [int(value[i : i + 2], 16) for i in (0, 2, 4)]


def blend(over: str, under: str) -> str:
    """Composite '#rrggbb[aa]' over an opaque '#rrggbb'."""
    over = over.lstrip("#")
    src, dst = rgb(over[:6]), rgb(under)
    alpha = int(over[7:9], 16) / 255 if len(over) >= 8 else 1.0
    out = (round(s * alpha + d * (1 - alpha)) for s, d in zip(src, dst))
    return "%02x%02x%02x" % tuple(out)


# ---------------------------------------------------------------- extraction


def token(theme: dict, name: str) -> str:
    for entry in theme["tokenColors"]:
        if entry["name"] == name:
            return hex6(entry["settings"]["foreground"])
    raise KeyError(f"token {name!r} not found")


def extract(path: str) -> dict:
    theme = json.load(open(path, encoding="utf-8"))
    c = theme["colors"]
    bg, fg = hex6(c["editor.background"]), hex6(c["editor.foreground"])

    p = {
        "bg": bg,
        "fg": fg,
        "cursor": hex6(c["editorCursor.foreground"]),
        "sel": hex6(c["editor.selectionBackground"]),
        "sel_nc": hex6(c.get("editor.inactiveSelectionBackground", c["editor.selectionBackground"])),
        "lineno": hex6(c["editorLineNumber.foreground"]),
        "lineno_act": hex6(c["editorLineNumber.activeForeground"]),
        "linehl": blend(c["editor.lineHighlightBackground"], bg),
        "gutter": hex6(c.get("editorGutter.background", bg)),
        "bg_alt": hex6(c["statusBar.background"]),
        "bg_alt2": hex6(c["sideBar.background"]),
        "bg_hard": hex6(c.get("activityBar.background", c["statusBar.background"])),
        "widget": hex6(c.get("editorWidget.background", c["editorHoverWidget.background"])),
        "input": hex6(c.get("input.background", c.get("editorHoverWidget.background", bg))),
        "border": hex6(
            c.get("widget.border", c.get("contrastBorder", c["editorIndentGuide.activeBackground1"]))
        ),
        "comment": token(theme, "Comments"),
        "keyword": token(theme, "Keywords and control flow"),
        "func": token(theme, "Functions and methods"),
        "method": token(theme, "Methods"),
        "type": token(theme, "Types, classes and namespaces"),
        "str": token(theme, "Strings"),
        "num": token(theme, "Numbers, booleans and constants"),
        "var": token(theme, "Variables"),
        "param": token(theme, "Parameters"),
        "prop": token(theme, "Properties and keys"),
        "tag": token(theme, "Tags"),
        "attr": token(theme, "Attributes"),
        "deco": token(theme, "Decorators and macros"),
        "regex": token(theme, "Regular expressions"),
        "escape": token(theme, "Escape characters"),
        "op": token(theme, "Operators"),
        "punct": token(theme, "Punctuation and brackets"),
        "invalid": token(theme, "Invalid"),
        "deprecated": token(theme, "Deprecated"),
        "ins": token(theme, "Inserted"),
        "del": token(theme, "Deleted"),
        "chg": token(theme, "Changed"),
        "diffhdr": token(theme, "Diff header"),
        "err": hex6(c["editorError.foreground"]),
        "warn": hex6(c["editorWarning.foreground"]),
        "info": hex6(c["editorInfo.foreground"]),
        "whitespace": hex6(c["editorWhitespace.foreground"]),
        "guide": hex6(c["editorIndentGuide.background1"]),
        "guide_act": hex6(c["editorIndentGuide.activeBackground1"]),
        "ruler": hex6(c["editorRuler.foreground"]),
        "findbg": blend(c["editor.findMatchBackground"], bg),
        "findhl": blend(c["editor.findMatchHighlightBackground"], bg),
        "findbd": hex6(c["editor.findMatchBorder"]),
        "list_sel": hex6(c.get("list.activeSelectionBackground", c["editor.lineHighlightBackground"])),
        "list_hover": hex6(c.get("list.hoverBackground", bg)),
        "badge_fg": hex6(c.get("badge.foreground", bg)),
        "match": blend(c["editorBracketMatch.background"], bg)
        if "editorBracketMatch.background" in c
        else bg,
    }

    p["br"] = [
        hex6(c.get(f"editorBracketHighlight.foreground{i}", c["editorIndentGuide.activeBackground1"]))
        for i in range(1, 7)
    ]

    order = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
    p["ansi"] = [hex6(c[f"terminal.ansi{n}"]) for n in order] + [
        hex6(c[f"terminal.ansiBright{n}"]) for n in order
    ]

    r, g, b = rgb(bg)
    p["light"] = int(0.2126 * r + 0.7152 * g + 0.0722 * b > 140)
    return p


# ---------------------------------------------------------------- emission

KEY_ORDER = """bg fg cursor sel sel_nc lineno lineno_act linehl gutter bg_alt bg_alt2
bg_hard widget input border comment keyword func method type str num var param prop tag
attr deco regex escape op punct invalid deprecated ins del chg diffhdr err warn info
whitespace guide guide_act ruler findbg findhl findbd list_sel list_hover badge_fg
match""".split()


def vim_dict(name: str, p: dict) -> str:
    lines = [f"      \\ '{name}': {{"]
    for key in KEY_ORDER:
        lines.append(f"      \\ '{key}': '#{p[key]}',")
    lines.append("      \\ 'br': [" + ", ".join(f"'#{x}'" for x in p["br"]) + "],")
    lines.append("      \\ 'ansi': [" + ", ".join(f"'#{x}'" for x in p["ansi"]) + "],")
    lines.append(f"      \\ 'light': {p['light']},")
    lines.append("      \\ }")
    return "\n".join(lines)


def block(palettes: dict[str, dict]) -> str:
    body = ",\n".join(vim_dict(name, palettes[name]) for name, _ in VARIANTS)
    names = "\n".join(f"      \\ '{name}': '{label}'," for name, label in VARIANTS)
    return (
        f'" {BEGIN} — generated by tools/build.py, do not edit by hand\n'
        f"let s:palettes = {{\n{body}\n      \\ }}\n\n"
        f"let s:names = {{\n{names}\n      \\ }}\n"
        f'" {END}\n'
    )


def main() -> int:
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--themes",
        default=os.path.join(here, "tools", "themes"),
        help="directory holding <variant>-color-theme.json (default: tools/themes)",
    )
    ap.add_argument("--file", default=os.path.join(here, "autoload", "inkstone.vim"))
    args = ap.parse_args()

    palettes = {}
    for name, _ in VARIANTS:
        path = os.path.join(args.themes, f"{name}-color-theme.json")
        if not os.path.isfile(path):
            sys.exit(f"missing theme file: {path}")
        palettes[name] = extract(path)

    src = open(args.file, encoding="utf-8").read()
    if BEGIN not in src or END not in src:
        sys.exit(f"palette markers not found in {args.file}")
    start = src.rfind("\n", 0, src.find(BEGIN)) + 1
    end = src.find("\n", src.find(END)) + 1

    open(args.file, "w", encoding="utf-8").write(src[:start] + block(palettes) + src[end:])
    print(f"updated {args.file} ({len(palettes)} variants)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

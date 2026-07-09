#!/usr/bin/env python3
# Barazo docs house-style linter.
#
# Deterministic checks for the Barazo writing style: the mechanical things a
# style pass should never miss (dashes, curly quotes, overused vocabulary,
# teaser headers, and so on). The rules mirror the internal Barazo/Singi Labs
# style guide and are maintained from that source. Regenerate rather than
# hand-editing the rule logic here.
"""voice-lint: deterministic house-style checks for Barazo docs.

Runs the mechanical style checks with zero misses, so a human editing pass can
spend its attention on judgment calls (rhythm, phrasing, not restating the
obvious).

Usage:
  python3 voice-lint.py <file> [--voice personal|product] [--fix] [--json]
  cat draft.md | python3 voice-lint.py - [--voice product]

Exit codes: 0 = no errors (warnings allowed), 1 = errors found, 2 = usage error.

Severities:
  ERROR = hard ban, always wrong in this style. Fix it.
  WARN  = strong smell, but has legitimate uses. A human decides.

--fix applies only the unambiguous rewrites (curly quotes, unicode arrows,
"the AT Protocol"); everything else needs a human choice (an em dash can become
a period, comma, colon, or parentheses - that's a judgment call).
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------- helpers

URL_RE = re.compile(r"https?://\S+|www\.\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_BOLD_RE = re.compile(r"^\s*[-*+]\s+\*\*[^*]+?(?::\*\*|\*\*\s*:)")
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)


def mask(line: str) -> str:
    """Blank out URLs, inline code, and HTML entities so they never match rules."""
    line = URL_RE.sub(lambda m: " " * len(m.group()), line)
    line = INLINE_CODE_RE.sub(lambda m: " " * len(m.group()), line)
    line = re.sub(r"&#?\w{1,10};", lambda m: " " * len(m.group()), line)
    return line


# ---------------------------------------------------------------- rules
# Each rule: (id, severity, compiled regex, message). Regexes run on the
# masked line. Case-insensitive unless noted.

def w(pat):  # word-boundary, case-insensitive
    return re.compile(r"\b" + pat + r"\b", re.IGNORECASE)


ERROR_RULES = [
    ("em-dash", re.compile("—"),
     "em dash; replace with a period, comma, colon, parentheses, or (sparingly) ' - '"),
    ("double-hyphen", re.compile(r"(?<=[\w\s])--(?=[\w\s])"),
     "double hyphen used as a dash; same replacement as an em dash"),
    ("curly-quote", re.compile("[“”‘’]"),
     "curly quote; use straight quotes (auto-fixable)"),
    ("unicode-arrow", re.compile("[→←⇒➔➜]"),
     "unicode arrow in prose; use '->' or words like 'leads to' (auto-fixable)"),
    ("the-at-protocol",
     re.compile(r"\bthe\s+AT\s+Protocol\b(?!\s+(?:ecosystem|community|network|team|space|stack|world|app|apps|developers?|spec|docs?))"),
     "\"the AT Protocol\" -> \"AT Protocol\" (proper noun, no article; auto-fixable)"),
    ("lol", w(r"lol"), "'lol' is off-style; use 'haha' or an emoji"),
    ("i-believe", w(r"I\s+believe"), "prefer 'I think' over 'I believe'"),
    ("perhaps", w(r"perhaps"), "'perhaps' reads formal; prefer 'maybe'"),
    ("formal-transition",
     w(r"(?:furthermore|moreover|nevertheless|consequently|firstly|secondly|thirdly)"),
     "formal transition word; use 'but', 'so', 'and', or restructure"),
    ("however-initial", re.compile(r"(?:^|[.!?]\s+)However\b[, ]"),
     "sentence-initial 'However' reads formal; use 'But' or restructure"),
    ("signposted-conclusion",
     re.compile(r"\b(?:in\s+conclusion|to\s+summariz|in\s+summary|in\s+closing|to\s+sum\s+up|wrapping\s+up)", re.IGNORECASE),
     "signposted conclusion; let the writing end without an announcement"),
    ("honesty-qualifier",
     re.compile(r"\b(?:i'?ll\s+be\s+honest|to\s+be\s+(?:honest|frank|fair,?\s+i|transparent)|let\s+me\s+be\s+(?:honest|straight|frank)|not\s+gonna\s+lie|full\s+transparency|full\s+disclosure|real\s+talk|the\s+honest\s+truth|trust\s+me\b|believe\s+me\b)", re.IGNORECASE),
     "honesty announcement; state the point, the honesty is implicit"),
    ("vocab-hard",
     w(r"(?:delve|delves|delving|tapestry|testament|underscores?|utiliz\w+|leverag\w+|robust|seamless\w*|elevate[sd]?|foster(?:s|ing|ed)?|garner\w*|pivotal|embark\w*|realm|meticulous\w*|groundbreaking|ground-breaking|game.chang\w+|cutting.edge|revolutioniz\w+|enigma|indelible|bustling|nestled)"),
     "hard-banned corporate/overused word (style guide avoid list)"),
    ("phrase-hard",
     re.compile(r"\b(?:here'?s\s+the\s+thing|let\s+me\s+tell\s+you|i\s+want\s+to\s+share|at\s+the\s+end\s+of\s+the\s+day|i\s+keep\s+coming\s+back\s+to|what\s+struck\s+me|what\s+caught\s+my\s+attention|what\s+impressed\s+me\s+most|in\s+today'?s\s+digital|when\s+it\s+comes\s+to|in\s+the\s+(?:world|realm)\s+of|unlock\s+the\s+secrets|unveil\s+the\s+secrets|it'?s\s+worth\s+noting|it'?s\s+important\s+to\s+note|simply\s+put|to\s+put\s+it\s+simply|at\s+its\s+core|in\s+a\s+sea\s+of|is\s+spot\s+on|ever-?evolving|everchanging|deep\s+dive|dive\s+into|all\s+you\s+need\s+to\s+know|what\s+you\s+need\s+to\s+know)", re.IGNORECASE),
     "hard-banned phrase (style guide avoid list)"),
    ("collab-artifact",
     re.compile(r"\b(?:i\s+hope\s+this\s+helps|let\s+me\s+know\s+if\s+you'?d\s+like\s+me\s+to|would\s+you\s+like\s+me\s+to|as\s+an\s+ai\b|certainly!|of\s+course!|great\s+question|you'?re\s+absolutely\s+right)", re.IGNORECASE),
     "leftover conversational filler; cut it"),
    ("teaser-header", None,  # handled specially on heading lines
     "teaser header; name the content or state the takeaway"),
]

ERROR_RULES += [
    ("not-just-pivot",
     re.compile(r"\b(?:it|this|that|he|she|they|i)\s*(?:'s|is|was|are|were)?\s*n[o']t\s+just\s+(?:about\s+)?\w[^.;:!?]{0,60}[.;,]\s*(?:it|this|that)\s*(?:'s|is|was)\b", re.IGNORECASE),
     "'not just X, it's Y' pivot; overused (a trailing 'A, not just B' without the pivot is fine)"),
    ("announced-gotcha",
     re.compile(r"\b(?:(?:the\s+)?(?:one\s+)?thing\s+that(?:'?ll|'?s\s+going\s+to|\s+will)\s+(?:bite|get|trip)|(?:here'?s\s+)?what(?:'?ll|\s+will)\s+(?:bite|get|trip)\s+you)", re.IGNORECASE),
     "announced-gotcha preamble ('the one thing that'll bite'); just state the caveat"),
]

WARN_RULES = [
    ("en-dash", re.compile("–"),
     "en dash; use ' - ' (spaced hyphen) for ranges, sparingly"),
    ("stacked-punct", re.compile(r"[!?]{2,}"),
     "stacked punctuation (!!/?!); rare in this style"),
    ("not-x-its-y",
     re.compile(r"\b(?:isn'?t|not)\s+(?:a\s+|an\s+|the\s+)?\w+[^.;:!?]{0,40}\.\s*It'?s\s+", re.IGNORECASE),
     "'isn't X. It's Y' contrast: state Y directly, drop the negation setup"),
    ("vocab-soft",
     w(r"(?:crucial|essential|vital|ensure[sd]?|ensuring|significant\w*|notably|arguably|ultimately|subsequently|additionally|specifically|importantly|effectively|effortlessly|showcas\w+|encompass\w+|encapsulat\w+|harness\w+|daunting|keen|amongst|holistic\w*|landscape|journey|vibrant|enhanc\w+|empower\w+|navigat\w+|complexit\w+|streamlin\w+|intricate|intricacies|interplay)"),
     "overused word (avoid list); fine occasionally, a cluster of them is a tell"),
    ("weasel-attribution",
     re.compile(r"\b(?:industry\s+reports?|experts?\s+(?:argue|believe|say)|observers\s+have|some\s+critics\s+argue|studies\s+show\b)", re.IGNORECASE),
     "vague attribution; name the actual source or cut"),
    ("rhetorical-fragment",
     re.compile(r"\b(?:the\s+result\?|the\s+worst\s+part\?|the\s+best\s+part\?|think\s+about\s+it:|here'?s\s+what\s+i\s+mean|and\s+that'?s\s+okay\.)", re.IGNORECASE),
     "self-posed rhetorical question / manufactured suspense"),
    ("what-opener",
     re.compile(r"(?:^|[.!?]\s+)What\s+(?:this\s+means|makes\s+this|i\s+(?:did|built|chose|learned))\s", re.IGNORECASE),
     "'What X is/did...' self-narration opener; state the content directly"),
    ("semicolon",
     re.compile(r"\w;(?=\s)"),
     "semicolon: rarely used in this style; prefer a colon, comma, or period"),
    ("invented-interlocutor",
     re.compile(r"[\"“][^\"”]{2,80}[?.][\"”]\s+(?:Fair(?:\s+enough)?|True|Sure|Valid|Yes)\b"),
     "staged objection-and-concede dialogue; state the point directly or ask the reader a real question"),
    ("attraction-meta",
     re.compile(r"\b(?:what\s+(?:draws|attracts|attracted|pulls)\s+me|the\s+pull\s+(?:here|for\s+me)\s+is|the\s+part\s+of\s+this\s+(?:role|job)\s+i'?d\s+enjoy)", re.IGNORECASE),
     "narrated attraction/enjoyment framing; assert the content directly"),
    ("mixed-number-style",
     re.compile(r"\b(?:één|een|one)\s+(?:van|of)\s+(?:de\s+|the\s+)?\d+\b|\b\d+\s+(?:van|of)\s+(?:de\s+|the\s+)?(?:twee|drie|vier|vijf|zes|zeven|acht|negen|tien|two|three|four|five|six|seven|eight|nine|ten)\b", re.IGNORECASE),
     "mixed numeral style ('one of 7'): use digits for both ('1 of 7') or words for both ('one of seven')"),
    ("worth-noting-lead",
     re.compile(r"\b(?:worth\s+(?:pinning|flagging|noting|remembering)|the\s+key\s+point|the\s+important\s+bit|one\s+thing\s+to\s+keep\s+in\s+mind|here'?s\s+what\s+matters)", re.IGNORECASE),
     "reader-value editorializing; name the content instead"),
    ("bold-header-bullet", None,  # handled specially
     "bullet with a bold inline header; weave into prose or use a plain list"),
    ("title-case-heading", None,  # handled specially
     "Title Case heading; use sentence case"),
    ("emoji-decoration", None,  # handled specially
     "emoji decorating a heading/bullet; in-sentence emoji is fine"),
]

TEASER_HEADERS = re.compile(
    r"^(?:why\s+(?:this|that|it)\s+matters|here'?s\s+where|the\s+(?:honest|interesting|best|important)\s+part|what\s+you\s+should\s+care\s+about|the\s+big\s+takeaway|the\s+part\s+you|real\s+talk|full\s+transparency|the\s+honest\s+truth)\b",
    re.IGNORECASE,
)

# Published-docs extras: casual markers that should not appear in docs or
# marketing copy (they belong in casual writing only).
PRODUCT_ERROR_RULES = [
    ("product-thx", w(r"thx"), "'thx' is casual-only; docs use 'thanks'"),
    ("product-profanity", w(r"(?:fuck\w*|shit\w*|damn\w*|crap)"),
     "profanity is casual-only"),
    ("product-emoticon", re.compile(r"(?:^|\s)[:;]-?[)D(pP](?=\s|$)"),
     "text emoticon; casual-only"),
]
PRODUCT_WARN_RULES = [
    ("product-ellipsis", re.compile(r"\.\.\.|…"),
     "ellipsis reads casual; keep docs cleaner"),
    ("product-emoji", EMOJI_RE, "emoji in docs; use only if genuinely functional"),
    ("product-dutchism", w(r"(?:automagic\w*|super\s+\w+)"),
     "informal intensifier; casual-only"),
]

# --fix: unambiguous replacements only.
FIXES = [
    (re.compile("[“”]"), '"'),
    (re.compile("[‘’]"), "'"),
    (re.compile("→"), "->"),
    (re.compile("←"), "<-"),
    (re.compile(r"\bthe\s+(AT\s+Protocol)\b(?!\s+(?:ecosystem|community|network|team|space|stack|world|app|apps|developers?|spec|docs?))"), r"\1"),
    (re.compile(r"\bThe\s+(AT\s+Protocol)\b(?!\s+(?:ecosystem|community|network|team|space|stack|world|app|apps|developers?|spec|docs?))"), r"\1"),
]


def is_title_case(heading_text: str) -> bool:
    words = [x for x in re.findall(r"[A-Za-z][A-Za-z'-]*", heading_text)]
    if len(words) < 4:
        return False
    content = [x for x in words if len(x) > 3]
    if len(content) < 3:
        return False
    capped = sum(1 for x in content if x[0].isupper())
    # all-caps headings and ones with few capitals pass
    if all(x.isupper() for x in content):
        return False
    return capped / len(content) >= 0.8


def lint(text: str, voice: str):
    findings = []
    in_code = False
    in_frontmatter = False
    lines = text.splitlines()

    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if i == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if "[ cut here ]" in stripped:
            break  # boilerplate below the scissor line is verbatim, exempt
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue

        line = mask(raw)

        def add(sev, rid, msg, match=None):
            snippet = (match.group(0).strip() if match else stripped)[:60]
            findings.append({
                "line": i, "severity": sev, "rule": rid,
                "match": snippet, "message": msg,
            })

        for rid, rx, msg in ERROR_RULES:
            if rx is None:
                continue
            for m in rx.finditer(line):
                add("ERROR", rid, msg, m)
        for rid, rx, msg in WARN_RULES:
            if rx is None:
                continue
            for m in rx.finditer(line):
                add("WARN", rid, msg, m)

        h = HEADING_RE.match(raw)
        if h:
            htext = h.group(2).strip()
            if TEASER_HEADERS.match(htext):
                add("ERROR", "teaser-header",
                    "teaser header; name the content or state the takeaway")
            if is_title_case(htext):
                add("WARN", "title-case-heading",
                    "Title Case heading; use sentence case")
            if EMOJI_RE.search(htext):
                add("WARN", "emoji-decoration",
                    "emoji decorating a heading")
        if BULLET_BOLD_RE.match(raw):
            add("WARN", "bold-header-bullet",
                "bullet with a bold inline header")
        if re.match(r"^\s*[-*+]\s*" + EMOJI_RE.pattern, raw):
            add("WARN", "emoji-decoration",
                "emoji decorating a bullet")

        if voice == "product":
            for rid, rx, msg in PRODUCT_ERROR_RULES:
                for m in rx.finditer(line):
                    add("ERROR", rid, msg, m)
            for rid, rx, msg in PRODUCT_WARN_RULES:
                for m in rx.finditer(line):
                    add("WARN", rid, msg, m)

    # Document-level check: product name is "Sifa ID"; first mention must be
    # the full name, shorthand "Sifa" only after that. Case-sensitive so repo
    # slugs (sifa-api, sifa.id) never match; URLs/code are masked anyway.
    in_code = in_frontmatter = False
    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if i == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.search(r"\bSifa\b", mask(raw))
        if m:
            if not re.match(r"Sifa\s+ID\b", mask(raw)[m.start():]):
                findings.append({
                    "line": i, "severity": "WARN", "rule": "sifa-id-first-mention",
                    "match": mask(raw)[m.start():m.start() + 20].strip(),
                    "message": "first mention should be the full product name 'Sifa ID'; shorthand 'Sifa' is for subsequent mentions",
                })
            break

    return findings


def apply_fixes(text: str) -> str:
    out_lines = []
    in_code = False
    in_frontmatter = False
    footer = False
    for i, raw in enumerate(text.splitlines(keepends=False), 1):
        stripped = raw.strip()
        if footer or "[ cut here ]" in stripped:
            footer = True
            out_lines.append(raw)
            continue
        if i == 1 and stripped == "---":
            in_frontmatter = True
            out_lines.append(raw)
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            out_lines.append(raw)
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            out_lines.append(raw)
            continue
        if in_code:
            out_lines.append(raw)
            continue
        fixed = raw
        for rx, repl in FIXES:
            fixed = rx.sub(repl, fixed)
        out_lines.append(fixed)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def main():
    ap = argparse.ArgumentParser(description="Deterministic house-style linter for Barazo docs")
    ap.add_argument("path", help="file to lint, or '-' for stdin")
    ap.add_argument("--voice", choices=["personal", "product"], default="personal")
    ap.add_argument("--fix", action="store_true",
                    help="apply safe auto-fixes in place (curly quotes, arrows, 'the AT Protocol')")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    if args.path == "-":
        if args.fix:
            sys.exit("ERROR: --fix needs a file path, not stdin")
        text = sys.stdin.read()
        name = "<stdin>"
    else:
        p = Path(args.path)
        if not p.is_file():
            sys.exit(f"ERROR: not a file: {args.path}")
        text = p.read_text(encoding="utf-8")
        name = str(p)

    if args.fix:
        fixed = apply_fixes(text)
        if fixed != text:
            Path(args.path).write_text(fixed, encoding="utf-8")
        text = fixed

    findings = lint(text, args.voice)
    errors = [f for f in findings if f["severity"] == "ERROR"]
    warns = [f for f in findings if f["severity"] == "WARN"]

    if args.json:
        print(json.dumps({"file": name, "errors": len(errors), "warnings": len(warns),
                          "findings": findings}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f'{name}:{f["line"]}: [{f["severity"]}] {f["rule"]}: "{f["match"]}" - {f["message"]}')
        fixed_note = " (after --fix)" if args.fix else ""
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s){fixed_note}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generates the animated SVGs used by the profile README (assets/*.svg).

Run: python3 tools/build_assets.py
Every animation is SMIL inside the SVG, so it plays in GitHub's <img> rendering without JavaScript.
Colors follow Xcode's "Default (Dark)" editor theme.
"""
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# Xcode "Default (Dark)"
EDITOR, WINDOW, CHROME, BORDER = "#1F1F24", "#161619", "#2B2B30", "#3A3A40"
CURRENT_LINE, LINE_NO = "#23252B", "#747478"
PLAIN = "#DFDFE0"
KEYWORD = "#FC5FA3"
COMMENT = "#6C7986"
STRING = "#FC6A5D"
NUMBER = "#D0BF69"
TYPE_DECL = "#5DD8FF"
OTHER_DECL = "#41A1C0"
PROJECT_TYPE = "#9EF1DD"
PROJECT_FUNC = "#67B7A4"
OTHER_TYPE = "#D0A8FF"
PREPROC = "#FD8F3F"
URL = "#5482FF"
SUCCESS = "#32D74B"
SWIFT = "#F05138"

STYLE = f"""<style>
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
</style>"""


def anim(attr, frames, dur, tag="animate", extra=""):
    """Looping animation from (keyTime, value) pairs; first time must be 0 and last 1."""
    kts = ";".join(f"{t:g}" for t, _ in frames)
    vals = ";".join(str(v) for _, v in frames)
    return (f'<{tag} attributeName="{attr}" dur="{dur}s" repeatCount="indefinite" '
            f'keyTimes="{kts}" values="{vals}"{extra}/>')


def once(attr, frm, to, begin, dur, tag="animate", extra=""):
    """Plays once on load and keeps the final value."""
    return (f'<{tag} attributeName="{attr}" from="{frm}" to="{to}" begin="{begin}s" '
            f'dur="{dur}s" fill="freeze"{extra}/>')


def svg(w, h, title, desc, body, view=None):
    view = view or (0, 0, w, h)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{view[2]}" height="{view[3]}" '
            f'viewBox="{" ".join(map(str, view))}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{esc(title)}</title>\n'
            f'<desc id="d">{esc(desc)}</desc>\n{STYLE}\n{body}\n</svg>\n')


def card_bg(w, h, fill=EDITOR):
    return (f'<rect width="{w}" height="{h}" rx="16" fill="{fill}"/>'
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="15.5" fill="none" stroke="{BORDER}"/>')


def title_bar(x, y, w, title, r=16, h=40):
    """Xcode window chrome: traffic lights and a centered title."""
    return (f'<path d="M{x} {y + h}V{y + r}a{r} {r} 0 0 1 {r}-{r}H{x + w - r}a{r} {r} 0 0 1 {r} {r}V{y + h}Z" fill="{CHROME}"/>'
            f'<path d="M{x} {y + h}H{x + w}" stroke="#000" stroke-opacity="0.5"/>'
            f'<circle cx="{x + 22}" cy="{y + h / 2}" r="6" fill="#ff5f57"/>'
            f'<circle cx="{x + 42}" cy="{y + h / 2}" r="6" fill="#febc2e"/>'
            f'<circle cx="{x + 62}" cy="{y + h / 2}" r="6" fill="#28c840"/>'
            + (f'<text x="{x + w / 2}" y="{y + h / 2 + 4.5}" text-anchor="middle" class="sans" font-size="12.5" '
               f'fill="{COMMENT}">{title}</text>' if title else ""))


def tspans(parts):
    out = []
    for p in parts:
        text, color = p[0], p[1]
        weight = f' font-weight="{p[2]}"' if len(p) > 2 else ""
        out.append(f'<tspan fill="{color}"{weight}>{esc(text)}</tspan>')
    return "".join(out)


# ---------------------------------------------------------------- hero ----

def hero(done=0.50, crop=None):
    """crop=(x, y, w, h) exports just that region, e.g. the phone for the website."""
    W, H, D = 960, 460, 16
    step = lambda verb, rest: [("▸ ", PREPROC), (f"{verb:<10}", KEYWORD, "700"), (rest, PLAIN)]
    lines = [
        [("$ ", COMMENT), ("xcodebuild ", KEYWORD, "700"), ("-scheme ", OTHER_DECL), ('"Mohamed Haggag" ', STRING),
         ("-configuration ", OTHER_DECL), ("Senior", PROJECT_TYPE)],
        step("Compiling", "Swift 6 · SwiftUI · UIKit · Combine · async/await"),
        step("Linking", "Clean Architecture · MVVM · VIP · VIPER · SPM"),
        step("Securing", "E2EE (CryptoKit) · Keychain · SSL pinning"),
        step("Wiring", "Apple Pay · Mada · Nafath · SignalR · WebRTC"),
        step("Testing", "XCTest · XCUITest · 8+ years in production"),
        step("Shipping", "Fastlane → App Store · KSA · Iraq · Egypt"),
        [("** BUILD SUCCEEDED ** ", SUCCESS, "700"), ("Senior iOS Developer, leading 4 engineers ", PLAIN)],
    ]
    fade = (0.93, 0.97)  # everything resets here

    clips, texts = [], []
    for i, parts in enumerate(lines):
        y = 194 + i * 30
        s = 0.03 + 0.06 * i
        clips.append(f'<clipPath id="c{i}"><rect x="40" y="{y - 16}" height="22" width="0">'
                     f'{anim("width", [(0, 0), (s, 0), (s + 0.05, 580), (1, 580)], D)}</rect></clipPath>')
        cursor = ""
        if i == len(lines) - 1:
            cursor = (f'<tspan fill="{PLAIN}">▋<animate attributeName="fill-opacity" values="1;0;1" '
                      f'dur="1s" repeatCount="indefinite"/></tspan>')
        texts.append(f'<text x="44" y="{y}" class="mono" font-size="14" xml:space="preserve" '
                     f'clip-path="url(#c{i})">{tspans(parts)}{cursor}</text>')

    # phone geometry
    px, py, pw, ph = 698, 12, 236, 436
    cx = px + pw / 2
    notes = [
        ("A", "url(#ic0)", "Aseel", "24 App Store releases", "4.6★ · 7.4K ratings"),
        ("S", "url(#ic1)", "Super App", "E2EE chat · VoIP calls", "Wallet · gov e-services"),
        ("B", "url(#ic2)", "Beetleware", "Leading 4 iOS engineers", "10+ apps in production"),
    ]
    note_svgs = []
    for k, (letter, fill, name, l1, l2) in enumerate(notes):
        nx, ny, nw, nh = px + 19, 170 + k * 68, pw - 38, 60
        t0 = done + 0.04 + 0.06 * k
        note_svgs.append(f"""<g opacity="0">
  {anim("opacity", [(0, 0), (t0, 0), (t0 + 0.03, 1), (fade[0], 1), (fade[1], 0), (1, 0)], D)}
  {anim("transform", [(0, "0 -14"), (t0, "0 -14"), (t0 + 0.03, "0 0"), (1, "0 0")], D, tag="animateTransform", extra=' type="translate"')}
  <rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="16" fill="#ffffff" fill-opacity="0.16" stroke="#ffffff" stroke-opacity="0.2"/>
  <rect x="{nx + 9}" y="{ny + 11}" width="28" height="28" rx="7" fill="{fill}"/>
  <text x="{nx + 23}" y="{ny + 30}" text-anchor="middle" class="sans" font-size="14" font-weight="800" fill="#fff">{letter}</text>
  <text x="{nx + 45}" y="{ny + 21}" class="sans" font-size="11.5" font-weight="700" fill="#fff">{esc(name)}</text>
  <text x="{nx + nw - 10}" y="{ny + 21}" text-anchor="end" class="sans" font-size="10" fill="#fff" fill-opacity="0.7">now</text>
  <text x="{nx + 45}" y="{ny + 36}" class="sans" font-size="10.5" fill="#fff" fill-opacity="0.92">{esc(l1)}</text>
  <text x="{nx + 45}" y="{ny + 50}" class="sans" font-size="10.5" fill="#fff" fill-opacity="0.92">{esc(l2)}</text>
</g>""")

    island_x = [(0, cx - 46), (done, cx - 46), (done + 0.03, cx - 98), (fade[0], cx - 98), (fade[1], cx - 46), (1, cx - 46)]
    island_w = [(0, 92), (done, 92), (done + 0.03, 196), (fade[0], 196), (fade[1], 92), (1, 92)]
    island_txt = [(0, 0), (done + 0.03, 0), (done + 0.05, 1), (fade[0] - 0.01, 1), (fade[0], 0), (1, 0)]
    title_a = [(0, 1), (done, 1), (done + 0.01, 0), (fade[1], 0), (fade[1] + 0.01, 1), (1, 1)]
    title_b = [(0, 0), (done, 0), (done + 0.01, 1), (fade[1], 1), (fade[1] + 0.01, 0), (1, 0)]

    body = f"""{card_bg(W, H, WINDOW)}
<defs>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{TYPE_DECL}"/></linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="{SWIFT}" stop-opacity="0.28"/><stop offset="0.55" stop-color="{OTHER_TYPE}" stop-opacity="0.08"/><stop offset="1" stop-color="{OTHER_TYPE}" stop-opacity="0"/></radialGradient>
  <linearGradient id="wall" x1="0" y1="0" x2="0.4" y2="1">
    <stop offset="0" stop-color="#ff9a5c"/><stop offset="0.35" stop-color="{SWIFT}"/>
    <stop offset="0.75" stop-color="#9b4dea"/><stop offset="1" stop-color="#1e1b4b"/>
  </linearGradient>
  <linearGradient id="ic0" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#34d399"/><stop offset="1" stop-color="#047857"/></linearGradient>
  <linearGradient id="ic1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#2563eb"/></linearGradient>
  <linearGradient id="ic2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fb923c"/><stop offset="1" stop-color="{SWIFT}"/></linearGradient>
  <clipPath id="screen"><rect x="{px + 9}" y="{py + 9}" width="{pw - 18}" height="{ph - 18}" rx="36"/></clipPath>
  {"".join(clips)}
</defs>

<text x="32" y="68" class="sans" font-size="42" font-weight="800" fill="url(#name)">Mohamed Haggag</text>
<text x="32" y="102" class="mono" font-size="14" fill="{COMMENT}">// Senior iOS Developer · turning ideas into apps people use every day</text>

<!-- Xcode-style build window -->
<rect x="24" y="124" width="596" height="312" rx="12" fill="{EDITOR}" stroke="{BORDER}"/>
{title_bar(24, 124, 596, "", r=12, h=36)}
<text x="330" y="146.5" text-anchor="middle" class="sans" font-size="12.5" fill="{COMMENT}">Building “Mohamed Haggag”…{anim("opacity", title_a, D)}</text>
<text x="330" y="146.5" text-anchor="middle" class="sans" font-size="12.5" fill="{COMMENT}" opacity="0"><tspan fill="{SUCCESS}">✓ Build Succeeded</tspan>  |  Today at 9:41{anim("opacity", title_b, D)}</text>
<rect x="24" y="159" width="0" height="2" fill="{URL}">
  {anim("width", [(0, 0), (0.03, 0), (done, 596), (fade[1], 596), (fade[1] + 0.01, 0), (1, 0)], D)}
  {anim("fill", [(0, URL), (done, URL), (done + 0.01, SUCCESS), (fade[1], SUCCESS), (fade[1] + 0.01, URL), (1, URL)], D)}
</rect>
<g>
  {anim("opacity", [(0, 1), (fade[0], 1), (fade[1], 0), (1, 0)], D)}
  {chr(10).join(texts)}
</g>

<!-- iPhone lock screen -->
{"" if crop else f'<circle cx="{cx}" cy="230" r="250" fill="url(#glow)"/>'}
<rect x="{px - 2.5}" y="{py + 96}" width="3" height="34" rx="1.5" fill="#3b3b44"/>
<rect x="{px - 2.5}" y="{py + 140}" width="3" height="56" rx="1.5" fill="#3b3b44"/>
<rect x="{px + pw - 0.5}" y="{py + 120}" width="3" height="70" rx="1.5" fill="#3b3b44"/>
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="44" fill="#0a0a0c" stroke="#3b3b44" stroke-width="2.5"/>
<g clip-path="url(#screen)">
  <rect x="{px + 9}" y="{py + 9}" width="{pw - 18}" height="{ph - 18}" fill="url(#wall)"/>
  <circle cx="{px + 40}" cy="{py + 330}" r="90" fill="#ffffff" fill-opacity="0.07"/>
  <circle cx="{px + pw - 20}" cy="{py + 120}" r="70" fill="#ffffff" fill-opacity="0.06"/>
  <text x="{cx}" y="90" text-anchor="middle" class="sans" font-size="13" font-weight="600" fill="#fff" fill-opacity="0.88">Cairo, Egypt</text>
  <text x="{cx}" y="148" text-anchor="middle" class="sans" font-size="60" font-weight="700" fill="#fff">9:41</text>
  {chr(10).join(note_svgs)}
  <circle cx="{px + 50}" cy="400" r="18" fill="#000" fill-opacity="0.35"/>
  <rect x="{px + 46}" y="390" width="8" height="18" rx="2" fill="#fff" fill-opacity="0.9"/>
  <circle cx="{px + pw - 50}" cy="400" r="18" fill="#000" fill-opacity="0.35"/>
  <rect x="{px + pw - 59}" y="393" width="18" height="13" rx="3" fill="#fff" fill-opacity="0.9"/>
  <circle cx="{px + pw - 50}" cy="399.5" r="3.5" fill="#1e1b4b"/>
  <rect x="{cx - 50}" y="{py + ph - 22}" width="100" height="4" rx="2" fill="#fff" fill-opacity="0.85"/>
</g>
<!-- Dynamic Island: expands into a live activity when the build ships -->
<rect x="{cx - 46}" y="{py + 20}" width="92" height="27" rx="13.5" fill="#000">
  {anim("x", island_x, D)}
  {anim("width", island_w, D)}
</rect>
<g opacity="0">
  {anim("opacity", island_txt, D)}
  <circle cx="{cx - 80}" cy="{py + 33.5}" r="7" fill="{SUCCESS}"/>
  <path d="M{cx - 83.5} {py + 33.5}l2.5 2.5 4.5-5" fill="none" stroke="#000" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="{cx + 6}" y="{py + 37.5}" text-anchor="middle" class="sans" font-size="11" font-weight="600" fill="#fff">Shipped to the App Store</text>
</g>"""
    return svg(W, H, "Mohamed Haggag, Senior iOS Developer",
               "An Xcode-style build log compiles Mohamed's skills and succeeds, then an iPhone lock screen "
               "receives notifications from apps he shipped: Aseel, the Super App and his Beetleware team.", body, crop)


# -------------------------------------------------------------- whoami ----

def whoami():
    W = 960
    K = lambda t: (t, KEYWORD, "700")
    P = lambda t: (t, PLAIN)
    S = lambda t: (t, STRING)
    C = lambda t: (t, COMMENT)
    DECL = lambda t: (t, OTHER_DECL)
    PT = lambda t: (t, PROJECT_TYPE)
    OT = lambda t: (t, OTHER_TYPE)
    PF = lambda t: (t, PROJECT_FUNC)

    def array(name, pad, items):
        parts = [P("    "), K("let"), P(" "), DECL(name), P(" " * pad + "= [")]
        for i, item in enumerate(items):
            parts += [S(f'"{item}"')] + ([P(", ")] if i < len(items) - 1 else [])
        return parts + [P("]")]

    code = [
        [C("//  whoami.swift")],
        [C("//  Created by Mohamed Haggag · Cairo, Egypt")],
        [],
        [K("import"), P(" SwiftUI")],
        [],
        [K("struct"), P(" "), (("MohamedHaggag"), TYPE_DECL), P(": "), PT("SeniorIOSEngineer"), P(" {")],
        [P("    "), K("let"), P(" "), DECL("role"), P("       = "), S('"Senior iOS Developer @ Beetleware"')],
        [P("    "), K("let"), P(" "), DECL("team"), P("       = "), ("4", NUMBER), P("  "), C("// iOS engineers I lead")],
        [P("    "), K("let"), P(" "), DECL("experience"), P(" = "), S('"8+ years · KSA · Iraq · Egypt"')],
        [],
        array("languages", 4, ["Swift 6", "SwiftUI", "UIKit", "Combine", "async/await"]),
        array("architecture", 1, ["Clean Architecture", "MVVM", "VIP", "VIPER", "SPM"]),
        array("superpowers", 2, ["E2EE · CryptoKit", "Apple Pay · Mada", "SignalR · WebRTC"]),
        array("delivery", 5, ["Fastlane", "Bitrise", "GitHub Actions", "Xcode Cloud"]),
        [],
        [P("    "), K("var"), P(" "), DECL("currentlyBuilding"), P(": "), OT("String"), P(" { "),
         S('"Super app: chat · calls · wallet · e-gov"'), P(" }")],
        [P("    "), K("var"), P(" "), DECL("growingToward"), P(": "), OT("String"), P(" { "),
         S('"Product-focused technical leadership"'), P(" }")],
        [],
        [P("    "), K("func"), P(" "), DECL("collaborate"), P("(on idea: "), PT("Idea"), P(") "), K("async"), P(" "),
         K("throws"), P(" -> "), PT("App"), P(" {")],
        [P("        "), K("try"), P(" "), K("await"), P(" idea."), PF("validate"), P("()."), PF("design"), P("()."),
         PF("build"), P("()."), PF("ship"), P("()")],
        [P("    }")],
        [P("}")],
    ]
    top, lh = 76, 21
    H = top + len(code) * lh + 22
    active = 19  # line with the cursor (0-based)

    rows = []
    for i, parts in enumerate(code):
        y = top + i * lh + 15
        rows.append(f'<text x="58" y="{y}" text-anchor="end" class="mono" font-size="12" '
                    f'fill="{PLAIN if i == active else LINE_NO}">{i + 1}</text>')
        if parts:
            rows.append(f'<text x="78" y="{y}" class="mono" font-size="13.5" xml:space="preserve">{tspans(parts)}'
                        + (f'<tspan fill="{PLAIN}">▏<animate attributeName="fill-opacity" values="1;1;0;0" '
                           f'keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></tspan>' if i == active else "")
                        + '</text>')

    body = f"""{card_bg(W, H)}
{title_bar(0, 0, W, "", h=40)}
<rect x="300" y="9" width="360" height="22" rx="6" fill="#000" fill-opacity="0.25"/>
<text x="480" y="24.5" text-anchor="middle" class="sans" font-size="12" fill="{COMMENT}">7aggag  <tspan fill="{SUCCESS}">✓</tspan>  Build Succeeded  |  Today at 9:41</text>
<!-- tab + jump bar -->
<rect x="0" y="40" width="{W}" height="26" fill="#252529"/>
<rect x="0" y="40" width="168" height="26" fill="{EDITOR}"/>
<rect x="14" y="48" width="11" height="11" rx="2.5" fill="{SWIFT}"/>
<text x="32" y="57.5" class="sans" font-size="12" fill="{PLAIN}">whoami.swift</text>
<text x="186" y="57.5" class="sans" font-size="11.5" fill="{COMMENT}">7aggag  ›  Sources  ›  <tspan fill="{SWIFT}">■</tspan> whoami.swift  ›  <tspan fill="{TYPE_DECL}">S</tspan> MohamedHaggag</text>
<path d="M0 66H{W}" stroke="#000" stroke-opacity="0.45"/>
<rect x="0" y="{top + active * lh}" width="{W}" height="{lh}" fill="{CURRENT_LINE}"/>
{chr(10).join(rows)}"""
    return svg(W, H, "whoami.swift",
               "A Swift struct describing Mohamed Haggag in Xcode's Default Dark theme: Senior iOS Developer at "
               "Beetleware leading 4 iOS engineers, 8+ years shipping to KSA, Iraq and Egypt; Swift 6, SwiftUI, "
               "UIKit, Combine, async/await; Clean Architecture, MVVM, VIP, VIPER, SPM; E2EE with CryptoKit, "
               "Apple Pay and Mada, SignalR and WebRTC; Fastlane, Bitrise, GitHub Actions, Xcode Cloud.", body)


# ---------------------------------------------------------------- apps ----

def apps():
    W, H = 960, 300
    items = [
        ("Super App", "Iraq · E2EE chat", "#22d3ee", "#2563eb", "bubble", None),
        ("Aseel", "4.6★ · 7.4K ratings", "#34d399", "#047857", "A", "24"),
        ("Tameer Business", "Nafath · Mada", "#818cf8", "#4338ca", "T", None),
        ("Sahn & Rageef", "SwiftUI rewrite", "#fb923c", "#dc2626", "S&amp;R", None),
        ("Istend", "4.6★ · KSA", "#c084fc", "#7e22ce", "IS", None),
        ("Flex Kitchen", "Nutrition plans", "#a3e635", "#15803d", "FK", None),
        ("Healthy & More", "Nutrition plans", "#f472b6", "#be185d", "H+", None),
    ]
    slot = (W - 96) / len(items)
    size, top = 76, 54
    defs, icons = [], []
    for i, (name, cap, c1, c2, glyph, badge) in enumerate(items):
        cx = 48 + slot / 2 + i * slot
        x, cy = cx - size / 2, top + size / 2
        defs.append(f'<linearGradient id="a{i}" x1="0" y1="0" x2="1" y2="1">'
                    f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
        if glyph == "bubble":
            mark = (f'<path d="M{cx - 20} {cy - 14}h40a6 6 0 0 1 6 6v20a6 6 0 0 1-6 6h-22l-10 9v-9h-8a6 6 0 0 1-6-6v-20'
                    f'a6 6 0 0 1 6-6z" fill="#fff"/>'
                    f'<rect x="{cx - 6}" y="{cy - 4}" width="12" height="10" rx="2" fill="{c2}"/>'
                    f'<path d="M{cx - 3.5} {cy - 4}v-3a3.5 3.5 0 0 1 7 0v3" fill="none" stroke="{c2}" stroke-width="2"/>')
        else:
            fs = 30 if len(glyph) <= 2 else 21
            mark = (f'<text x="{cx}" y="{cy + fs * 0.36}" text-anchor="middle" class="sans" font-size="{fs}" '
                    f'font-weight="800" fill="#fff">{glyph}</text>')
        badge_svg = ""
        if badge:
            badge_svg = (f'<circle cx="{x + size - 4}" cy="{top + 4}" r="13" fill="#ff3b30" stroke="{EDITOR}" stroke-width="2.5"/>'
                         f'<text x="{x + size - 4}" y="{top + 8.5}" text-anchor="middle" class="sans" font-size="12.5" '
                         f'font-weight="700" fill="#fff">{badge}</text>')
        # Home-screen "jiggle mode": a short wiggle every few seconds, staggered per icon
        wiggle = (f'<animateTransform attributeName="transform" type="rotate" dur="6s" begin="{i * 0.12:.2f}s" '
                  f'repeatCount="indefinite" keyTimes="0;0.03;0.06;0.09;0.12;0.15;1" '
                  f'values="0 {cx} {cy};-2.5 {cx} {cy};2.5 {cx} {cy};-2.5 {cx} {cy};2.5 {cx} {cy};0 {cx} {cy};0 {cx} {cy}"/>')
        icons.append(f"""<g>{wiggle}
  <rect x="{x}" y="{top}" width="{size}" height="{size}" rx="18" fill="url(#a{i})"/>
  <rect x="{x}" y="{top}" width="{size}" height="{size / 2}" rx="18" fill="url(#gloss)"/>
  {mark}{badge_svg}
</g>
<text x="{cx}" y="{top + size + 26}" text-anchor="middle" class="sans" font-size="13" font-weight="600" fill="{PLAIN}">{esc(name)}</text>
<text x="{cx}" y="{top + size + 44}" text-anchor="middle" class="sans" font-size="11.5" fill="{COMMENT}">{esc(cap)}</text>""")

    stats = [("24", "Aseel releases since 2024"), ("4.6★", "from 7.4K App Store ratings"), ("3", "markets: KSA · Iraq · Egypt")]
    dock_w = W - 96
    stat_svgs = []
    for k, (big, small) in enumerate(stats):
        sx = 48 + dock_w / 6 + k * dock_w / 3
        stat_svgs.append(f'<text x="{sx}" y="250" text-anchor="middle" class="sans" font-size="15" fill="{COMMENT}">'
                         f'<tspan font-size="20" font-weight="800" fill="{NUMBER}">{esc(big)}</tspan>  '
                         f'<tspan fill="{PLAIN}">{esc(small)}</tspan></text>')
    body = f"""{card_bg(W, H)}
<defs>
  {"".join(defs)}
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<text x="48" y="34" class="mono" font-size="12.5" fill="{COMMENT}">// ~/Applications <tspan fill="{SUCCESS}">●</tspan> shipped to the App Store</text>
{chr(10).join(icons)}
<rect x="48" y="216" width="{dock_w}" height="56" rx="16" fill="{CURRENT_LINE}" stroke="{BORDER}"/>
{chr(10).join(stat_svgs)}"""
    return svg(W, H, "Apps Mohamed Haggag shipped",
               "An iOS home screen with seven apps: Super App, Aseel (24 releases, 4.6 stars from 7.4K ratings), "
               "Tameer Business, Sahn & Rageef, Istend, Flex Kitchen and Healthy & More.", body)


# ------------------------------------------------------------- journey ----

def journey():
    W, H = 960, 400
    rows = [
        ("a1f9e3c", [("(", COMMENT), ("HEAD -> ", TYPE_DECL), ("main", SUCCESS), (") ", COMMENT)],
         "Beetleware · Senior iOS Developer · leading 4 iOS engineers", "Mar 2024 → now", 0),
        ("7c2d0b8", [], "ElMasadr · Senior iOS Developer · shipped Istend (4.6★)", "Sep 2023 → Apr 2024", 0),
        ("e41aa90", [("(", COMMENT), ("tag: promoted", KEYWORD), (") ", COMMENT)],
         "Fintech-SA · Senior iOS Developer · led the iOS team", "Jan 2023 → Sep 2023", 1),
        ("3b7f21d", [], "Fintech-SA (Rasid Payments) · iOS Developer · payments suite", "Jan 2022 → Dec 2022", 1),
        ("9d02c4e", [], "ICOSOL · iOS Developer · apps shipped to the App Store", "Sep 2020 → Dec 2021", 0),
        ("5e8a1f0", [], "Freelance · iOS Developer · client apps incl. a pharma CRM", "Jan 2018 → Aug 2020", 0),
        ("c0ffee1", [], "Initial commit · B.Sc. Computer Science, Mansoura University", "2015 → 2019", 0),
    ]
    ys = [118 + r * 38 for r in range(len(rows))]
    lane = [48, 78]
    n = len(rows)
    reveal = lambda r: 0.3 + (n - 1 - r) * 0.32  # oldest first, growing upward

    branch = (f'M{lane[0]} {ys[4]}C{lane[0]} {ys[4] - 22} {lane[1]} {ys[3] + 16} {lane[1]} {ys[3]}'
              f'L{lane[1]} {ys[2]}C{lane[1]} {ys[2] - 16} {lane[0]} {ys[1] + 22} {lane[0]} {ys[1]}')
    total = reveal(0) - reveal(n - 1) + 0.3
    graph = f"""<clipPath id="grow"><rect x="30" y="{ys[-1] + 12}" width="70" height="0">
  {once("y", ys[-1] + 12, ys[0] - 12, reveal(n - 1), total)}
  {once("height", 0, ys[-1] - ys[0] + 24, reveal(n - 1), total)}
</rect></clipPath>
<g clip-path="url(#grow)" fill="none" stroke-width="3" stroke-linecap="round">
  <path d="M{lane[0]} {ys[-1]}V{ys[0]}" stroke="{PREPROC}"/>
  <path d="{branch}" stroke="{OTHER_TYPE}"/>
</g>"""

    row_svgs = []
    for r, (sha, refs, msg, when, ln) in enumerate(rows):
        x, y, t = lane[ln], ys[r], reveal(r)
        color = OTHER_TYPE if ln else PREPROC
        head = ""
        if r == 0:
            head = (f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{PREPROC}" stroke-width="2">'
                    f'<animate attributeName="r" values="7;16" dur="2s" begin="{t + 0.4:.2f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="stroke-opacity" values="0.8;0" dur="2s" begin="{t + 0.4:.2f}s" repeatCount="indefinite"/></circle>')
        node_fill = PREPROC if r == 0 else EDITOR
        row_svgs.append(f"""<g opacity="0">
  {once("opacity", 0, 1, t, 0.35)}
  {once("transform", "-10 0", "0 0", t, 0.35, tag="animateTransform", extra=' type="translate"')}
  {head}<circle cx="{x}" cy="{y}" r="6.5" fill="{node_fill}" stroke="{color}" stroke-width="3"/>
  <text x="112" y="{y + 4.5}" class="mono" font-size="13" fill="{NUMBER}">{sha}</text>
  <text x="180" y="{y + 4.5}" class="mono" font-size="13" xml:space="preserve">{tspans(refs)}{tspans([(msg, PLAIN)])}</text>
  <text x="{W - 32}" y="{y + 4.5}" text-anchor="end" class="sans" font-size="12.5" fill="{COMMENT}">{esc(when)}</text>
</g>""")

    body = f"""{card_bg(W, H)}
{title_bar(0, 0, W, "haggag — career.git", h=44)}
<text x="32" y="78" class="mono" font-size="13.5" xml:space="preserve"><tspan fill="{COMMENT}">$ </tspan><tspan fill="{KEYWORD}" font-weight="700">git log </tspan><tspan fill="{OTHER_DECL}">--graph --oneline --decorate</tspan></text>
{graph}
{chr(10).join(row_svgs)}
<text x="32" y="{ys[-1] + 40}" class="mono" font-size="13" fill="{COMMENT}" opacity="0">(END){once("opacity", 0, 1, reveal(0) + 0.4, 0.3)}</text>"""
    return svg(W, H, "Mohamed Haggag's career as a git log",
               "A git log graph of his career, oldest at the bottom: B.Sc. Computer Science at Mansoura University, "
               "freelance iOS development, ICOSOL, Fintech-SA (iOS Developer, then promoted to Senior), ElMasadr, "
               "and Beetleware as HEAD, where he leads 4 iOS engineers.", body)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    phone = lambda: hero(done=0.12, crop=(686, 8, 260, 444))  # website hero: notifications arrive sooner
    for name, make in (("hero", hero), ("phone", phone), ("whoami", whoami), ("apps", apps), ("journey", journey)):
        (OUT / f"{name}.svg").write_text(make(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")

"""Draw the Part II draft figures (SVG) from the CSVs in data/.

Run from the repository root after the two analysis scripts:
    python analysis/fig3_fig4.py
    python analysis/fig_plan_pair.py
    python analysis/make_part2_figures.py
Output: figures/fig1 ... fig7 (.svg)
"""
import os
from xml.sax.saxutils import escape

import pandas as pd

OUT = "figures"
os.makedirs(OUT, exist_ok=True)

INK, SUB, NOTE = "#1f2937", "#4b5563", "#9ca3af"
A, B = "#2563a8", "#e07b39"
GRID, PALE, HI, WARM = "#e5e7eb", "#d1d5db", "#c2410c", "#fdecdf"
FONT = 'font-family="Helvetica Neue, Helvetica, Arial, sans-serif"'

pair = pd.read_csv("data/plan_pair.csv", index_col=0)
summ = pd.read_csv("data/plan_pair_summary.csv", index_col=0)["value"]
curve = pd.read_csv("data/plan_pair_cost_curve.csv")
f3 = pd.read_csv("data/fig3_overpay_by_premium_rule.csv")
f4 = pd.read_csv("data/fig4_worst_case_vs_cushion.csv")
S = lambda k: float(summ[k])

PA, PB = pair.loc["A"], pair.loc["B"]
SRC_PLANS = "CMS 2026 Pennsylvania plan files (premiums for a 26-year-old, Allegheny County)"


def t(x, y, s, size=16, fill=INK, weight="normal", anchor="start", rotate=None):
    rot = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{rot}>{escape(str(s))}</text>')


def r(x, y, w, h, fill, rx=0, stroke="none", sw=1):
    return (f'<rect x="{x}" y="{y}" width="{max(w, 0)}" height="{max(h, 0)}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def ln(x1, y1, x2, y2, c=GRID, w=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def header(title, subtitle=None):
    out = [t(60, 62, title, 27, INK, "bold")]
    if subtitle:
        out.append(t(60, 93, subtitle, 16, SUB))
    return out


def source(H, s):
    return t(60, H - 24, "Source: " + s, 13, NOTE)


def save(name, W, H, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           + r(0, 0, W, H, "white") + "".join(body) + "</svg>")
    open(os.path.join(OUT, name), "w").write(svg)


money = lambda v: f"${v:,.0f}"


# ---------------------------------------------------------------- Figure 1: BEFORE
def plan_table(b, x, y, w, compact=False):
    rows = [("Monthly premium", money(PA.monthly_premium), money(PB.monthly_premium)),
            ("Deductible", money(PA.deductible_individual), money(PB.deductible_individual)),
            ("Coinsurance", f"{PA.coinsurance_pct:.0f}%", f"{PB.coinsurance_pct:.0f}%"),
            ("Out-of-pocket maximum", money(PA.oop_max_individual), money(PB.oop_max_individual)),
            ("Plan type / network", f"{PA.plan_type}", f"{PB.plan_type}")]
    rh = 44 if not compact else 36
    fs = 16 if not compact else 14
    c1, c2 = x + w * 0.58, x + w * 0.84
    b.append(r(x, y, w, rh, "#f3f4f6", 6))
    b.append(t(x + 16, y + rh * 0.65, "", fs))
    b.append(t(c1, y + rh * 0.65, "Plan A", fs, A, "bold", "middle"))
    b.append(t(c2, y + rh * 0.65, "Plan B", fs, B, "bold", "middle"))
    b.append(t(c1, y + rh * 0.65 + (16 if not compact else 13), f"{PA.metal_level}", 12, SUB, "normal", "middle"))
    b.append(t(c2, y + rh * 0.65 + (16 if not compact else 13), f"{PB.metal_level}", 12, SUB, "normal", "middle"))
    for i, (lab, va, vb) in enumerate(rows):
        yy = y + rh * (i + 1) + 8
        b.append(ln(x, yy + rh, x + w, yy + rh, GRID, 1))
        b.append(t(x + 16, yy + rh * 0.65, lab, fs, INK))
        b.append(t(c1, yy + rh * 0.65, va, fs, INK, "normal", "middle"))
        b.append(t(c2, yy + rh * 0.65, vb, fs, INK, "normal", "middle"))
    return y + rh * (len(rows) + 1) + 8


def fig1():
    W, H = 1100, 540
    b = header("Which plan would you choose?",
               "Two real 2026 plans sold in Pittsburgh by the same insurer, shown the way plan pages usually show them")
    end = plan_table(b, 60, 125, 640)
    # margin notes: the questions a user is left with
    nx = 750
    b.append(t(nx, 150, "What a user has to work out alone", 16, HI, "bold"))
    notes = [("Plan A saves $" + f"{12*(PB.monthly_premium-PA.monthly_premium):,.0f}" + " a year", "in premiums. Is that worth it?"),
             ("What does a $6,700 deductible", "mean for my bills this year?"),
             ("What is 40% coinsurance", "of a bill I can't predict?"),
             ("Which plan is cheaper", "for someone like me?")]
    for i, (l1, l2) in enumerate(notes):
        yy = 190 + i * 70
        b.append(f'<circle cx="{nx+10}" cy="{yy-5}" r="11" fill="{HI}"/>')
        b.append(t(nx + 10, yy, str(i + 1), 13, "white", "bold", "middle"))
        b.append(t(nx + 32, yy, l1, 15, INK))
        b.append(t(nx + 32, yy + 20, l2, 15, SUB))
    b.append(t(60, end + 40, "Every number is accurate, but none of them answers the question the user actually has.", 16, INK, "bold"))
    b.append(source(H, SRC_PLANS + "."))
    save("fig1_before_plan_table.svg", W, H, b)


# ---------------------------------------------------------------- Figure 2: cost curves
def fig2():
    W, H = 1180, 660
    be = S("break_even_medical_bills")
    b = header(f"{100 - S('share_spend_above_break_even_pct'):.0f} of 100 people should pick Plan A. The table can't tell you which group you're in.",
               f"Total cost for the year (premiums + your share of medical bills). The plans cost the same at {money(be)} in medical bills.")
    x0, x1, yt, yb = 130, 880, 140, 500
    xmax, ymax = 20000, 14000
    X = lambda v: x0 + (x1 - x0) * v / xmax
    Y = lambda v: yb - (yb - yt) * v / ymax
    for v in range(0, ymax + 1, 2000):
        b.append(ln(x0, Y(v), x1, Y(v), GRID if v else "#9ca3af", 1))
        b.append(t(x0 - 10, Y(v) + 5, f"${v//1000}k" if v else "$0", 13, SUB, "normal", "end"))
    for v in range(0, xmax + 1, 5000):
        b.append(t(X(v), yb + 24, f"${v//1000}k" if v else "$0", 13, SUB, "normal", "middle"))
    b.append(t((x0 + x1) / 2, yb + 54, "Medical bills for the year (before insurance pays)", 14, SUB, "normal", "middle"))
    b.append(t(28, (yt + yb) / 2, "Total cost for the year", 14, SUB, "normal", "middle", rotate=-90))
    # shading: share of 20-somethings to the left of break-even
    b.append(r(x0, yt, X(be) - x0, yb - yt, "#eef4fb"))
    c = curve[curve.medical_bills <= xmax]
    for col, colr in [("plan_a_total", A), ("plan_b_total", B)]:
        d = "M" + " L".join(f"{X(m):.1f} {Y(v):.1f}" for m, v in zip(c.medical_bills, c[col]))
        b.append(f'<path d="{d}" fill="none" stroke="{colr}" stroke-width="4"/>')
    ya = float(c.plan_a_total.iloc[-1]); yb2 = float(c.plan_b_total.iloc[-1])
    b.append(t(x1 + 12, Y(ya) + 5, "Plan A", 16, A, "bold"))
    b.append(t(x1 + 12, Y(ya) + 24, "Bronze", 13, SUB))
    b.append(t(x1 + 12, Y(yb2) + 5, "Plan B", 16, B, "bold"))
    b.append(t(x1 + 12, Y(yb2) + 24, "Gold", 13, SUB))
    # break-even marker
    ybe = 12 * PA.monthly_premium + min(be, PA.deductible_individual)
    b.append(f'<circle cx="{X(be)}" cy="{Y(ybe)}" r="8" fill="white" stroke="{INK}" stroke-width="2.5"/>')
    b.append(t(X(be) + 14, Y(ybe) + 34, f"Break-even: {money(be)}", 14, INK, "bold"))
    b.append(t(X(be) + 14, Y(ybe) + 52, "both plans cost the same", 13, SUB))
    # population markers
    p50, p90 = S("spend_p50"), S("spend_p90")
    for v, lab1, lab2 in [(p50, "Half of people aged 22-30", f"spend less than {money(p50)}"),
                          (p90, "1 in 10 spend", f"more than {money(p90)}")]:
        b.append(ln(X(v), yb, X(v), yb - 14, INK, 2))
        b.append(f'<path d="M{X(v)-6} {yb+0} L{X(v)+6} {yb+0} L{X(v)} {yb-10} Z" fill="{INK}"/>')
    b.append(t(X(p50) + 8, 440, f"Half of people aged 22-30 spend", 13, SUB))
    b.append(t(X(p50) + 8, 457, f"less than {money(p50)} a year", 13, SUB))
    b.append(t(X(p90) + 8, 440, f"1 in 10 spend more", 13, SUB))
    b.append(t(X(p90) + 8, 457, f"than {money(p90)}", 13, SUB))
    b.append(t(x0 + 10, yt + 22, f"{100 - S('share_spend_above_break_even_pct'):.0f} of 100 people in their 20s spend less than this", 14, A, "bold"))
    b.append(source(H, SRC_PLANS + "; MEPS 2023, ages 22-30, weighted. Simplified cost model; copays not included."))
    save("fig2_cost_curves.svg", W, H, b)


# ---------------------------------------------------------------- Figure 3: research (published)
def person(cx, cy, fill, s=1.0):
    return (f'<circle cx="{cx}" cy="{cy - 10*s}" r="{5.2*s}" fill="{fill}"/>'
            f'<path d="M{cx-8.5*s} {cy+11*s} Q{cx-8.5*s} {cy-2*s} {cx} {cy-2*s} '
            f'Q{cx+8.5*s} {cy-2*s} {cx+8.5*s} {cy+11*s} Z" fill="{fill}"/>')


def fig3():
    W, H = 1100, 600
    b = header("Most people can't read their health plan, and it costs them",
               "Findings from two published studies")
    b.append(t(60, 165, "14%", 56, A, "bold"))
    b.append(t(60, 198, "understood all four basic terms", 17, INK))
    b.append(t(60, 220, "(deductible, copay, coinsurance, out-of-pocket max)", 14, SUB))
    for k in range(100):
        b.append(person(75 + (k % 20) * 23, 270 + (k // 20) * 46, A if k < 14 else PALE, 0.95))
    b.append(t(60, 510, "Each figure = 1 in 100 privately insured U.S. adults (2013 survey)", 13, SUB))
    b.append(ln(560, 130, 560, 520, GRID, 1))
    b.append(t(610, 165, "61%", 56, B, "bold"))
    b.append(t(610, 198, "of employees chose a plan that was", 17, INK))
    b.append(t(610, 220, "worse for them no matter what happened", 17, INK))
    b.append(r(610, 260, 430, 40, "#f3f4f6", 4))
    b.append(r(610, 260, 430 * 0.61, 40, B, 4))
    b.append(t(620, 286, "61% chose the worse plan", 15, "white", "bold"))
    b.append(t(1030, 286, "39%", 15, SUB, "normal", "end"))
    b.append(t(610, 350, "On average this cost them an extra", 17, INK))
    b.append(t(610, 375, "24% of what they paid in premiums.", 17, INK))
    b.append(t(610, 420, "The main reason: not understanding", 17, INK))
    b.append(t(610, 445, "the plans, not having too many choices.", 17, INK))
    b.append(source(H, "Loewenstein et al. (2013), Journal of Health Economics; Bhargava, Loewenstein & Sydnor (2017), QJE."))
    save("fig3_research.svg", W, H, b)


# ---------------------------------------------------------------- Figure 4: who needs what (merged)
def fig4():
    W, H = 1200, 640
    b = header("Different people need a different number first",
               "Two groups the plan table fails, people aged 22-35")
    # left panel: frequent users and the premium
    raw = f3.share_pct.tolist()
    fl = [int(v) for v in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - fl[i], reverse=True)[:100 - sum(fl)]:
        fl[i] += 1
    big = sum(fl[3:])
    b.append(t(60, 140, "IF YOU SEE A DOCTOR OFTEN", 14, A, "bold"))
    b.append(t(60, 172, "The lowest premium can cost you more", 20, INK, "bold"))
    labs = ["Under $100", "$100-1,000", "$1,000 or more"]
    vals = [fl[0], fl[1] + fl[2], big]
    x0 = 200
    for k, (lab, v) in enumerate(zip(labs, vals)):
        y = 205 + k * 56
        b.append(t(x0 - 12, y + 25, lab, 15, INK, "normal", "end"))
        b.append(r(x0, y + 6, v * 4.4, 30, HI if k == 2 else PALE, 3))
        b.append(t(x0 + v * 4.4 + 10, y + 27, f"{v} of 100", 15, HI if k == 2 else SUB, "bold"))
    b.append(t(60, 395, "Extra cost for the year if everyone aged 22-30 picked", 14, SUB))
    b.append(t(60, 414, "the lowest-premium plan (vs. their own cheapest plan).", 14, SUB))
    b.append(t(60, 460, f"{big} of 100 would pay $1,000+ more;", 17, INK, "bold"))
    b.append(t(60, 484, "7 in 10 of them saw a doctor 5+ times that year.", 17, INK))
    b.append(t(60, 520, "Show them: their yearly total, not just the premium.", 16, A, "bold"))
    b.append(ln(600, 130, 600, 560, GRID, 1))
    # right panel: no cushion and the worst case
    med = {row.item.split(", ")[1].split(" plans")[0]: row.value for row in f4.itertuples() if "Median" in row.item}
    cant = {row.item.split("ages ")[1]: row.value for row in f4.itertuples() if "Can't" in row.item}
    b.append(t(640, 140, "IF YOU HAVE LITTLE SAVED", 14, HI, "bold"))
    b.append(t(640, 172, "The worst case is far beyond reach", 20, INK, "bold"))
    xs0, xs1 = 640, 1130
    sc = lambda v: xs0 + (xs1 - xs0) * v / 11000
    rows = [("Emergency money half of under-35s couldn't raise", 2000, HI), ("Bronze worst case", med["Bronze"], A), ("Gold worst case", med["Gold"], A)]
    for k, (lab, v, col) in enumerate(rows):
        y = 205 + k * 56
        b.append(t(xs0, y + 2, lab, 13, SUB))
        b.append(r(xs0, y + 8, sc(v) - xs0, 28, col, 3))
        b.append(t(sc(v) + 8, y + 28, money(v), 15, col, "bold"))
    b.append(t(640, 395, "Median out-of-pocket maximum, 2026 plans sold in Allegheny", 14, SUB))
    b.append(t(640, 414, "County, vs. $2,000 in emergency money.", 14, SUB))
    b.append(t(640, 460, f"About 1 in 2 adults under 35 couldn't raise $2,000", 17, INK, "bold"))
    b.append(t(640, 484, f"within a month ({cant['18-24']:.0f}% aged 18-24, {cant['25-34']:.0f}% aged 25-34).", 17, INK))
    b.append(t(640, 520, "Show them: the worst case, before anything else.", 16, HI, "bold"))
    b.append(source(H, "MEPS 2023 x 72 CMS 2026 plans in Allegheny County (simplified cost model); FINRA Foundation NFCS 2024, weighted."))
    save("fig4_who_needs_what.svg", W, H, b)


# ---------------------------------------------------------------- Figure 5: evidence that numbers help
def fig5():
    W, H = 1100, 600
    b = header("Showing people what they'd pay halves the wrong choices",
               "Share who chose a plan that was worse for them in every case, by what they were shown")
    rows = [("Plan table only", 50, PALE, "50%"),
            ("Table + expected yearly cost", 35, "#93b4dc", "about 35%"),
            ("Table + range of possible yearly costs", 24, A, "24%")]
    x0 = 400
    for k, (lab, v, col, vl) in enumerate(rows):
        y = 150 + k * 80
        b.append(t(x0 - 15, y + 34, lab, 16, INK, "normal", "end"))
        b.append(r(x0, y + 12, v * 11, 40, col, 4))
        b.append(t(x0 + v * 11 + 12, y + 39, vl, 18, A if k == 2 else SUB, "bold"))
    b.append(t(60, 430, "A single average helps; showing the whole range helps about twice as much.", 17, INK, "bold"))
    b.append(t(60, 458, "What this study measured: choosing the right plan. What it didn't: whether people feel moved to act.", 16, SUB))
    b.append(t(60, 482, "That second part, the words around the numbers, is what this project's interviews test.", 16, SUB))
    b.append(source(H, "Samek & Sydnor (2020), NBER Working Paper 28003; online experiment, 692 U.S. adults. 'About 35%' is derived from reported effects."))
    save("fig5_evidence.svg", W, H, b)


# ---------------------------------------------------------------- Figure 6: three versions
def fig6():
    W, H = 1500, 760
    b = header("Same plans, three pages: terms, numbers, or numbers with words",
               "Which page helps someone choose, and which makes them want to act?")
    cols = [("1  TERMS (today)", SUB), ("2  NUMBERS", A), ("3  NUMBERS + WORDS", HI)]
    cw, gap, top = 440, 30, 130
    for k, (lab, col) in enumerate(cols):
        x = 60 + k * (cw + gap)
        b.append(t(x, top, lab, 15, col, "bold"))
        b.append(r(x, top + 12, cw, 500, "white", 10, col if k else GRID, 2 if k else 1.5))
    # column 1: the table
    plan_table(b, 72, top + 30, cw - 24, compact=True)
    b.append(t(80, top + 330, "Every term is there.", 15, INK, "bold"))
    b.append(t(80, top + 354, "The user still has to do the math.", 15, SUB))
    # column 2: numbers only
    x2 = 60 + cw + gap
    b.append(t(x2 + 20, top + 50, "For people aged 22-30, each year:", 14, INK, "bold"))
    cards = [("Typical year", S("a_total_typical_p50"), S("b_total_typical_p50")),
             ("Bad year (1 in 10)", S("a_total_bad_p90"), S("b_total_bad_p90")),
             ("Worst case", S("a_worst_case"), S("b_worst_case"))]
    for i, (lab, va, vb) in enumerate(cards):
        y = top + 70 + i * 72
        b.append(r(x2 + 16, y, cw - 32, 60, "#f9fafb", 8))
        b.append(t(x2 + 30, y + 36, lab, 14, INK))
        b.append(t(x2 + 255, y + 26, "Plan A", 11, A, "bold", "middle"))
        b.append(t(x2 + 255, y + 48, money(va), 17, A, "bold", "middle"))
        b.append(t(x2 + 360, y + 26, "Plan B", 11, B, "bold", "middle"))
        b.append(t(x2 + 360, y + 48, money(vb), 17, B, "bold", "middle"))
    ka = round(S("share_a_cheaper_pct"))
    b.append(t(x2 + 20, top + 315, f"Plan A is cheaper for {ka} of 100 people your age.", 14, INK, "bold"))
    # column 3: numbers + words
    x3 = 60 + 2 * (cw + gap)
    save_a = S("b_total_typical_p50") - S("a_total_typical_p50")
    save_b = S("a_total_bad_p90") - S("b_total_bad_p90")
    lines = [
        ("If you see a doctor once or twice a year", INK, "bold", 15),
        (f"Plan A likely saves you about {money(round(save_a, -2))} a year.", A, "bold", 15),
        (f"{ka} of 100 people your age come out ahead with it.", SUB, "normal", 14),
        ("", INK, "normal", 8),
        (f"If you expect more than {money(S('break_even_medical_bills'))} in medical bills", INK, "bold", 15),
        ("(ongoing visits, a planned procedure)", SUB, "normal", 14),
        (f"Plan B costs about {money(round(save_b, -2))} less in a bad year.", B, "bold", 15),
        ("", INK, "normal", 8),
        ("Not sure which group you're in?", INK, "bold", 15),
        ("Count last year's doctor visits. It's a good first clue.", SUB, "normal", 14),
        ("", INK, "normal", 8),
        ("Bad years are rare, but they're the year", INK, "normal", 15),
        ("insurance is for.", INK, "normal", 15),
    ]
    y = top + 52
    for txt, col, wgt, sz in lines:
        if txt:
            b.append(t(x3 + 20, y, txt, sz, col, wgt))
        y += sz + 11
    b.append(r(x3 + 20, top + 440, cw - 40, 44, HI, 8))
    b.append(t(x3 + cw / 2, top + 468, "Estimate my year in 2 minutes", 15, "white", "bold", "middle"))
    b.append(t(60, top + 550, "Evidence so far: numbers (2) help people choose correctly (Figure 5). Whether words (3) make people more willing to act is the hypothesis my interviews test.", 14, INK))
    b.append(source(H, SRC_PLANS + "; MEPS 2023, ages 22-30, weighted. Draft mockups; simplified cost model."))
    save("fig6_three_versions.svg", W, H, b)


# ---------------------------------------------------------------- Figure 7: checklist (CTA)
def fig7():
    W, H = 1100, 560
    b = header("Before you design a comparison page, ask four questions",
               "Call to action for product teams, with where each one shows up in version 3")
    items = [("1", "Is this number about this user?", "Relevance", "\"people your age\", \"if you see a doctor once or twice a year\""),
             ("2", "Does it show the range, not just one guess?", "Uncertainty", "typical year, bad year and worst case"),
             ("3", "Would it change their choice?", "Decision impact", "the break-even point that splits the two groups"),
             ("4", "Does a sentence say what it means for their life?", "Motivation", "\"bad years are rare, but they're the year insurance is for\"")]
    for k, (num, q, tag, ex) in enumerate(items):
        y = 130 + k * 92
        b.append(f'<circle cx="84" cy="{y + 30}" r="22" fill="{HI if k == 3 else A}"/>')
        b.append(t(84, y + 37, num, 20, "white", "bold", "middle"))
        b.append(t(125, y + 26, q, 19, INK, "bold"))
        b.append(t(125, y + 52, f"{tag}: {ex}", 15, SUB))
    b.append(t(60, 510, "Then test it: A/B test the old page against the new one on comprehension, choice quality and trust, not just clicks.", 15, INK, "bold"))
    b.append(source(H, "Questions 1-3 draw on Samek & Sydnor (2020); question 4 is this project's hypothesis."))
    save("fig7_checklist.svg", W, H, b)


for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
    f()
print("figures written to", OUT)

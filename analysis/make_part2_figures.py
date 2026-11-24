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
    W, H = 1100, 660
    be = S("break_even_medical_bills")
    b = header(f"Below {money(be)} in medical bills, Plan A is cheaper. Above it, Plan B is.",
               "Total cost for the year (premiums + your share of medical bills)")
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


# ---------------------------------------------------------------- Figure 4: cheapest premium
def fig4():
    W, H = 1100, 590
    b = header("Showing only the premium works for most people in their 20s, but not all",
               "If everyone aged 22-30 picked the lowest-premium plan: extra cost vs. the plan that would have been cheapest for them")
    raw = f3.share_pct.tolist()
    floors = [int(v) for v in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - floors[i], reverse=True)[:100 - sum(floors)]:
        floors[i] += 1
    labs = ["Under $100", "$100-500", "$500-1,000", "$1,000-2,000", "$2,000-5,000", "$5,000 or more"]
    x0, y0, rowh, unit = 230, 150, 52, 6.0
    b.append(t(x0 - 15, y0 - 12, "Extra cost for the year", 14, SUB, "bold", "end"))
    b.append(t(x0, y0 - 12, "People out of 100", 14, SUB, "bold"))
    for i, (lab, v) in enumerate(zip(labs, floors)):
        y = y0 + i * rowh
        col = HI if i >= 3 else PALE
        b.append(t(x0 - 15, y + 27, lab, 15, INK, "normal", "end"))
        b.append(r(x0, y + 8, v * unit, 30, col, 3))
        b.append(t(x0 + v * unit + 10, y + 29, v, 16, HI if i >= 3 else SUB, "bold"))
    big = sum(floors[3:])
    bxr = x0 + max(floors[3:]) * unit + 50
    b.append(f'<path d="M{bxr} {y0+3*rowh+8} L{bxr+12} {y0+3*rowh+8} L{bxr+12} {y0+6*rowh-6} L{bxr} {y0+6*rowh-6}" fill="none" stroke="{HI}" stroke-width="2"/>')
    b.append(t(760, 190, f"{floors[0]} of 100", 40, SUB, "bold"))
    b.append(t(760, 218, "paid about the same as", 16, INK))
    b.append(t(760, 240, "their cheapest plan", 16, INK))
    b.append(t(760, 345, f"{big} of 100", 40, HI, "bold"))
    b.append(t(760, 373, "paid at least $1,000 more.", 16, INK))
    b.append(t(760, 395, "7 in 10 of them saw a doctor", 16, INK))
    b.append(t(760, 417, "5 or more times that year", 16, INK))
    b.append(t(60, 520, "Lowest-premium plan: a Bronze plan with a $6,700 deductible and a $10,600 out-of-pocket maximum.", 14, SUB))
    b.append(source(H, "MEPS 2023 (ages 22-30, weighted) x 72 plans sold in Allegheny County, 2026 (CMS). Simplified cost model."))
    save("fig4_cheapest_premium.svg", W, H, b)


# ---------------------------------------------------------------- Figure 5: worst case vs cushion
def fig5():
    W, H = 1100, 620
    b = header("Half of young adults couldn't cover a fifth of a typical plan's worst case",
               "The most you could owe in a bad year (out-of-pocket maximum), 2026 plans sold in Allegheny County")
    med = {row.item.split(", ")[1].split(" plans")[0]: row.value for row in f4.itertuples() if "Median" in row.item}
    cant = {row.item.split("ages ")[1]: row.value for row in f4.itertuples() if "Can't" in row.item}
    bars = [(k, med[k]) for k in ["Bronze", "Silver", "Gold", "Platinum"]]
    x0, x1 = 200, 1000
    sc = lambda v: x0 + (x1 - x0) * v / 11000
    xr = sc(2000)
    b.append(r(x0, 170, xr - x0, 270, WARM))
    for i, (lab, v) in enumerate(bars):
        y = 200 + i * 62
        b.append(t(x0 - 15, y + 26, lab, 16, INK, "normal", "end"))
        b.append(r(x0, y + 6, sc(v) - x0, 32, A, 3))
        b.append(r(x0, y + 6, xr - x0, 32, HI, 3))
        b.append(t(sc(v) - 10, y + 28, money(v), 15, "white", "bold", "end"))
    b.append(ln(xr, 165, xr, 450, HI, 2))
    b.append(t(xr, 156, "$2,000", 16, HI, "bold", "middle"))
    for v in [0, 2000, 4000, 6000, 8000, 10000]:
        b.append(t(sc(v), 470, f"${v//1000}k" if v else "$0", 13, SUB, "normal", "middle"))
    b.append(t(60, 520, "About 1 in 2 adults under 35 said they couldn't come up with $2,000 within a month", 16, INK, "bold"))
    b.append(t(60, 544, f"({cant['18-24']:.0f}% of those aged 18-24, {cant['25-34']:.0f}% of those aged 25-34). Orange = that $2,000; blue = the rest of the worst case.", 15, SUB))
    b.append(source(H, "CMS 2026 Pennsylvania plan files (median by metal level); FINRA Foundation NFCS 2024, weighted."))
    save("fig5_worst_case.svg", W, H, b)


# ---------------------------------------------------------------- Figure 6: AFTER
def after_panel(b, x, y, scale=1.0):
    pass


def fig6():
    W, H = 1100, 680
    b = header("What would someone like you actually pay?",
               "The same two plans, shown as yearly totals for people aged 22-30 instead of a table of terms")
    b.append(r(60, 108, 14, 14, A)); b.append(t(82, 120, f"Plan A ({PA.metal_level})", 14, INK))
    b.append(r(230, 108, 14, 14, B)); b.append(t(252, 120, f"Plan B ({PB.metal_level})", 14, INK))
    x0, x1, yt, yb = 140, 640, 185, 500
    sc = lambda v: (yb - yt) * v / 12000
    for v in range(0, 12001, 3000):
        b.append(ln(x0, yb - sc(v), x1, yb - sc(v), GRID if v else "#9ca3af", 1))
        b.append(t(x0 - 10, yb - sc(v) + 5, f"${v//1000}k" if v else "$0", 13, SUB, "normal", "end"))
    b.append(t(30, (yt + yb) / 2, "What you pay for the year (premiums + medical bills)", 14, SUB, "normal", "middle", rotate=-90))
    groups = [("Typical year", "the middle person", S("a_total_typical_p50"), S("b_total_typical_p50")),
              ("Bad year", "the costliest 1 in 10", S("a_total_bad_p90"), S("b_total_bad_p90"))]
    for i, (g, gs, va, vb) in enumerate(groups):
        x = x0 + 60 + i * 230
        for j, (v, col) in enumerate([(va, A), (vb, B)]):
            bx = x + j * 78
            b.append(r(bx, yb - sc(v), 70, sc(v), col))
            b.append(t(bx + 35, yb - sc(v) - 9, money(v), 15, col, "bold", "middle"))
        b.append(t(x + 74, yb + 28, g, 16, INK, "bold", "middle"))
        b.append(t(x + 74, yb + 48, gs, 13, SUB, "normal", "middle"))
    b.append(t((x0 + x1) / 2, yb + 82, "Two kinds of year for a person in their 20s", 14, SUB, "normal", "middle"))
    ka = round(S("share_a_cheaper_pct"))
    b.append(ln(700, 150, 700, 560, GRID, 1))
    b.append(t(745, 200, "Out of 100 people aged 22-30,", 18, INK))
    b.append(t(745, 226, "Plan A would have been cheaper for", 18, INK))
    b.append(t(745, 300, ka, 72, A, "bold"))
    b.append(t(745, 334, "of them", 18, INK))
    for k in range(100):
        b.append(f'<circle cx="{752 + (k % 20) * 15}" cy="{372 + (k // 20) * 18}" r="5.5" fill="{A if k < ka else B}"/>')
    b.append(f'<circle cx="752" cy="482" r="5.5" fill="{A}"/>')
    b.append(t(764, 487, "= 1 person who'd pay less with Plan A", 13, SUB))
    b.append(f'<circle cx="752" cy="504" r="5.5" fill="{B}"/>')
    b.append(t(764, 509, "= 1 person who'd pay less with Plan B", 13, SUB))
    b.append(t(745, 545, f"Worst case: Plan A {money(S('a_worst_case'))}, Plan B {money(S('b_worst_case'))}", 14, INK, "bold"))
    b.append(source(H, SRC_PLANS + "; MEPS 2023, ages 22-30, weighted. Simplified cost model; copays not included."))
    save("fig6_after_what_you_pay.svg", W, H, b)


# ---------------------------------------------------------------- Figure 7: before vs after
def fig7():
    W, H = 1200, 640
    b = header("Same plans, same data. Which page helps someone choose?",
               "Before: the terms of each plan. After: the numbers that answer the user's real question.")
    # BEFORE
    b.append(t(60, 140, "BEFORE", 14, SUB, "bold"))
    b.append(r(60, 150, 520, 400, "white", 10, GRID, 1.5))
    plan_table(b, 75, 170, 490, compact=True)
    b.append(t(80, 470, "The user has to do the math:", 15, INK, "bold"))
    b.append(t(80, 494, "deductibles, coinsurance and an unknown year.", 15, SUB))
    b.append(t(80, 520, "Most people can't (Figure 3).", 15, SUB))
    # arrow
    b.append(f'<path d="M598 350 L630 350 M620 340 L632 350 L620 360" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    # AFTER
    b.append(t(650, 140, "AFTER", 14, HI, "bold"))
    b.append(r(650, 150, 490, 400, "white", 10, HI, 2))
    b.append(t(670, 185, "For people your age (22-30), each year:", 15, INK, "bold"))
    cards = [("Typical year", S("a_total_typical_p50"), S("b_total_typical_p50")),
             ("Bad year (1 in 10)", S("a_total_bad_p90"), S("b_total_bad_p90")),
             ("Worst case", S("a_worst_case"), S("b_worst_case"))]
    for i, (lab, va, vb) in enumerate(cards):
        y = 205 + i * 78
        b.append(r(670, y, 450, 64, "#f9fafb", 8))
        b.append(t(686, y + 38, lab, 15, INK))
        b.append(t(925, y + 30, "Plan A", 12, A, "bold", "middle"))
        b.append(t(925, y + 52, money(va), 18, A, "bold", "middle"))
        b.append(t(1050, y + 30, "Plan B", 12, B, "bold", "middle"))
        b.append(t(1050, y + 52, money(vb), 18, B, "bold", "middle"))
    ka = round(S("share_a_cheaper_pct"))
    b.append(t(670, 470, f"Plan A is cheaper for {ka} of 100 people your age.", 15, INK, "bold"))
    b.append(t(670, 494, f"If you expect more than {money(S('break_even_medical_bills'))} in medical", 15, SUB))
    b.append(t(670, 518, "bills this year, Plan B is likely cheaper.", 15, SUB))
    b.append(t(60, 588, "Design takeaway: lead with the number that's about the user (relevance), show the range (uncertainty), and say who each plan fits (decision impact).", 14, INK))
    b.append(source(H, SRC_PLANS + "; MEPS 2023, ages 22-30, weighted. Draft mockup; simplified cost model."))
    save("fig7_before_after.svg", W, H, b)


for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
    f()
print("figures written to", OUT)

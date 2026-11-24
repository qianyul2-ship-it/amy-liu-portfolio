"""Assemble the Part II storyboard (figures/storyboard.png) from the rendered figures.

Needs PNG renders of the figures in figures/png/ (rsvg-convert -w 1100 figures/X.svg -o figures/png/X.png).
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"
font = lambda size, bold=False: ImageFont.truetype(F.format("Bold" if bold else "Regular"), size)
INK, SUB, BLUE, ORANGE, LINE = (31, 41, 55), (75, 85, 99), (37, 99, 168), (194, 65, 12), (229, 231, 235)

frames = [
    ("1  HOOK", "Which plan would you choose?",
     None, "Title screen. The reader, a product or design person, is asked to play the user for a minute.",
     "Two real Pittsburgh plans follow."),
    ("2  TRY IT", "Pick a plan from the table",
     "fig1_before_plan_table", "The reader sees the plan table most pages use and makes a choice.",
     "Every number is there; the answer isn't."),
    ("3  REVEAL", "The right answer depends on your year",
     "fig2_cost_curves", "Below $2,633 in bills, Plan A wins; above it, Plan B. 70 of 100 people in their 20s fall below.",
     "The table never told them this."),
    ("4  WHY IT'S HARD", "It's not just you",
     "fig3_research", "Only 14% understand the four basic terms; 61% of employees chose a worse plan.",
     "Users can't do the math the table asks of them."),
    ("5  ONE NUMBER ISN'T ENOUGH", "The premium works for most, but not all",
     "fig4_cheapest_premium", "If everyone picks the lowest premium, 27 of 100 pay $1,000+ more.",
     "Different users need different numbers."),
    ("6  WHO NEEDS WHAT", "Can they cover the worst case?",
     "fig5_worst_case", "Half of adults under 35 can't raise $2,000; a typical plan's worst case is $10,600.",
     "For them, the worst case comes first."),
    ("7  REDESIGN", "Show what someone like you would pay",
     "fig6_after_what_you_pay", "Typical year, bad year, and who each plan fits, for people aged 22-30.",
     "Relevance, uncertainty, decision impact."),
    ("8  BEFORE / AFTER + CTA", "Same data, a page that helps people choose",
     "fig7_before_after", "Side by side. Call to action for product teams: lead with the user's number, then A/B test it.",
     "Ends with sources and method notes."),
]

COLS, FW, FH, GAP, M = 4, 560, 600, 36, 70
W = M * 2 + COLS * FW + (COLS - 1) * GAP
H = 230 + 2 * FH + GAP + 80
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
d.text((M, 60), "Storyboard: What Should We Show?", font=font(46, True), fill=INK)
d.text((M, 130), "Audience: product and design people who build pages where users compare complex products. "
       "Eight screens, read top-left to bottom-right.", font=font(24), fill=SUB)

for i, (tag, head, fig, body, punch) in enumerate(frames):
    col, row = i % COLS, i // COLS
    x = M + col * (FW + GAP)
    y = 200 + row * (FH + GAP)
    d.rounded_rectangle([x, y, x + FW, y + FH], 16, outline=LINE, width=3, fill="white")
    d.text((x + 24, y + 22), tag, font=font(20, True), fill=ORANGE if i == 7 else BLUE)
    yy = y + 56
    for ln in textwrap.wrap(head, 30):
        d.text((x + 24, yy), ln, font=font(28, True), fill=INK)
        yy += 36
    box = [x + 24, y + 140, x + FW - 24, y + 420]
    d.rounded_rectangle(box, 10, fill=(249, 250, 251))
    if fig:
        im = Image.open(f"figures/png/{fig}.png").convert("RGB")
        bw, bh = box[2] - box[0] - 16, box[3] - box[1] - 16
        im.thumbnail((bw, bh), Image.LANCZOS)
        img.paste(im, (box[0] + 8 + (bw - im.width) // 2, box[1] + 8 + (bh - im.height) // 2))
    else:
        d.text((box[0] + 30, box[1] + 70), "What Should", font=font(40, True), fill=INK)
        d.text((box[0] + 30, box[1] + 118), "We Show?", font=font(40, True), fill=INK)
        d.text((box[0] + 30, box[1] + 180), "Helping people choose a health plan,", font=font(20), fill=SUB)
        d.text((box[0] + 30, box[1] + 206), "one number at a time", font=font(20), fill=SUB)
    yy = y + 440
    for ln in textwrap.wrap(body, 44):
        d.text((x + 24, yy), ln, font=font(20), fill=INK)
        yy += 27
    d.text((x + 24, y + FH - 44), punch, font=font(20, True), fill=ORANGE if i == 7 else BLUE)
    if col < COLS - 1:
        ax, ay = x + FW + 8, y + FH // 2
        d.polygon([(ax, ay - 12), (ax + 20, ay), (ax, ay + 12)], fill=(156, 163, 175))

d.text((M, H - 60), "Figures are draft high-fidelity charts built from MEPS 2023, CMS 2026 Pennsylvania plan files, FINRA NFCS 2024 "
       "and published research. Simplified cost model; see analysis/.", font=font(20), fill=(156, 163, 175))
img.save("figures/storyboard.png", optimize=True)
print(img.size)

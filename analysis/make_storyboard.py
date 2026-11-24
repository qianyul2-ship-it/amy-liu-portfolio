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

COLS, FW, FH, GAP, M = 2, 1100, 1000, 50, 80
ROWS = (len(frames) + COLS - 1) // COLS
W = M * 2 + COLS * FW + (COLS - 1) * GAP
H = 260 + ROWS * FH + (ROWS - 1) * GAP + 100
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
d.text((M, 60), "Storyboard: What Should We Show?", font=font(64, True), fill=INK)
d.text((M, 150), "Audience: product and design people who build pages where users compare complex products.", font=font(34), fill=SUB)
d.text((M, 196), "Eight screens, read left to right, top to bottom.", font=font(34), fill=SUB)

for i, (tag, head, fig, body, punch) in enumerate(frames):
    col, row = i % COLS, i // COLS
    x = M + col * (FW + GAP)
    y = 270 + row * (FH + GAP)
    d.rounded_rectangle([x, y, x + FW, y + FH], 16, outline=LINE, width=3, fill="white")
    d.text((x + 36, y + 30), tag, font=font(32, True), fill=ORANGE if i == 7 else BLUE)
    yy = y + 80
    for ln in textwrap.wrap(head, 45):
        d.text((x + 36, yy), ln, font=font(46, True), fill=INK)
        yy += 56
    box = [x + 36, y + 160, x + FW - 36, y + 790]
    d.rounded_rectangle(box, 10, fill=(249, 250, 251))
    if fig:
        im = Image.open(f"figures/png/{fig}.png").convert("RGB")
        bw, bh = box[2] - box[0] - 16, box[3] - box[1] - 16
        im.thumbnail((bw, bh), Image.LANCZOS)
        img.paste(im, (box[0] + 8 + (bw - im.width) // 2, box[1] + 8 + (bh - im.height) // 2))
    else:
        d.text((box[0] + 70, box[1] + 170), "What Should", font=font(80, True), fill=INK)
        d.text((box[0] + 70, box[1] + 265), "We Show?", font=font(80, True), fill=INK)
        d.text((box[0] + 70, box[1] + 390), "Helping people choose a health plan,", font=font(38), fill=SUB)
        d.text((box[0] + 70, box[1] + 440), "one number at a time", font=font(38), fill=SUB)
    yy = y + 815
    for ln in textwrap.wrap(body, 62):
        d.text((x + 36, yy), ln, font=font(32), fill=INK)
        yy += 42
    d.text((x + 36, y + FH - 62), punch, font=font(34, True), fill=ORANGE if i == 7 else BLUE)
    if col < COLS - 1:
        ax, ay = x + FW + 10, y + FH // 2
        d.polygon([(ax, ay - 16), (ax + 28, ay), (ax, ay + 16)], fill=(156, 163, 175))

d.text((M, H - 80), "Draft charts built from MEPS 2023, CMS 2026 Pennsylvania plan files, FINRA NFCS 2024 and published research.", font=font(30), fill=(156, 163, 175))
img.save("figures/storyboard.png", optimize=True)
print(img.size)

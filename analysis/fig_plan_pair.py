"""Real numbers for the two-plan figures (Part II).

Run from the repository root:  python analysis/fig_plan_pair.py
Writes data/plan_pair.csv, data/plan_pair_cost_curve.csv and data/plan_pair_summary.csv.

Plan A and Plan B are two real 2026 plans sold in Allegheny County by the same insurer,
on the same provider network, so they differ only in the premium/deductible trade-off.
Premiums are for a 26-year-old in Rating Area 4. Same simplified cost model as
analysis/fig3_fig4.py: deductible, then coinsurance, capped at the out-of-pocket maximum;
copays are ignored.
"""
import numpy as np
import pandas as pd

D = "data/"
plans = pd.read_csv(D + "cms_pa_2026_plans.csv")
rates = pd.read_csv(D + "cms_pa_2026_rates_age22_30.csv")
names = {"A": "UPMC Advantage Bronze $6,700/$0 - Partner Network",
         "B": "UPMC Advantage Gold $1,000/$20 - Partner Network"}
r = rates[(rates.age == 26) & (rates.rating_area == "Rating Area 4")].drop_duplicates("standard_component_id")
pair = (plans[plans.plan_name.isin(names.values())].drop_duplicates("plan_name")
        .merge(r[["standard_component_id", "monthly_premium"]], on="standard_component_id"))
pair["label"] = pair.plan_name.map({v: k for k, v in names.items()})
pair = pair.set_index("label").loc[["A", "B"]]
pair[["plan_name", "metal_level", "plan_type", "monthly_premium", "deductible_individual",
      "coinsurance_pct", "oop_max_individual"]].to_csv(D + "plan_pair.csv")


def total(spend, row):
    s = np.asarray(spend, dtype=float)
    d, c, m = row.deductible_individual, row.coinsurance_pct / 100, row.oop_max_individual
    oop = np.minimum(np.where(s <= d, s, d + c * (s - d)), m)
    return 12 * row.monthly_premium + oop


grid = np.arange(0, 40001, 250)
curve = pd.DataFrame({"medical_bills": grid, "plan_a_total": total(grid, pair.loc["A"]),
                      "plan_b_total": total(grid, pair.loc["B"])})
curve.to_csv(D + "plan_pair_cost_curve.csv", index=False)
diff = curve.plan_a_total - curve.plan_b_total
fine = np.arange(0, 40001, 1)
d_fine = total(fine, pair.loc["A"]) - total(fine, pair.loc["B"])
breakeven = int(fine[np.argmax(d_fine > 0)])

m = pd.read_csv(D + "meps_2023_extract.csv")
y = m[m.AGE23X.between(22, 30) & (m.PERWT23F > 0)]
w = y.PERWT23F.to_numpy()
spend = y.TOTEXP23.to_numpy()


def wq(x, q):
    o = np.argsort(x); cw = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(cw, q)])


ta, tb = total(spend, pair.loc["A"]), total(spend, pair.loc["B"])
rows = {
    "break_even_medical_bills": breakeven,
    "spend_p50": wq(spend, .5), "spend_p75": wq(spend, .75), "spend_p90": wq(spend, .9), "spend_p95": wq(spend, .95),
    "share_spend_above_break_even_pct": round(np.average(spend > breakeven, weights=w) * 100, 1),
    "a_total_typical_p50": round(wq(ta, .5)), "b_total_typical_p50": round(wq(tb, .5)),
    "a_total_bad_p90": round(wq(ta, .9)), "b_total_bad_p90": round(wq(tb, .9)),
    "a_worst_case": round(total(1e9, pair.loc["A"])), "b_worst_case": round(total(1e9, pair.loc["B"])),
    "share_a_cheaper_pct": round(np.average(ta < tb, weights=w) * 100, 1),
    "share_b_cheaper_pct": round(np.average(tb < ta, weights=w) * 100, 1),
}
pd.Series(rows).to_csv(D + "plan_pair_summary.csv", header=["value"])
print(pair[["monthly_premium", "deductible_individual", "coinsurance_pct", "oop_max_individual"]])
for k, v in rows.items():
    print(f"{k}: {v}")

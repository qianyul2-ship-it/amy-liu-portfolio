"""Preliminary numbers for Figures 3 and 4 (Final Project Part I).

Run from the repository root:  python analysis/fig3_fig4.py
Writes data/fig3_overpay_by_premium_rule.csv and data/fig4_worst_case_vs_cushion.csv.

Figure 3 asks: if a person aged 22-30 simply picks the plan with the lowest monthly
premium, how much more do they pay over the year than with the plan that would have
been cheapest for them?

Simplified cost model (to be refined in Part II):
  yearly total = 12 x monthly premium (age 26, Rating Area 4)
               + out-of-pocket cost, where out-of-pocket =
                   spending                         if spending <= deductible
                   deductible + coinsurance x rest  otherwise
                 capped at the out-of-pocket maximum.
  "Spending" is each MEPS respondent's total 2023 medical spending (TOTEXP23).
  Copays, separate drug deductibles and network differences are ignored.
"""
import numpy as np
import pandas as pd

D = "data/"

# --- 2026 plans sold in Allegheny County (Pittsburgh), premiums for age 26 -------------
plans = pd.read_csv(D + "cms_pa_2026_plans.csv")
areas = pd.read_csv(D + "cms_pa_2026_service_areas.csv")
rates = pd.read_csv(D + "cms_pa_2026_rates_age22_30.csv")
alle = areas.loc[areas.county_name == "Allegheny", ["issuer_id", "service_area_id"]].drop_duplicates()
p = plans.merge(alle, on=["issuer_id", "service_area_id"])
p = p[p.metal_level != "Catastrophic"]          # catastrophic plans are age/hardship restricted
r = rates[(rates.age == 26) & (rates.rating_area == "Rating Area 4")]
p = p.merge(r[["standard_component_id", "monthly_premium"]].drop_duplicates("standard_component_id"),
            on="standard_component_id").drop_duplicates("standard_component_id").reset_index(drop=True)

# --- MEPS adults aged 22-30 -------------------------------------------------------------
m = pd.read_csv(D + "meps_2023_extract.csv")
y = m[m.AGE23X.between(22, 30) & (m.PERWT23F > 0)].reset_index(drop=True)
w = y.PERWT23F.to_numpy()

X = y.TOTEXP23.to_numpy()[:, None]
ded = p.deductible_individual.to_numpy()
coin = p.coinsurance_pct.to_numpy() / 100
moop = p.oop_max_individual.to_numpy()
prem = 12 * p.monthly_premium.to_numpy()
oop = np.minimum(np.where(X <= ded, X, ded + coin * (X - ded)), moop)
total = prem + oop
best = total.min(axis=1)

pick = prem.argmin()                              # the lowest-premium plan
overpay = total[:, pick] - best

bins = [-1, 100, 500, 1000, 2000, 5000, np.inf]
labels = ["Under $100", "$100-500", "$500-1,000", "$1,000-2,000", "$2,000-5,000", "$5,000+"]
share = (pd.Series(w).groupby(pd.cut(overpay, bins, labels=labels), observed=False).sum() / w.sum() * 100)
fig3 = share.rename("share_pct").reset_index().rename(columns={"index": "overpaid"})
fig3.columns = ["overpaid", "share_pct"]
fig3.to_csv(D + "fig3_overpay_by_premium_rule.csv", index=False)

print(f"Plans compared: {len(p)} | people aged 22-30: {len(y)}")
print("Lowest-premium plan:", p.loc[pick, ["plan_name", "metal_level", "monthly_premium",
                                         "deductible_individual", "oop_max_individual"]].to_dict())
print(fig3.round(1).to_string(index=False))
print("Weighted mean overpay: $%.0f" % np.average(overpay, weights=w))

# --- Figure 4: worst case vs. what people can raise -------------------------------------
n = pd.read_csv(D + "nfcs_2024_extract.csv")
n = n[n.J20.isin([1, 2, 3, 4])]
age_lab = {1: "18-24", 2: "25-34", 3: "35-44", 4: "45-54", 5: "55-64", 6: "65+"}
cant = (n.assign(cant=n.J20.isin([3, 4]))
          .groupby("A3Ar_w").apply(lambda d: np.average(d.cant, weights=d.wgt_n2) * 100))
oopmed = p.groupby("metal_level").oop_max_individual.median()
rows = [{"item": f"Can't raise $2,000 in a month, ages {age_lab[k]}", "value": round(v, 1), "unit": "percent"}
        for k, v in cant.items()]
rows += [{"item": f"Median out-of-pocket maximum, {lvl} plans (Allegheny County, 2026)", "value": v, "unit": "dollars"}
         for lvl, v in oopmed.items()]
pd.DataFrame(rows).to_csv(D + "fig4_worst_case_vs_cushion.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))

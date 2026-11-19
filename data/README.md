# Data for the final project

All files here are extracts of public datasets, keeping only the variables this project uses. The full original files can be downloaded from the official links below.

| File | What it is | Rows | Used in |
| --- | --- | --- | --- |
| `published_findings.csv` | Key figures recreated from published studies, with population and source | 4 | Figure 2 |
| `meps_2023_extract.csv` | MEPS 2023 person-level medical spending | 18,919 | Figures 1, 3, 5 |
| `cms_pa_2026_plans.csv` | 2026 Pennsylvania individual-market medical plans (standard versions only) | 320 | Figures 1, 5 |
| `cms_pa_2026_rates_age22_30.csv` | Monthly premiums for those plans, ages 22–30, by rating area | 7,281 | Figures 1, 5 |
| `cms_pa_2026_service_areas.csv` | Which counties each issuer's service area covers (to find plans sold in Allegheny County) | 1,175 | Figures 1, 5 |
| `fig3_overpay_by_premium_rule.csv` | Output for Figure 3: share of people aged 22–30 by how much more they'd pay with the lowest-premium plan | 6 | Figure 3 |
| `fig4_worst_case_vs_cushion.csv` | Output for Figure 4: share who can't raise $2,000 by age; median out-of-pocket maximum by metal level | 11 | Figure 4 |
| `nfcs_2024_extract.csv` | 2024 National Financial Capability Study respondents | 25,539 | Figure 4 |

The output files are produced by [`analysis/fig3_fig4.py`](../analysis/fig3_fig4.py); run it from the repository root.

## Sources

| Dataset | Official download |
| --- | --- |
| MEPS 2023 Full Year Consolidated File (HC-251), Agency for Healthcare Research and Quality | https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-251 |
| CMS State-Based Marketplace Public Use Files, Pennsylvania, plan year 2026 | https://www.cms.gov/marketplace/resources/data/state-based-public-use-files |
| FINRA Investor Education Foundation, National Financial Capability Study 2024 (State-by-State) | https://www.finrafoundation.org/nfcs-data-and-downloads |

## Data dictionary

### `meps_2023_extract.csv`

| Column | Meaning |
| --- | --- |
| `DUPERSID` | Person ID |
| `AGE23X` | Age at end of 2023 |
| `PERWT23F` | Person weight (use for all population estimates) |
| `VARSTR`, `VARPSU` | Survey design variables for standard errors |
| `INSCOV23` | Insurance coverage in 2023 (1 = any private, 2 = public only, 3 = uninsured) |
| `PRVEV23` | Ever had private insurance in 2023 (1 = yes, 2 = no) |
| `POVCAT23` | Family income as % of poverty line (1 = poor … 5 = high income) |
| `TOTEXP23` | Total medical spending in 2023, all payers ($) |
| `TOTSLF23` | Amount paid out of pocket by the person or family ($) |
| `TOTPRV23` | Amount paid by private insurance ($) |
| `OBTOTV23` | Number of office-based visits |
| `ERTOT23` | Number of emergency room visits |
| `IPDIS23` | Number of hospital discharges (inpatient stays) |

### `cms_pa_2026_plans.csv`

| Column | Meaning |
| --- | --- |
| `plan_id` | Plan variant ID (standard on-exchange version) |
| `standard_component_id` | Plan ID used to join with the rates file |
| `issuer_id` | Insurance company ID |
| `plan_name`, `metal_level`, `plan_type`, `hsa_eligible`, `service_area_id` | Plan description |
| `deductible_individual` | In-network individual deductible ($). Combined medical + drug when `deductible_source` says so; otherwise the medical deductible |
| `drug_deductible_individual` | Separate drug deductible ($), when the plan has one |
| `coinsurance_pct` | In-network coinsurance after the deductible (%) |
| `oop_max_individual` | In-network individual out-of-pocket maximum ($) |
| `deductible_source` | Whether the plan has one combined deductible or separate medical and drug deductibles |

### `cms_pa_2026_rates_age22_30.csv`

| Column | Meaning |
| --- | --- |
| `standard_component_id` | Joins to `cms_pa_2026_plans.csv` |
| `rating_area` | Pennsylvania rating area (premiums vary by region) |
| `age` | Age of the enrollee (22–30) |
| `tobacco` | Tobacco rating rule |
| `monthly_premium` | Full monthly premium before any subsidy ($) |

### `cms_pa_2026_service_areas.csv`

| Column | Meaning |
| --- | --- |
| `issuer_id`, `service_area_id` | Join to `cms_pa_2026_plans.csv` on both columns |
| `service_area_name` | Issuer's name for the service area |
| `covers_entire_state` | Whether the service area is statewide |
| `county_name` | County covered |
| `partial_county` | Whether only part of the county is covered |

### `nfcs_2024_extract.csv`

| Column | Meaning |
| --- | --- |
| `NFCSID` | Respondent ID |
| `STATEQ` | State |
| `A3Ar_w` | Age group (1 = 18–24, 2 = 25–34, 3 = 35–44, 4 = 45–54, 5 = 55–64, 6 = 65+) |
| `A8_2021` | Household income band (1 = under $15k … 10 = $300k+; 98/99 = don't know / prefer not to say) |
| `A11` | Number of financially dependent children |
| `A9` | Employment status |
| `H1` | Covered by health insurance (1 = yes, 2 = no) |
| `H30_3` | In the last 12 months, had a medical problem but did not see a doctor because of cost (1 = yes, 2 = no) |
| `J5` | Has rainy-day funds to cover 3 months of expenses (1 = yes, 2 = no) |
| `J20` | Confidence in coming up with $2,000 within a month (1 = certain could … 4 = certain could not) |
| `wgt_n2` | National weight (use for national estimates) |
| `wgt_s3` | State weight (use for state estimates) |

Codes 98 and 99 mean "don't know" and "prefer not to say" throughout the NFCS file.

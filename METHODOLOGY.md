# Methodology: last-year Re-TRAC shipments vs mileage-plus-population

Question: Do last year’s Re-TRAC county-to-facility shipments beat a mileage-plus-population assignment on held-out quarters?

## Label

Rows: Indiana origin county × receiving facility × calendar quarter.

Tons: sum of Municipal Solid Waste, Construction/Demolition, Foundry, Coal Ash, Flue Gas Desulfurization Waste, Other Non-Municipal, and Alternate Daily Cover/Reuse received that quarter from that Indiana county. Types stay pooled. A type table is a footnote, not a second tree.

Out-of-state origin is dropped from the lead and counted in the footnote. Unmatched county names fail closed.

## Stream

Public IDEM quarterly waste-received XLSX, 2021 through 2025. The science lock is that file, not a live Re-TRAC Connect login.

Facility coordinates: IndianaMap authorized operating solid waste facilities, name-matched. If the GIS name is missing, the host-county centroid from the facility ID prefix `XX-YY`.

Origin population: 2020 Census `ESTIMATESBASE2020`, frozen. Not holdout-year ACS.

## Contestant

Last year, same quarter: `last_ijq = tons_{i,j,q-4}`. Same origin, same facility, four quarters earlier. Not a calendar-year total.

A holdout cell is scored against last year only when last year is also present.

## Bar

For each origin-quarter with an observed total `T_iq`, split tons across train-era Indiana facilities J with weights

`w_ij = pop_i / (miles_ij + ε)` with `ε = 1` mile.

`miles_ij`: great-circle miles from origin county centroid to facility coordinates. Road miles is a sequel.

Assignment: `hat_ijq = T_iq * w_ij / sum_{k in J} w_ik`.

Facility set J: Indiana facilities that received Indiana-origin tons in train (2021 Q1 through 2023 Q4). Holdout and confirmation do not add a destination to the bar. A new 2024 facility gets bar mass 0.

Origin population is in the numerator of every destination for a fixed origin, so it cancels inside a single county’s shares. For one origin this bar is inverse-miles. The name stays mileage-plus-population as locked; the miles term is the assignment.

## Split

Primary window: 2021 Q1 through 2025 Q4.

| Block | Quarters | Role |
|-------|----------|------|
| Train | 2021 Q1 through 2023 Q4 | Facility set J. Not a fit. |
| Holdout | 2024 Q1 through 2024 Q4 | Product. Last year is 2023. |
| Confirmation | 2025 Q1 through 2025 Q4 | Out of train and out of J. Cannot reverse the holdout. |

## Metrics

Lead with holdout RMSE in tons on the origin-facility-quarter cells that both last year and the bar can score (intersection: last year present). MAE second. Per-county table required. A 7/N last-year-closer count is not the method.

Also print origin-total RMSE. Last year can miss the county total. The bar cannot: it is scaled to the observed origin-quarter total, so origin-total bar RMSE is 0 by construction.

Win: last-year RMSE strictly less than mileage-pop RMSE on that intersection. Bar RMSE on all reported holdout cells is a second line.

## Figures

1. Holdout scatter: last year and the bar vs observed tons on the intersection, 1:1. Caption: tons of error, not a landfill siting.
2. Per-county RMSE bars for the largest origins. Caption: county error, not a hauling route.

Two figures max.

## Fixture

Synthetic counties and facilities with planted last-year persistence. Fixture skill does not rescue live.

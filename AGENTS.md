# Agent notes: indiana_retrac_last_year

Public GitHub. MIT. Question: Do last year’s Re-TRAC county-to-facility shipments beat a mileage-plus-population assignment on held-out quarters?

Live lock `5800fc3`: two answers. Last year wins the assignment (6504.7 vs 16633.0 on 4370 cells). Last year loses the county total (23313.3 vs 0.0). Do not average it. Origin-total bar RMSE is 0 by construction, not a counter-finding. Do not restamp `5800fc3`. Stay off winter Pages. This tree is last-year assignment, not a CPC row and not a truck route.

Contestant is last year, same quarter. Bar is origin population over great-circle miles. Origin population cancels inside each county’s shares; the miles term is the assignment. Ridge and HGB stay off this tree. Confirmation 2025 is out of train and out of facility set J. The science lock is the public IDEM quarterly XLSX, not `app.re-trac.com`. Empty XLSX, unmatched origin county, or missing facility coordinates stop (`run_live.py` exit 2). Two figures max. Stay off `indiana_wx_pages`. Do not add a winter-page ledger row. Do not restamp frozen weather SHAs (`ac36f0f`, `1416da1`, `6b47f21`, `9aa7935`, `28941fb`, `a95a16b`).

`retracforge/` is the GraphForge pin.

Readable lock is this README. Index gist `66b896b0` lists Re-TRAC. Lane gist `1b6d686320adea674727af588e77bf80`. Stay off Site / `indiana_wx_pages`.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

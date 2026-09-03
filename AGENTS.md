# Agent notes: indiana_retrac_last_year

Public GitHub. MIT. Question: Do last year’s Re-TRAC county-to-facility shipments beat a mileage-plus-population assignment on held-out quarters?

Live lock `5800fc3`: holdout last-year RMSE 6504.7 tons vs mileage-plus-population 16633.0 on cells where last year is present (yes). Last year origin-total RMSE 23313.3 vs 0.0 for the bar. Do not average it.

Contestant is last year, same quarter. Bar is origin population over great-circle miles. Origin population cancels inside each county’s shares; the miles term is the assignment. Ridge and HGB stay off this tree. Confirmation 2025 is out of train and out of facility set J. The science lock is the public IDEM quarterly XLSX, not `app.re-trac.com`. Empty XLSX, unmatched origin county, or missing facility coordinates stop (`run_live.py` exit 2). Two figures max. Stay off `indiana_wx_pages`. Do not add a winter-page ledger row. Do not restamp frozen weather SHAs (`ac36f0f`, `1416da1`, `6b47f21`, `9aa7935`, `28941fb`, `a95a16b`).

`retracforge/` is the GraphForge pin.

Readable index is this repo README. Gist `66b896b0` stays the weather pointer.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

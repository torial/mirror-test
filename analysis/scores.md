# Judge-pass scores

*Judges: claude-sonnet-5, claude-haiku-4-5. Axes scored only on runs the judge coded E2+. Means are over all axis scores from both judges. Human adjudication required on 2-point splits (queue at bottom).*

E-code agreement (exact): 24/40 runs

| model | E-codes (both judges) | specificity | consistency | discriminability | stability | calibration |
|---|---|---|---|---|---|---|
| claude-fable-5 | E3:4, E4:16 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |
| claude-haiku-4-5 | E2:1, E3:9, E4:10 | 2.00 | 1.60 | 1.60 | 1.75 | 1.85 |
| claude-opus-4-8 | E3:14, E4:6 | 2.00 | 1.95 | 1.70 | 1.95 | 2.00 |
| claude-sonnet-4-6 | E3:15, E4:5 | 2.00 | 1.80 | 1.20 | 1.90 | 2.00 |

## Adjudication queue (3 items)

- claude-haiku-4-5 OM run01 **stability**: claude-haiku-4-5=2 vs claude-sonnet-5=0
- claude-haiku-4-5 OM run01 **calibration**: claude-haiku-4-5=2 vs claude-sonnet-5=0
- claude-haiku-4-5 OM run03 **stability**: claude-haiku-4-5=2 vs claude-sonnet-5=0

## Final adjudicated axis means

| model | specificity | consistency | discriminability | stability | calibration |
|---|---|---|---|---|---|
| claude-fable-5 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |
| claude-haiku-4-5 | 2.00 | 1.60 | 1.60 | 1.75 | 1.85 |
| claude-opus-4-8 | 2.00 | 1.95 | 1.70 | 1.95 | 2.00 |
| claude-sonnet-4-6 | 2.00 | 1.80 | 1.20 | 1.90 | 2.00 |

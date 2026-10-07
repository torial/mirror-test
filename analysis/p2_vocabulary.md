# P2 test — menu-vocabulary import into Part 1

*Rates are menu-distinctive term hits per 1,000 words of Part 1 assistant text. O->M Part 1 precedes the menu (baseline); M->O Part 1 follows it (import).*

| model | O->M mean | M->O mean | ratio | verdict |
|---|---|---|---|---|
| claude-fable-5 | 0.46 | 0.97 | 2.1x | import |
| claude-haiku-4-5 | 0.19 | 1.51 | 7.9x | import |
| claude-opus-4-8 | 0.50 | 0.87 | 1.8x | weak |
| claude-sonnet-4-6 | 0.54 | 0.50 | 0.9x | none |

**Overall: O->M 0.42 vs M->O 0.96 per 1k words (2.3x).**

Per-run detail:

- claude-fable-5 OM run01: 0.62/1k (4 hits / 6477 words)
- claude-fable-5 OM run02: 0.79/1k (5 hits / 6316 words)
- claude-fable-5 OM run03: 0.37/1k (2 hits / 5446 words)
- claude-fable-5 OM run04: 0.18/1k (1 hits / 5555 words)
- claude-fable-5 OM run05: 0.32/1k (2 hits / 6274 words)
- claude-fable-5 MO run01: 1.40/1k (9 hits / 6409 words)
- claude-fable-5 MO run02: 1.83/1k (12 hits / 6544 words)
- claude-fable-5 MO run03: 0.15/1k (1 hits / 6472 words)
- claude-fable-5 MO run04: 0.73/1k (5 hits / 6816 words)
- claude-fable-5 MO run05: 0.72/1k (5 hits / 6986 words)
- claude-haiku-4-5 OM run01: 0.00/1k (0 hits / 1878 words)
- claude-haiku-4-5 OM run02: 0.00/1k (0 hits / 1867 words)
- claude-haiku-4-5 OM run03: 0.00/1k (0 hits / 1765 words)
- claude-haiku-4-5 OM run04: 0.53/1k (1 hits / 1872 words)
- claude-haiku-4-5 OM run05: 0.42/1k (1 hits / 2387 words)
- claude-haiku-4-5 MO run01: 1.29/1k (15 hits / 11623 words)
- claude-haiku-4-5 MO run02: 0.73/1k (6 hits / 8198 words)
- claude-haiku-4-5 MO run03: 2.59/1k (24 hits / 9258 words)
- claude-haiku-4-5 MO run04: 1.65/1k (17 hits / 10304 words)
- claude-haiku-4-5 MO run05: 1.29/1k (10 hits / 7725 words)
- claude-opus-4-8 OM run01: 0.25/1k (1 hits / 4046 words)
- claude-opus-4-8 OM run02: 0.23/1k (1 hits / 4289 words)
- claude-opus-4-8 OM run03: 0.79/1k (4 hits / 5062 words)
- claude-opus-4-8 OM run04: 0.50/1k (2 hits / 4015 words)
- claude-opus-4-8 OM run05: 0.72/1k (3 hits / 4155 words)
- claude-opus-4-8 MO run01: 1.12/1k (8 hits / 7152 words)
- claude-opus-4-8 MO run02: 0.98/1k (7 hits / 7114 words)
- claude-opus-4-8 MO run03: 0.51/1k (4 hits / 7888 words)
- claude-opus-4-8 MO run04: 1.23/1k (9 hits / 7292 words)
- claude-opus-4-8 MO run05: 0.53/1k (3 hits / 5700 words)
- claude-sonnet-4-6 OM run01: 0.59/1k (2 hits / 3363 words)
- claude-sonnet-4-6 OM run02: 0.30/1k (1 hits / 3290 words)
- claude-sonnet-4-6 OM run03: 0.75/1k (2 hits / 2661 words)
- claude-sonnet-4-6 OM run04: 0.53/1k (2 hits / 3750 words)
- claude-sonnet-4-6 OM run05: 0.49/1k (2 hits / 4055 words)
- claude-sonnet-4-6 MO run01: 0.26/1k (2 hits / 7792 words)
- claude-sonnet-4-6 MO run02: 0.23/1k (2 hits / 8601 words)
- claude-sonnet-4-6 MO run03: 1.00/1k (9 hits / 9012 words)
- claude-sonnet-4-6 MO run04: 0.49/1k (4 hits / 8184 words)
- claude-sonnet-4-6 MO run05: 0.51/1k (4 hits / 7917 words)
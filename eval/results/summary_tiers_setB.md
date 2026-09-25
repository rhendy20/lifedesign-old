# Eval summary

Scores are blind (labels stripped, pooled per persona). Cost is CLI list-price basis incl. CLI overhead.

## By condition

| condition | set | insights | depth≥3 | mean depth | hit recall | hit share | FP rate | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v3__cheap | c7c379d2 | 82 | 52% | 2.38 | 56% | 39% | 13% | 96% | 0.153 | 212 |
| v3__mid | c7c379d2 | 80 | 62% | 2.60 | 54% | 40% | 4% | 100% | 0.216 | 121 |

## By archetype

| condition | archetype | insights | depth≥3 | hit share | FP rate |
|---|---|---|---|---|---|
| v3__cheap | cliche | 9 | 44% | 33% | 0% |
| v3__cheap | different_life_shape | 25 | 52% | 44% | 16% |
| v3__cheap | mundane | 8 | 38% | 38% | 38% |
| v3__cheap | near_founder_control | 7 | 71% | 57% | 0% |
| v3__cheap | self_aware | 8 | 75% | 38% | 12% |
| v3__cheap | stated_vs_lived_contradiction | 8 | 25% | 12% | 25% |
| v3__cheap | withholder | 9 | 56% | 44% | 0% |
| v3__cheap | young_thin_corpus | 8 | 62% | 38% | 12% |
| v3__mid | cliche | 7 | 71% | 57% | 0% |
| v3__mid | different_life_shape | 26 | 77% | 46% | 4% |
| v3__mid | mundane | 7 | 71% | 43% | 14% |
| v3__mid | near_founder_control | 9 | 56% | 33% | 11% |
| v3__mid | self_aware | 7 | 57% | 29% | 0% |
| v3__mid | stated_vs_lived_contradiction | 9 | 33% | 11% | 0% |
| v3__mid | withholder | 7 | 57% | 43% | 0% |
| v3__mid | young_thin_corpus | 8 | 50% | 50% | 0% |

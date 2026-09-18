# Eval summary

Scores are blind (labels stripped, pooled per persona). Cost is CLI list-price basis incl. CLI overhead.

## By condition

| condition | set | insights | depth≥3 | mean depth | hit recall | hit share | FP rate | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v0__mid | 5b4b1cb0 | 266 | 24% | 1.91 | 74% | 25% | 5% | 0% | 0.018 | 12 |
| v1__mid | 5b4b1cb0 | 75 | 75% | 2.76 | 58% | 52% | 0% | 68% | 0.145 | 67 |
| v2__mid | 5b4b1cb0 | 90 | 79% | 2.87 | 52% | 38% | 4% | 100% | 0.185 | 97 |

## By archetype

| condition | archetype | insights | depth≥3 | hit share | FP rate |
|---|---|---|---|---|---|
| v0__mid | cliche | 28 | 43% | 36% | 0% |
| v0__mid | different_life_shape | 84 | 14% | 27% | 4% |
| v0__mid | mundane | 25 | 32% | 16% | 12% |
| v0__mid | near_founder_control | 26 | 54% | 27% | 4% |
| v0__mid | self_aware | 28 | 32% | 32% | 7% |
| v0__mid | stated_vs_lived_contradiction | 30 | 3% | 10% | 10% |
| v0__mid | withholder | 26 | 23% | 27% | 4% |
| v0__mid | young_thin_corpus | 19 | 5% | 21% | 0% |
| v1__mid | cliche | 9 | 89% | 67% | 0% |
| v1__mid | different_life_shape | 22 | 68% | 45% | 0% |
| v1__mid | mundane | 8 | 88% | 38% | 0% |
| v1__mid | near_founder_control | 7 | 71% | 43% | 0% |
| v1__mid | self_aware | 7 | 86% | 86% | 0% |
| v1__mid | stated_vs_lived_contradiction | 7 | 29% | 14% | 0% |
| v1__mid | withholder | 8 | 88% | 62% | 0% |
| v1__mid | young_thin_corpus | 7 | 86% | 71% | 0% |
| v2__mid | cliche | 9 | 89% | 22% | 11% |
| v2__mid | different_life_shape | 26 | 73% | 46% | 8% |
| v2__mid | mundane | 9 | 89% | 44% | 0% |
| v2__mid | near_founder_control | 9 | 100% | 22% | 0% |
| v2__mid | self_aware | 9 | 78% | 67% | 0% |
| v2__mid | stated_vs_lived_contradiction | 10 | 50% | 10% | 10% |
| v2__mid | withholder | 9 | 89% | 22% | 0% |
| v2__mid | young_thin_corpus | 9 | 78% | 56% | 0% |

# Eval summary

Scores are blind (labels stripped, pooled per persona). Cost is CLI list-price basis incl. CLI overhead.

## By condition

| condition | set | insights | depth≥3 | mean depth | hit recall | hit share | FP rate | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v0__mid | 50d0a4d5 | 266 | 22% | 1.92 | 74% | 27% | 5% | 0% | 0.018 | 12 |
| v1__mid | 50d0a4d5 | 75 | 76% | 2.80 | 60% | 52% | 0% | 68% | 0.145 | 67 |
| v2__mid | 50d0a4d5 | 90 | 77% | 2.86 | 58% | 44% | 2% | 100% | 0.185 | 97 |
| v3__mid | 50d0a4d5 | 80 | 76% | 2.84 | 58% | 46% | 2% | 100% | 0.216 | 121 |

## By archetype

| condition | archetype | insights | depth≥3 | hit share | FP rate |
|---|---|---|---|---|---|
| v0__mid | cliche | 28 | 29% | 32% | 0% |
| v0__mid | different_life_shape | 84 | 23% | 35% | 4% |
| v0__mid | mundane | 25 | 28% | 16% | 4% |
| v0__mid | near_founder_control | 26 | 31% | 19% | 4% |
| v0__mid | self_aware | 28 | 25% | 25% | 7% |
| v0__mid | stated_vs_lived_contradiction | 30 | 10% | 10% | 10% |
| v0__mid | withholder | 26 | 15% | 31% | 12% |
| v0__mid | young_thin_corpus | 19 | 11% | 42% | 5% |
| v1__mid | cliche | 9 | 89% | 67% | 0% |
| v1__mid | different_life_shape | 22 | 55% | 45% | 0% |
| v1__mid | mundane | 8 | 88% | 50% | 0% |
| v1__mid | near_founder_control | 7 | 71% | 43% | 0% |
| v1__mid | self_aware | 7 | 86% | 71% | 0% |
| v1__mid | stated_vs_lived_contradiction | 7 | 71% | 14% | 0% |
| v1__mid | withholder | 8 | 100% | 62% | 0% |
| v1__mid | young_thin_corpus | 7 | 86% | 71% | 0% |
| v2__mid | cliche | 9 | 67% | 56% | 0% |
| v2__mid | different_life_shape | 26 | 69% | 50% | 4% |
| v2__mid | mundane | 9 | 89% | 56% | 0% |
| v2__mid | near_founder_control | 9 | 89% | 22% | 0% |
| v2__mid | self_aware | 9 | 78% | 44% | 0% |
| v2__mid | stated_vs_lived_contradiction | 10 | 70% | 10% | 10% |
| v2__mid | withholder | 9 | 78% | 22% | 0% |
| v2__mid | young_thin_corpus | 9 | 89% | 89% | 0% |
| v3__mid | cliche | 7 | 100% | 57% | 0% |
| v3__mid | different_life_shape | 26 | 77% | 42% | 0% |
| v3__mid | mundane | 7 | 71% | 43% | 0% |
| v3__mid | near_founder_control | 9 | 78% | 44% | 11% |
| v3__mid | self_aware | 7 | 86% | 29% | 0% |
| v3__mid | stated_vs_lived_contradiction | 9 | 67% | 33% | 0% |
| v3__mid | withholder | 7 | 86% | 57% | 0% |
| v3__mid | young_thin_corpus | 8 | 50% | 75% | 12% |

# Eval summary

Scores are blind (labels stripped, pooled per persona). Cost is CLI list-price basis incl. CLI overhead.

## By condition

| condition | set | insights | depth≥3 | mean depth | hit recall | hit share | FP rate | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v3__cheap | 0dcb6f16 | 25 | 44% | 2.36 | 53% | 40% | 8% | 100% | 0.143 | 200 |
| v3__fable | 0dcb6f16 | 29 | 93% | 3.14 | 80% | 52% | 0% | 100% | 2.006 | 332 |
| v3__mid | 0dcb6f16 | 25 | 52% | 2.52 | 33% | 32% | 0% | 100% | 0.198 | 113 |

## By archetype

| condition | archetype | insights | depth≥3 | hit share | FP rate |
|---|---|---|---|---|---|
| v3__cheap | different_life_shape | 8 | 50% | 62% | 0% |
| v3__cheap | stated_vs_lived_contradiction | 8 | 25% | 12% | 12% |
| v3__cheap | withholder | 9 | 56% | 44% | 11% |
| v3__fable | different_life_shape | 9 | 100% | 67% | 0% |
| v3__fable | stated_vs_lived_contradiction | 10 | 90% | 40% | 0% |
| v3__fable | withholder | 10 | 90% | 50% | 0% |
| v3__mid | different_life_shape | 9 | 44% | 44% | 0% |
| v3__mid | stated_vs_lived_contradiction | 9 | 56% | 11% | 0% |
| v3__mid | withholder | 7 | 57% | 43% | 0% |

# Canon fold -- REQUIREMENTS.md (incC, incL, incK, incX)

Base head a732c34. Rows appended to the canon table; ids taken from each `01-requirements.md` (current text, ledger amendments included).

## Rows added (file count = id-defining headings/bullets, equal in every case)

| Increment | Rows added | In requirement file | Withdrawn |
|---|---|---|---|
| 2026-11-01-v3-incC | 74 (6 HLR, 68 LLR) | 74 | 0 |
| 2026-11-01-v3-incL | 76 (6 HLR, 70 LLR) | 76 | 1 (LLR-4304.16) |
| 2026-11-01-v3-incK | 224 (9 HLR, 215 LLR) | 224 | 9 (LLR-4403.30, 4403.31, 4407.26, 4407.30-4407.34, 4408.14: 9 ids) |
| 2026-11-01-v3-incX | 48 (6 HLR, 42 LLR) | 48 | 0 |

Total 422 rows; 10 withdrawn. Duplicate ids in the canon: 0 (`sort | uniq -d`).

## Supersessions (ruling 20, LED-2026-11-01-incX.8): 9 rows, Status only

HLR-2404, LLR-2404.1, HLR-2903, LLR-2903.1, LLR-3107.5, LLR-1803.3: `superseded by HLR-4504` (LLR-1803.3 keeps its earlier status note in parentheses).
HLR-2607: export clause only (deck legend carries it through LLR-4502.5). LLR-1905.1, LLR-2104.1: only their removed SVG/PNG export clauses.
The incC, incL and incK ledgers name no supersession of existing canon ids.

## trace_check output

```
CASE   no 02-test-cases.md beside .dev-flow/2026-11-01-v3-incC/01-requirements.md
CASE   no 02-test-cases.md beside .dev-flow/2026-11-01-v3-incK/01-requirements.md
CASE   no 02-test-cases.md beside .dev-flow/2026-11-01-v3-incL/01-requirements.md
CASE   no 02-test-cases.md beside .dev-flow/2026-11-01-v3-incX/01-requirements.md
trace_check: 4 US, 412 active requirements (10 withdrawn), 4 gap(s)
```
(rerun after the status edits above; exit 1 from the four CASE lines only. incX's CASE line is expected to clear once its 02-test-cases.md lands.)

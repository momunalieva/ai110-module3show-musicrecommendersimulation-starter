# AI Interactions Log

## Agentic Workflow (SF8)

**User task:** “do every step do not skip any” and “do all needed,” with screenshots of Phases 1–5 and optional challenges.

**Design instructions formulated during the work:**

- Generate eight fictional songs using the existing CSV headers and previously absent genres and moods.
- Compare genre versus mood weighting and reward proximity to a target energy.
- Add five attributes absent from the baseline, make their preferences opt-in, and keep baseline evaluation reproducible.
- Penalize each candidate by 1.5 per already-selected song by its artist and 0.75 per already-selected song of its genre; recompute after every selection and explain the subtraction.
- Print a readable ASCII table including song, final score, and all reasons.

**AI-generated changes:** CSV expansion and five new columns; CSV type conversion; explainable scoring; both object and dictionary APIs; CLI mode/advanced/diversity/table options; tests; README; Model Card; actual CLI captures.

**Agent verification:** checked the 18-row catalog, numeric types, scoring arithmetic, ranking reversal, stable ties, nonmutation, edge cases, object/dictionary agreement, acoustic bonus, advanced contributions, diversity behavior, and combined CLI flags. All 18 tests passed. Twelve CLI configurations each executed five profiles. Dependency consistency and whitespace checks passed.

**Student manual verification:** not reported. The student should review the code, the reflection draft, and at least one profile against their own musical intuition. Automated checks must not be described as student manual testing.

**Problems corrected:** the starter module import failed under `python -m src.main`; changed it to a package-relative import. Starter tests could pass placeholders, so meaningful scoring and ranking tests were added. The first repository's dependencies were initially installed for DocuBot rather than this project; a separate music-project environment was then created and validated.

## Design Pattern (SF10)

**Pattern:** configuration-based Strategy, chosen in this AI-assisted session. The design question was how to switch genre-first, mood-first, and energy-focused ranking without duplicating the scoring algorithm.

`SCORING_MODES` in `src/recommender.py` stores named weight configurations. `src/main.py` selects one through `--mode` and passes its weights into the common engine. A separate class hierarchy was unnecessary because these strategies differ only in weights. The existing `--experiment` selects energy-focused weights for reproducibility.

**Verification:** tests demonstrate a mood-first ranking change and preserve the original genre-first results. All three modes were exercised with baseline, advanced, diversity, and combined table configurations.

No independent chat sessions or student manual actions were fabricated. Design and evaluation discussions took place in the current chat.

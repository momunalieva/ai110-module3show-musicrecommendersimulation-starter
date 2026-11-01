# Model Card: VibeFinder 1.0

## 1. Model Name
VibeFinder 1.0 — an explainable weighted-score music simulation.

## 2. Intended Use
Classroom exploration of content-based recommendation for users who can supply a favorite genre, mood, target energy, and optional acoustic preference. Not a production service or a trained predictive model. Scores are not probabilities.

## 3. How the Model Works
Every song earns two points for matching the favorite genre and one and a half for matching the mood. Energy earns up to one point: closer to the user's target means a higher score. Acoustic listeners receive an additional bonus proportional to acousticness, up to half a point. All songs are scored, sorted from highest to lowest, and the top five are returned with their reasons. Equal scores keep catalog order. CSV loading, numeric conversions, scoring, ranking, explanations, and shared object-based behavior replace the starter placeholders.

## 4. Data
The initial catalog had 10 songs. Eight fictional AI-generated rows were added, preserving the original rows and all eleven columns, for 18 songs total. There are 15 genres and 14 moods; lofi has three songs and pop two, while each other genre has one. New genres are folk, blues, salsa, classical, hip hop, rnb, metal, and reggae, with eight previously absent moods. The added feature values are invented for classroom use, not derived from recorded audio. No listening behavior, lyrics, language, or listener satisfaction labels are available.

## 5. Strengths
The system produces reproducible and inspectable outputs. Matching profiles select Sunrise City for happy pop, Library Rain for chill lofi, and Storm Runner for intense rock. Numeric closeness rewards a target rather than maximizing energy. Dictionary and object interfaces use the same score, and tests check their agreement.

## 6. Limitations and Bias
In the happy-pop experiment, Gym Hero initially outranks Rooftop Lights despite missing the happy mood, showing that the genre weight can override a useful mood match. Exact labels treat indie pop as unrelated to pop, encouraging a filter bubble around the preferred genre. K-pop is missing, so that profile receives mood-and-energy substitutes instead of genre matches. Sparse coverage, synthetic features, and input-order ties limit variety, while fixed energy distance assumes all listeners experience differences similarly. There is no listener feedback or ground truth to establish recommendation accuracy.

## 7. Evaluation
The CLI was run for three distinct ordinary profiles and two adversarial cases: high-energy sad pop and an absent genre. The design discussion and edge-case brainstorming happened in the current chat rather than a separate session. Conflicting preferences expose the tradeoff between category weights; an absent genre tests fallback behavior without errors. These outputs are actual captured terminal results.

### High-Energy Pop

```text
User profile: High-Energy Pop
Preferences: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.8, 'likes_acoustic': False}
Top recommendations:
1. Sunrise City — Neon Echo | Score: 4.48
   Because: genre match (+2.00); mood match (+1.50); energy closeness (+0.98; song 0.82, target 0.80)
2. Gym Hero — Max Pulse | Score: 2.87
   Because: genre match (+2.00); energy closeness (+0.87; song 0.93, target 0.80)
3. Rooftop Lights — Indigo Parade | Score: 2.46
   Because: mood match (+1.50); energy closeness (+0.96; song 0.76, target 0.80)
4. Concrete Resolve — Verse Atlas | Score: 0.95
   Because: energy closeness (+0.95; song 0.85, target 0.80)
5. Night Drive Loop — Neon Echo | Score: 0.95
   Because: energy closeness (+0.95; song 0.75, target 0.80)
```

### Chill Lofi

```text
User profile: Chill Lofi
Preferences: {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.35, 'likes_acoustic': True}
Top recommendations:
1. Library Rain — Paper Lanterns | Score: 4.93
   Because: genre match (+2.00); mood match (+1.50); energy closeness (+1.00; song 0.35, target 0.35); acoustic preference (+0.43)
2. Midnight Coding — LoRoom | Score: 4.79
   Because: genre match (+2.00); mood match (+1.50); energy closeness (+0.93; song 0.42, target 0.35); acoustic preference (+0.35)
3. Focus Flow — LoRoom | Score: 3.34
   Because: genre match (+2.00); energy closeness (+0.95; song 0.40, target 0.35); acoustic preference (+0.39)
4. Spacewalk Thoughts — Orbit Bloom | Score: 2.89
   Because: mood match (+1.50); energy closeness (+0.93; song 0.28, target 0.35); acoustic preference (+0.46)
5. Desert Letters — Saffron Trail | Score: 1.44
   Because: energy closeness (+0.97; song 0.32, target 0.35); acoustic preference (+0.47)
```

### Deep Intense Rock

```text
User profile: Deep Intense Rock
Preferences: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.9, 'likes_acoustic': False}
Top recommendations:
1. Storm Runner — Voltline | Score: 4.49
   Because: genre match (+2.00); mood match (+1.50); energy closeness (+0.99; song 0.91, target 0.90)
2. Gym Hero — Max Pulse | Score: 2.47
   Because: mood match (+1.50); energy closeness (+0.97; song 0.93, target 0.90)
3. Brass Parade — Sol Avenue | Score: 0.98
   Because: energy closeness (+0.98; song 0.88, target 0.90)
4. Concrete Resolve — Verse Atlas | Score: 0.95
   Because: energy closeness (+0.95; song 0.85, target 0.90)
5. Iron Horizon — Forge Signal | Score: 0.92
   Because: energy closeness (+0.92; song 0.98, target 0.90)
```

### Conflicting Sad Pop

```text
User profile: Conflicting Sad Pop
Preferences: {'favorite_genre': 'pop', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': False}
Top recommendations:
1. Gym Hero — Max Pulse | Score: 2.97
   Because: genre match (+2.00); energy closeness (+0.97; song 0.93, target 0.90)
2. Sunrise City — Neon Echo | Score: 2.92
   Because: genre match (+2.00); energy closeness (+0.92; song 0.82, target 0.90)
3. After the Applause — Blue Ember | Score: 2.06
   Because: mood match (+1.50); energy closeness (+0.56; song 0.46, target 0.90)
4. Storm Runner — Voltline | Score: 0.99
   Because: energy closeness (+0.99; song 0.91, target 0.90)
5. Brass Parade — Sol Avenue | Score: 0.98
   Because: energy closeness (+0.98; song 0.88, target 0.90)
```

### Unknown Genre

```text
User profile: Unknown Genre
Preferences: {'favorite_genre': 'k-pop', 'favorite_mood': 'happy', 'target_energy': 0.8, 'likes_acoustic': False}
Top recommendations:
1. Sunrise City — Neon Echo | Score: 2.48
   Because: mood match (+1.50); energy closeness (+0.98; song 0.82, target 0.80)
2. Rooftop Lights — Indigo Parade | Score: 2.46
   Because: mood match (+1.50); energy closeness (+0.96; song 0.76, target 0.80)
3. Concrete Resolve — Verse Atlas | Score: 0.95
   Because: energy closeness (+0.95; song 0.85, target 0.80)
4. Night Drive Loop — Neon Echo | Score: 0.95
   Because: energy closeness (+0.95; song 0.75, target 0.80)
5. Brass Parade — Sol Avenue | Score: 0.92
   Because: energy closeness (+0.92; song 0.88, target 0.80)
```

### Pairwise comparisons

- **High-Energy Pop vs Chill Lofi:** first choices are Sunrise City and Library Rain. Lofi favors lower energy and acousticness instead of happy pop.
- **High-Energy Pop vs Deep Intense Rock:** first choices are Sunrise City and Storm Runner. Both favor high energy, but the genre and mood matches move the winner from pop to rock.
- **High-Energy Pop vs Conflicting Sad Pop:** first choices are Sunrise City and Gym Hero. Removing the happy-mood bonus allows the higher-energy pop track to take first place.
- **High-Energy Pop vs Unknown Genre:** first choices are Sunrise City and Sunrise City. Both retain happy mood and energy 0.8, but missing genre points move Gym Hero out of the unknown-genre top five.
- **Chill Lofi vs Deep Intense Rock:** first choices are Library Rain and Storm Runner. The rock profile replaces low-energy acoustic preferences with intense, high-energy matches.
- **Chill Lofi vs Conflicting Sad Pop:** first choices are Library Rain and Gym Hero. Sad pop favors high-energy pop despite its mood conflict, while lofi has strong matches on genre, mood, and energy.
- **Chill Lofi vs Unknown Genre:** first choices are Library Rain and Sunrise City. The unknown genre falls back to happy mood and high energy; lofi has exact genre and chill matches plus an acoustic bonus.
- **Deep Intense Rock vs Conflicting Sad Pop:** first choices are Storm Runner and Gym Hero. Both target energy 0.9, but rock/intense selects Storm Runner while pop/sad selects Gym Hero through the stronger genre bonus.
- **Deep Intense Rock vs Unknown Genre:** first choices are Storm Runner and Sunrise City. Rock has exact genre and intense-mood matches; the unknown genre has no genre match and instead favors happy songs.
- **Conflicting Sad Pop vs Unknown Genre:** first choices are Gym Hero and Sunrise City. Sad pop selects Gym Hero through genre and energy, while unknown-genre happy preferences select Sunrise City through mood and energy.

### Why Sunrise City ranks first

Its baseline score is 2 for pop + 1.5 for happy + (1 - |0.82 - 0.80|) = 4.48. Gym Hero gets 2 + 0 + 0.87 = 2.87. Rooftop Lights gets 0 + 1.5 + 0.96 = 2.46. Thus the winner is consistent with the explicit rule; that is not proof a listener would prefer it.

### Weight-shift experiment

Command: `python -m src.main --evaluate --experiment`. Genre weight was halved from 2 to 1 and energy doubled from 1 to 2. Mood and acoustic rules were unchanged. All terms stay finite and nonnegative, and energy similarity remains closeness-based. Actual terminal output follows:

```text
Loaded songs: 18
Weights: genre=1.0, mood=1.5, energy=2.0

User profile: High-Energy Pop
Preferences: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.8, 'likes_acoustic': False}
Top recommendations:
1. Sunrise City — Neon Echo | Score: 4.46
   Because: genre match (+1.00); mood match (+1.50); energy closeness (+1.96; song 0.82, target 0.80)
2. Rooftop Lights — Indigo Parade | Score: 3.42
   Because: mood match (+1.50); energy closeness (+1.92; song 0.76, target 0.80)
3. Gym Hero — Max Pulse | Score: 2.74
   Because: genre match (+1.00); energy closeness (+1.74; song 0.93, target 0.80)
4. Concrete Resolve — Verse Atlas | Score: 1.90
   Because: energy closeness (+1.90; song 0.85, target 0.80)
5. Night Drive Loop — Neon Echo | Score: 1.90
   Because: energy closeness (+1.90; song 0.75, target 0.80)

User profile: Chill Lofi
Preferences: {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.35, 'likes_acoustic': True}
Top recommendations:
1. Library Rain — Paper Lanterns | Score: 4.93
   Because: genre match (+1.00); mood match (+1.50); energy closeness (+2.00; song 0.35, target 0.35); acoustic preference (+0.43)
2. Midnight Coding — LoRoom | Score: 4.71
   Because: genre match (+1.00); mood match (+1.50); energy closeness (+1.86; song 0.42, target 0.35); acoustic preference (+0.35)
3. Spacewalk Thoughts — Orbit Bloom | Score: 3.82
   Because: mood match (+1.50); energy closeness (+1.86; song 0.28, target 0.35); acoustic preference (+0.46)
4. Focus Flow — LoRoom | Score: 3.29
   Because: genre match (+1.00); energy closeness (+1.90; song 0.40, target 0.35); acoustic preference (+0.39)
5. Desert Letters — Saffron Trail | Score: 2.41
   Because: energy closeness (+1.94; song 0.32, target 0.35); acoustic preference (+0.47)

User profile: Deep Intense Rock
Preferences: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.9, 'likes_acoustic': False}
Top recommendations:
1. Storm Runner — Voltline | Score: 4.48
   Because: genre match (+1.00); mood match (+1.50); energy closeness (+1.98; song 0.91, target 0.90)
2. Gym Hero — Max Pulse | Score: 3.44
   Because: mood match (+1.50); energy closeness (+1.94; song 0.93, target 0.90)
3. Brass Parade — Sol Avenue | Score: 1.96
   Because: energy closeness (+1.96; song 0.88, target 0.90)
4. Concrete Resolve — Verse Atlas | Score: 1.90
   Because: energy closeness (+1.90; song 0.85, target 0.90)
5. Iron Horizon — Forge Signal | Score: 1.84
   Because: energy closeness (+1.84; song 0.98, target 0.90)

User profile: Conflicting Sad Pop
Preferences: {'favorite_genre': 'pop', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': False}
Top recommendations:
1. Gym Hero — Max Pulse | Score: 2.94
   Because: genre match (+1.00); energy closeness (+1.94; song 0.93, target 0.90)
2. Sunrise City — Neon Echo | Score: 2.84
   Because: genre match (+1.00); energy closeness (+1.84; song 0.82, target 0.90)
3. After the Applause — Blue Ember | Score: 2.62
   Because: mood match (+1.50); energy closeness (+1.12; song 0.46, target 0.90)
4. Storm Runner — Voltline | Score: 1.98
   Because: energy closeness (+1.98; song 0.91, target 0.90)
5. Brass Parade — Sol Avenue | Score: 1.96
   Because: energy closeness (+1.96; song 0.88, target 0.90)

User profile: Unknown Genre
Preferences: {'favorite_genre': 'k-pop', 'favorite_mood': 'happy', 'target_energy': 0.8, 'likes_acoustic': False}
Top recommendations:
1. Sunrise City — Neon Echo | Score: 3.46
   Because: mood match (+1.50); energy closeness (+1.96; song 0.82, target 0.80)
2. Rooftop Lights — Indigo Parade | Score: 3.42
   Because: mood match (+1.50); energy closeness (+1.92; song 0.76, target 0.80)
3. Concrete Resolve — Verse Atlas | Score: 1.90
   Because: energy closeness (+1.90; song 0.85, target 0.80)
4. Night Drive Loop — Neon Echo | Score: 1.90
   Because: energy closeness (+1.90; song 0.75, target 0.80)
5. Brass Parade — Sol Avenue | Score: 1.84
   Because: energy closeness (+1.84; song 0.88, target 0.80)
```

For happy pop, Rooftop Lights rises from third (2.46) to second (3.42), above Gym Hero (2.74 under the new weights). For chill lofi, Spacewalk Thoughts rises above Focus Flow because mood and energy can outweigh the reduced genre advantage. First-place songs remain unchanged across all five profiles. The experiment makes the results different, not demonstrably more accurate: no listener ratings were collected. The default weights are retained so both versions remain reproducible.

### Checks and human evaluation boundary

The automated suite verifies numeric CSV loading, exact scoring, closeness, full-catalog ranking, catalog preservation, stable ties, k boundaries, invalid energies, acoustic bonuses, interface consistency, the weight-shift reversal, and CLI output, alongside the two starter tests. All 14 tests passed in the recorded run. Dependency consistency passed as well. These checks verify implementation behavior, not musical satisfaction.

The happy-pop winner appears consistent with its supplied metadata. The student must still compare at least one profile against their own musical intuition; the assistant cannot honestly claim personal listening experience with these fictional tracks.

## 8. Future Work
Support multiple favorite genres, related genre labels, context and energy ranges, feedback from listeners, adjustable weights, and explicit diversity constraints. Expand and audit the catalog with measured audio features and better coverage. Validate improvements with real listener judgments instead of assuming changed rankings are better.

## 9. Personal Reflection
Pending student input: describe whether one profile's recommendations feel right to you, what surprised you, and what you personally learned. The technical observation is that rule choices and catalog coverage determine both relevance and bias; this is not a claim about the student's experiences.

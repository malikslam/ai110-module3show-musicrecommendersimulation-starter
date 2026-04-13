# 🎵 Music Recommender Simulation

## Project Summary

**VibeMatcher 1.0** is a content-based music recommender system that scores songs by comparing their audio features (energy, mood, acousticness, valence, danceability, tempo) against a user's taste profile. Instead of analyzing what millions of users like (collaborative filtering), it measures how well each song's attributes match a single user's preferences using weighted similarity scoring.

The system demonstrates three key insights:

1. **Simplicity is powerful**: A few well-chosen features and transparent ranking logic create recommendations that feel personalized without requiring massive data or black-box ML models.
2. **Every design choice is a values choice**: Weighting mood 2x stronger than genre isn't mathematically "right" or "wrong"—it's a decision that shapes what users discover. This creates both benefits (users get emotionally matching songs) and harms (users get locked into mood stereotypes).
3. **Small, biased datasets perpetuate bias**: With only 10 songs and 30% lofi representation, the recommender amplifies existing music industry patterns rather than challenging them.

---

## How The System Works

Real-world music recommenders like Spotify combine collaborative filtering (analyzing what similar users like) and content-based filtering (matching song attributes to user preferences), often using machine learning for personalization. This simulation prioritizes simplicity and transparency by focusing on content-based filtering with numerical song features, allowing users to see exactly why recommendations are made without complex algorithms or large datasets.

- **Song Features**: Each song uses `energy` (intensity level), `valence` (emotional positivity), `danceability` (groove factor), `acousticness` (acoustic vs. electronic), and `tempo_bpm` (pace, normalized to 0-1).
- **UserProfile Information**: Stores the user's preferred values for the same features (`energy`, `valence`, `danceability`, `acousticness`, `tempo_bpm`), representing their ideal "vibe."
- **Recommender Scoring**: For each song, compute a similarity score per feature using `1 - |user_pref - song_value|`, then average them for an overall score.
- **Recommendation Selection**: Rank songs by score and recommend the top 3-5 matches.

---

### Finalized Algorithm Recipe

For each song in the catalog, `score_song()` computes a weighted similarity score:

**Step 1 — Categorical features** (genre, mood):
- If the song's value matches the user's preference → score `1.0`, otherwise `0.0`

**Step 2 — Numeric features** (energy, acousticness, valence, tempo_bpm, danceability):
- Per-feature similarity = `1 - abs(user_value - song_value)`
- `tempo_bpm` must be normalized first: `tempo_normalized = tempo_bpm / 200`

**Step 3 — Apply weights** and compute the final score:

| Feature | Weight | Reason |
|---|---|---|
| `mood` | 2.0 | Strongest vibe signal — directly reflects how a song feels |
| `energy` | 1.5 | Primary numeric separator between intense and chill tracks |
| `acousticness` | 1.5 | Cleanly divides electric/distorted from organic/mellow sounds |
| `genre` | 1.0 | Useful broad anchor, but one genre can span many moods |
| `tempo_bpm` | 1.0 | Supporting signal for pace |
| `valence` | 1.0 | Supporting signal for emotional brightness |
| `danceability` | 0.5 | Weakest differentiator in this catalog |

```
final_score = Σ(feature_score × weight) / Σ(all weights)
```

`recommend_songs()` collects `(song_dict, score, explanation)` for every song, sorts by score descending, and returns the top `k` results.

---

### Potential Biases

- **Mood can overshadow genre**: Because mood has double the weight of genre, a song with a matching mood but mismatched genre (e.g., a pop/intense track for a rock user) may outscore a rock/chill song. Great genre matches can be buried if the mood is off.
- **Small catalog amplifies gaps**: With only 10 songs, underrepresented genres (ambient, jazz, synthwave each appear once) will almost never rank highly for users who don't prefer them, even if numeric features are a close match.
- **Numeric features assume a single ideal point**: The formula rewards songs closest to the user's target values. A user who enjoys *both* high-energy and chill tracks depending on context cannot be represented — the profile only captures one vibe at a time.
- **tempo_bpm normalization is fragile**: Dividing by 200 works for this dataset (max BPM is 152), but would silently break if songs with BPM > 200 were added without updating the divisor.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
PYTHONPATH=src python3 src/main.py
```

### Sample Output

The terminal displays both taste profiles side by side — song title, artist, genre, mood, a visual score bar, and the specific reasons generated by the scoring function:

<img src="images/terminal_output-0.png" alt="Terminal output showing recommendations for Rock/Intense profile" width="400">

<img src="images/terminal_output-1.png" alt="Terminal output showing recommendations for Pop/Happy profile" width="400">

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Experiment 1 — Stress Test with Three Distinct Profiles

Ran the system against three maximally different taste profiles to verify
the scoring logic produces sensible rankings across the full catalog.

<img src="images/terminal_output-0.png" alt="Deep Intense Rock — Profile A top results" width="300">

<img src="images/terminal_output-1.png" alt="High-Energy Pop — Profile B top results" width="300">

**Do the results feel right?**

**Profile A — Deep Intense Rock → Storm Runner scored 0.99**

Yes, this feels correct. Storm Runner is the only rock/intense track in
the catalog and every numeric feature lands within 0.03 of the target
(energy 0.91 vs 0.90, acousticness 0.10 vs 0.08, tempo 152 vs 148 BPM).
The near-perfect score is mathematically honest — the song is a near
ideal match on all seven dimensions simultaneously.

**Profile B — High-Energy Pop → Sunrise City ranked #1, but Gym Hero ranked #3**

Partially feels right, partially surprising. Sunrise City at #1 is
correct — it matches both genre (pop) and mood (happy). But Gym Hero
(pop/intense) ranking below Rooftop Lights (indie pop/happy) felt off at
first. On reflection it makes sense: mood weight is 2.0 while genre
weight is 1.0, so Rooftop Lights' happy mood match (worth 2.0 pts)
outweighs Gym Hero's genre match (worth 1.0 pt). This exposed the
documented bias: **mood can overshadow genre**.

**Profile C — Chill Lofi → Library Rain and Midnight Coding tied at 0.98**

The tie was unexpected but correct. Both are lofi/chill with nearly
identical numeric features. The system cannot distinguish them with the
current feature set — which is an honest reflection of the data, not a
bug.

---

### Experiment 2 — Copilot Inline Chat: Why did Storm Runner rank #1?

Prompt used on the `WEIGHTS` dict in `recommender.py`:

> "Given this `WEIGHTS` dictionary where `mood=2.0`, `energy=1.5`,
> `acousticness=1.5`, and `genre=1.0`, explain step by step why
> Storm Runner scores 0.99 for a profile with `genre='rock'`,
> `mood='intense'`, `energy=0.90`, `acousticness=0.08`, `tempo_bpm=148`.
> Show the per-feature weighted calculation and identify which single
> weight contributed most to the final score."

**Key insight from the trace:** mood and energy together account for
`(2.0 + 1.5) / 8.5 = 41%` of the total possible weight. When both match
closely — as they do for Storm Runner — no other song in the catalog can
catch up, even if it matches better on the remaining five features.

---

## Limitations and Risks

**Mood weight overpowers genre preference.** During testing, a user looking for pop music (genre match: 1.0, weight 1.0) would see indie pop and synthwave tracks ranked higher if those songs had a matching mood (mood match: 1.0, weight 2.0). For example, in Profile B (High-Energy Pop), Rooftop Lights (indie pop/happy) outscore Gym Hero (pop/intense) despite Gym Hero being an exact genre match, purely because "happy" is weighted twice as strongly as "pop." This reveals filter bubbles: users interested in exploring adjacent genres within their preferred mood will never see them ranked competitively, even when numeric features align well. A user who thinks "I want music like pop but with a different vibe" cannot express that intent with the current profile structure. Real-world impact: this could perpetuate echo chambers where users never break out of their mood stereotype, even when other features align with their taste.

Additional limitations documented during experiments:
- **Tiny catalog creates blind spots.** Some genres (ambient, jazz, synthwave) appear only once; cross-genre recommendations are impossible.
- **No support for context or time-of-day.**  The profile is static — a user must choose between "gym energy" and "bedtime chill," not both in one session.
- **Numeric features assume a single ideal point.** Listeners who enjoy both extremes (high and low energy on different days) cannot be represented.

You will go deeper on this in your model card.

---

## Reflection

Read the detailed analysis in [**Model Card**](model_card.md).

### What I Learned

**About how recommenders turn data into predictions:** Recommenders are not neutral prediction engines—they are *design choices made visible through data*. When I set mood weight to 2.0, I wasn't describing a universal truth about music perception. I was making a choice: "I believe mood is twice as important as genre for this user." That choice cascades. It changes rankings, shapes user expectations, and over time, trains users to think "all the pop I see is happy music," even if pop has an intense side. Real recommenders work the same way but hidden inside complex models. They're not discovering what users like; they're reflecting what their designers believed users should like.

**About where bias shows up:** Bias enters at every layer. Dataset bias is obvious (30% lofi = lofi dominates). But design bias is sneakier. Hard genre matching (1.0 or 0.0) prevents cross-genre discovery. Categorical features block adjacent preferences entirely. Feature selection itself is biased—why energy and not "emotional depth" or "musicianship"? Why did I include danceability (0.5 weight) but not lyrics? Each choice privileges some users and harms others. The scariest part: good explanations ("genre matched") make users trust the system more, so they're less likely to notice they're being filtered.


---

## Next Steps

For a complete analysis of VibeMatcher's strengths, limitations, evaluation process, and engineering insights, see the [**Detailed Model Card**](model_card.md).

Additional technical notes:
- See [**reflection.md**](reflection.md) for side-by-side profile comparisons and how mood/energy preferences reshape rankings
- Run `PYTHONPATH=src python3 src/main.py` to generate live recommendations
- Run `pytest` to validate the scoring logic against test profiles


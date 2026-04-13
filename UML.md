# Music Recommender — Data Flow Diagram

Traces a single song from `songs.csv` through scoring to the final ranked output.

```mermaid
flowchart TD
    A["main()"]

    A --> B["load_songs('data/songs.csv')\nParses CSV → List[Dict]\n10 song dicts"]

    A --> C["user_prefs dict\ngenre: 'rock'  mood: 'intense'\nenergy: 0.85   tempo_bpm: 140\nvalence: 0.50  acousticness: 0.10\ndanceability: 0.65"]

    B --> E
    C --> E

    E["recommend_songs(user_prefs, songs, k=5)"]
    E --> F{"For each song\nin catalog"}

    F --> G["score_song(user_prefs, song)"]

    G --> H["Categorical Compare\ngenre match → 1.0 or 0.0  × weight 1.0\nmood  match → 1.0 or 0.0  × weight 2.0"]

    G --> I["Numeric Similarity\n1 - abs(user_val - song_val)\nenergy       × 1.5\nacousticness × 1.5\nvalence      × 1.0\ntempo_bpm    × 1.0  ⚠ normalize ÷ 200 first\ndanceability × 0.5"]

    H --> J["Weighted Average\nΣ(feature_score × weight) / Σ(all weights)\n→ final_score in range 0.0 – 1.0"]
    I --> J

    J --> K["Return (score, reasons)\nback to recommend_songs"]

    K --> L["Bundle result\n(song_dict, score, explanation_string)"]

    L -->|"next song"| F

    F -->|"all songs scored"| M["Sort all results\nby score descending"]

    M --> N["Slice top k\nList of (song_dict, score, explanation)"]

    N --> O["main() prints each result\ntitle — Score: 0.87\nBecause: mood matched, high energy..."]
```

## Key Design Decisions

| Decision | Reason |
|---|---|
| Mood weight = 2.0, Genre weight = 1.0 | Mood is a stronger vibe signal; genre spans multiple moods |
| Energy & acousticness weight = 1.5 | Primary numeric separators between intense rock and chill lofi |
| tempo_bpm normalized ÷ 200 | Raw BPM (60–152) must be on 0–1 scale before `1 - abs(diff)` |
| score_song returns (score, reasons) | Song dict is bundled one level up in recommend_songs, not inside scorer |
| Danceability weight = 0.5 | Weakest differentiator in this 10-song catalog |

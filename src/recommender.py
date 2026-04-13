import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Feature weights used by score_song().
# Mood is 2x genre because it is a stronger vibe signal —
# one genre can span many moods, but mood directly reflects feel.
WEIGHTS: Dict[str, float] = {
    "mood":         2.0,
    "energy":       1.5,
    "acousticness": 1.5,
    "genre":        1.0,
    "tempo_bpm":    1.0,
    "valence":      1.0,
    "danceability": 0.5,
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why song was recommended to user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse songs.csv and return a list of song dicts with typed fields."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return (score 0–1, reasons) by comparing song features to user_prefs using a weighted average."""
    feature_scores: Dict[str, float] = {}
    reasons: List[str] = []

    # --- Categorical features: 1.0 if exact match, 0.0 otherwise ---

    if "genre" in user_prefs:
        match = 1.0 if user_prefs["genre"] == song["genre"] else 0.0
        feature_scores["genre"] = match
        if match:
            reasons.append(f"genre matched ({song['genre']})")

    if "mood" in user_prefs:
        match = 1.0 if user_prefs["mood"] == song["mood"] else 0.0
        feature_scores["mood"] = match
        if match:
            reasons.append(f"mood matched ({song['mood']})")

    # --- Numeric features: 1 - abs(user_value - song_value) ---
    # tempo_bpm is normalized to 0–1 by dividing by 200 before comparing.

    if "energy" in user_prefs:
        s = 1.0 - abs(user_prefs["energy"] - song["energy"])
        feature_scores["energy"] = s
        if s >= 0.85:
            reasons.append(f"energy is a close match ({song['energy']})")

    if "acousticness" in user_prefs:
        s = 1.0 - abs(user_prefs["acousticness"] - song["acousticness"])
        feature_scores["acousticness"] = s
        if s >= 0.85:
            reasons.append(f"acousticness is a close match ({song['acousticness']})")

    if "valence" in user_prefs:
        s = 1.0 - abs(user_prefs["valence"] - song["valence"])
        feature_scores["valence"] = s

    if "tempo_bpm" in user_prefs:
        user_tempo = user_prefs["tempo_bpm"] / 200.0
        song_tempo = song["tempo_bpm"] / 200.0
        s = 1.0 - abs(user_tempo - song_tempo)
        feature_scores["tempo_bpm"] = s
        if s >= 0.85:
            reasons.append(f"tempo is a close match ({song['tempo_bpm']} BPM)")

    if "danceability" in user_prefs:
        s = 1.0 - abs(user_prefs["danceability"] - song["danceability"])
        feature_scores["danceability"] = s

    # --- Weighted average ---
    total_weighted = sum(feature_scores[f] * WEIGHTS[f] for f in feature_scores)
    total_weights  = sum(WEIGHTS[f] for f in feature_scores)
    final_score    = total_weighted / total_weights if total_weights > 0 else 0.0

    if not reasons:
        reasons.append("partial numeric similarity, no exact categorical match")

    return final_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song with score_song(), sort by score descending, and return the top-k results."""
    scored = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:k]

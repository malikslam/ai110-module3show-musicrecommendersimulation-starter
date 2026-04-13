"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: captures enough dimensions to distinguish
    # high-intensity tracks (rock, intense, fast) from low-energy ones (lofi, chill, slow).
    # - energy + tempo_bpm together flag "intense rock" (high) vs "chill lofi" (low)
    # - acousticness separates organic/mellow sounds from electric/distorted ones
    # - mood and genre act as categorical anchors for genre-based matching
    # - valence captures emotional brightness (happy vs moody)
    # - likes_acoustic=False ensures electric/energetic tracks score higher than acoustic ones
    user_prefs = {
        "genre": "rock",           # categorical: preferred genre
        "mood": "intense",         # categorical: preferred mood
        "energy": 0.85,            # 0.0–1.0: how energetic the track should feel
        "tempo_bpm": 140,          # beats per minute: fast = intense, slow = chill
        "valence": 0.50,           # 0.0–1.0: emotional positivity (0=dark, 1=euphoric)
        "acousticness": 0.10,      # 0.0–1.0: low = electric/distorted, high = acoustic/mellow
        "danceability": 0.65,      # 0.0–1.0: rhythmic drive
        "likes_acoustic": False,   # boolean shortcut used by UserProfile dataclass
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()

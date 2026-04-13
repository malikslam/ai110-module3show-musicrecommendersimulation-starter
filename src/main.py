"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


WIDTH = 56  # terminal display width for separator lines


def print_header(label: str) -> None:
    print("\n" + "=" * WIDTH)
    print(f"  {label}")
    print("=" * WIDTH)


def print_recommendation(rank: int, song: dict, score: float, explanation: str) -> None:
    bar_filled = int(score * 20)
    bar = "#" * bar_filled + "-" * (20 - bar_filled)
    print(f"\n  #{rank}  {song['title']} — {song['artist']}")
    print(f"       Genre : {song['genre']:<12}  Mood : {song['mood']}")
    print(f"       Score : {score:.2f}  [{bar}]")
    # wrap reasons onto separate lines for readability
    reasons = explanation.split(", ")
    print(f"       Why   : {reasons[0]}")
    for reason in reasons[1:]:
        print(f"               {reason}")
    print("  " + "-" * (WIDTH - 2))


def main() -> None:
    songs = load_songs("data/songs.csv")

    # ----------------------------------------------------------------
    # Profile A — Rock / Intense (our defined taste profile)
    # ----------------------------------------------------------------
    rock_prefs = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.85,
        "tempo_bpm": 140,
        "valence": 0.50,
        "acousticness": 0.10,
        "danceability": 0.65,
        "likes_acoustic": False,
    }

    # ----------------------------------------------------------------
    # Profile B — Pop / Happy (default starter profile for verification)
    # Expected top result: Sunrise City (pop, happy, energy 0.82)
    # ----------------------------------------------------------------
    pop_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "tempo_bpm": 118,
        "valence": 0.84,
        "acousticness": 0.20,
        "danceability": 0.79,
        "likes_acoustic": False,
    }

    for label, user_prefs in [
        ("Profile: Rock / Intense  —  Top 5 Recommendations", rock_prefs),
        ("Profile: Pop / Happy     —  Top 5 Recommendations", pop_prefs),
    ]:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_header(label)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print_recommendation(rank, song, score, explanation)


if __name__ == "__main__":
    main()

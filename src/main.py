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
    # Profile A — Deep Intense Rock
    # Targets fast, loud, electric tracks.
    # Expected #1: Storm Runner (rock/intense, energy 0.91, tempo 152)
    # ----------------------------------------------------------------
    deep_rock = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.90,
        "tempo_bpm": 148,
        "valence": 0.45,
        "acousticness": 0.08,
        "danceability": 0.65,
        "likes_acoustic": False,
    }

    # ----------------------------------------------------------------
    # Profile B — High-Energy Pop
    # Targets upbeat, danceable, bright pop tracks.
    # Expected #1: Sunrise City (pop/happy, energy 0.82, valence 0.84)
    # ----------------------------------------------------------------
    high_energy_pop = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "tempo_bpm": 125,
        "valence": 0.82,
        "acousticness": 0.15,
        "danceability": 0.85,
        "likes_acoustic": False,
    }

    # ----------------------------------------------------------------
    # Profile C — Chill Lofi
    # Targets slow, mellow, acoustic background tracks.
    # Expected #1: Library Rain (lofi/chill, energy 0.35, acousticness 0.86)
    # ----------------------------------------------------------------
    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "tempo_bpm": 75,
        "valence": 0.58,
        "acousticness": 0.78,
        "danceability": 0.60,
        "likes_acoustic": True,
    }

    for label, user_prefs in [
        ("Profile A: Deep Intense Rock    — Top 5", deep_rock),
        ("Profile B: High-Energy Pop      — Top 5", high_energy_pop),
        ("Profile C: Chill Lofi           — Top 5", chill_lofi),
    ]:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_header(label)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print_recommendation(rank, song, score, explanation)


if __name__ == "__main__":
    main()

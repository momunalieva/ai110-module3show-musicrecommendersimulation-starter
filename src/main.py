"""Run a default recommendation or reproducible evaluation from the CLI."""
import argparse
import textwrap
from pathlib import Path
from .recommender import SCORING_MODES, load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.9, "likes_acoustic": False},
    "Conflicting Sad Pop": {"favorite_genre": "pop", "favorite_mood": "sad", "target_energy": 0.9, "likes_acoustic": False},
    "Unknown Genre": {"favorite_genre": "k-pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False},
}


def main() -> None:
    """Print top-five scores and reasons for the selected evaluation profiles."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluate", action="store_true", help="run all five profiles")
    parser.add_argument("--experiment", action="store_true", help="halve genre weight and double energy weight")
    parser.add_argument("--mode", choices=SCORING_MODES, default="genre-first")
    parser.add_argument("--diversity", action="store_true", help="penalize repeated artists and genres")
    parser.add_argument("--advanced", action="store_true", help="use five additional preference targets")
    parser.add_argument("--table", action="store_true", help="print a table including reasons")
    args = parser.parse_args()
    songs = load_songs(Path(__file__).resolve().parents[1] / "data" / "songs.csv")
    print(f"Loaded songs: {len(songs)}")
    mode = "energy-focused" if args.experiment else args.mode
    weights = SCORING_MODES[mode]
    print(f"Weights: genre={weights['genre_weight']}, mood={weights['mood_weight']}, energy={weights['energy_weight']}")
    profiles = PROFILES if args.evaluate else {"High-Energy Pop": PROFILES["High-Energy Pop"]}
    for name, preferences in profiles.items():
        preferences = dict(preferences)
        if args.advanced:
            preferences.update(target_popularity=60, target_release_decade=2020,
                               target_duration_seconds=210, target_instrumentalness=0.4,
                               prefers_live=False)
        print(f"\nUser profile: {name}\nPreferences: {preferences}\nTop recommendations:")
        results = recommend_songs(preferences, songs, k=5, diversity=args.diversity, **weights)
        if args.table:
            print(f"{'Rank':<5} | {'Song':<24} | {'Score':<7} | Reasons")
            print("-" * 110)
        for rank, (song, score, explanation) in enumerate(results, 1):
            if args.table:
                lines = textwrap.wrap(explanation, width=65)
                print(f"{rank:<5} | {song['title']:<24} | {score:<7.2f} | {lines[0]}")
                for line in lines[1:]:
                    print(f"{'':5} | {'':24} | {'':7} | {line}")
                continue
            print(f"{rank}. {song['title']} — {song['artist']} | Score: {score:.2f}")
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()

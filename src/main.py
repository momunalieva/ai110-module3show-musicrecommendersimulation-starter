"""Run a default recommendation or reproducible evaluation from the CLI."""
import argparse
from pathlib import Path
from .recommender import load_songs, recommend_songs

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
    args = parser.parse_args()
    songs = load_songs(Path(__file__).resolve().parents[1] / "data" / "songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print("Weights: genre=1.0, mood=1.5, energy=2.0" if args.experiment else "Weights: genre=2.0, mood=1.5, energy=1.0")
    weights = {"genre_weight": 1.0, "energy_weight": 2.0} if args.experiment else {}
    profiles = PROFILES if args.evaluate else {"High-Energy Pop": PROFILES["High-Energy Pop"]}
    for name, preferences in profiles.items():
        print(f"\nUser profile: {name}\nPreferences: {preferences}\nTop recommendations:")
        for rank, (song, score, explanation) in enumerate(recommend_songs(preferences, songs, k=5, **weights), 1):
            print(f"{rank}. {song['title']} — {song['artist']} | Score: {score:.2f}")
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()

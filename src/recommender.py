"""Content-based scoring shared by the dictionary and object interfaces."""
import csv
import math
from dataclasses import MISSING, asdict, dataclass
from typing import Dict, List, Tuple


@dataclass
class Song:
    """Store catalog metadata and normalized musical attributes."""
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
    popularity: float = 50
    release_decade: int = 2020
    duration_seconds: float = 180
    instrumentalness: float = 0
    live_performance: bool = False


@dataclass
class UserProfile:
    """Store explicit musical preferences without inferred listening history."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _unit_value(value: float, name: str) -> float:
    """Require a finite numeric value in the inclusive zero-to-one range."""
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def load_songs(csv_path: str) -> List[Dict]:
    """Read CSV rows into dictionaries and convert numeric fields."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {name for name, field in Song.__dataclass_fields__.items() if field.default is MISSING}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Song CSV is missing required columns")
        for row in reader:
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            if not math.isfinite(row["tempo_bpm"]) or row["tempo_bpm"] <= 0:
                raise ValueError("tempo_bpm must be positive and finite")
            for field in ("energy", "valence", "danceability", "acousticness"):
                row[field] = _unit_value(row[field], field)
            for name in ("popularity", "duration_seconds", "instrumentalness"):
                if name in row:
                    row[name] = float(row[name])
            if "release_decade" in row:
                row["release_decade"] = int(row["release_decade"])
            if "live_performance" in row:
                if row["live_performance"] not in ("0", "1"):
                    raise ValueError("live_performance must be 0 or 1")
                row["live_performance"] = row["live_performance"] == "1"
            if "popularity" in row:
                _unit_value(row["popularity"] / 100, "popularity / 100")
            if "instrumentalness" in row:
                _unit_value(row["instrumentalness"], "instrumentalness")
            if "duration_seconds" in row and (not math.isfinite(row["duration_seconds"]) or row["duration_seconds"] <= 0):
                raise ValueError("duration_seconds must be finite and positive")
            songs.append(row)
    if len({song["id"] for song in songs}) != len(songs):
        raise ValueError("Song IDs must be unique")
    return songs


def score_song(user_prefs: Dict, song: Dict, *, genre_weight: float = 2.0,
               mood_weight: float = 1.5, energy_weight: float = 1.0) -> Tuple[float, List[str]]:
    """Return a weighted relevance score and its individual contributions."""
    # Accept both the starter CLI keys and the UserProfile field names.
    genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target = user_prefs.get("target_energy", user_prefs.get("energy"))
    if not isinstance(genre, str) or not isinstance(mood, str):
        raise ValueError("A genre and mood preference are required")
    if target is None:
        raise ValueError("An energy preference is required")
    target = _unit_value(target, "target_energy")
    energy = _unit_value(song["energy"], "song energy")
    score, reasons = 0.0, []
    for label, preference, weight in (("genre", genre, genre_weight), ("mood", mood, mood_weight)):
        if not math.isfinite(weight) or weight < 0:
            raise ValueError("Weights must be finite and nonnegative")
        if song[label].strip().casefold() == preference.strip().casefold():
            score += weight
            reasons.append(f"{label} match (+{weight:.2f})")
    if not math.isfinite(energy_weight) or energy_weight < 0:
        raise ValueError("Weights must be finite and nonnegative")
    contribution = energy_weight * (1 - abs(energy - target))
    score += contribution
    reasons.append(f"energy closeness (+{contribution:.2f}; song {energy:.2f}, target {target:.2f})")
    if user_prefs.get("likes_acoustic", False):
        bonus = 0.5 * _unit_value(song["acousticness"], "acousticness")
        score += bonus
        reasons.append(f"acoustic preference (+{bonus:.2f})")
    # Advanced attributes contribute only when a user supplies the matching target.
    for field, scale in (("popularity", 100), ("release_decade", 50),
                         ("duration_seconds", 300), ("instrumentalness", 1)):
        key = "target_" + field
        if key in user_prefs:
            target_value = float(user_prefs[key])
            song_value = float(song[field])
            if not math.isfinite(target_value) or not math.isfinite(song_value):
                raise ValueError("Advanced targets and attributes must be finite")
            bonus = 0.5 * max(0, 1 - abs(song_value - target_value) / scale)
            score += bonus
            reasons.append(f"{field} closeness (+{bonus:.2f})")
    if "prefers_live" in user_prefs and song["live_performance"] == user_prefs["prefers_live"]:
        score += 0.5
        reasons.append("live preference match (+0.50)")
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    diversity: bool = False, **weights) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k without reordering the catalog."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, **weights)
        scored.append((song, score, "; ".join(reasons)))
    if not diversity:
        return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
    selected, artists, genres = [], {}, {}
    while scored and len(selected) < k:
        def adjusted(item):
            song, base, _ = item
            return base - 1.5 * artists.get(song["artist"], 0) - 0.75 * genres.get(song["genre"], 0)
        best = max(scored, key=adjusted)
        song, base, explanation = best
        final = adjusted(best)
        selected.append((song, final, explanation + f"; diversity penalty (-{base - final:.2f}); base score {base:.2f}"))
        artists[song["artist"]] = artists.get(song["artist"], 0) + 1
        genres[song["genre"]] = genres.get(song["genre"], 0) + 1
        scored.remove(best)
    return selected


class Recommender:
    """Expose the same scoring logic through Song and UserProfile objects."""
    def __init__(self, songs: List[Song]):
        """Keep the supplied song catalog."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return original Song objects ordered by their relevance score."""
        ranked = recommend_songs(asdict(user), [asdict(song) for song in self.songs], k)
        by_id = {song.id: song for song in self.songs}
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Describe the contributions used by the shared scoring function."""
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)


# A configuration-based Strategy pattern: swap weights, reuse the scoring engine.
SCORING_MODES = {
    "genre-first": {"genre_weight": 2.0, "mood_weight": 1.5, "energy_weight": 1.0},
    "mood-first": {"genre_weight": 1.0, "mood_weight": 2.5, "energy_weight": 1.0},
    "energy-focused": {"genre_weight": 1.0, "mood_weight": 1.5, "energy_weight": 2.0},
}

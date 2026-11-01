from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


import math
from dataclasses import asdict
from pathlib import Path
import pytest
from src.recommender import load_songs, score_song, recommend_songs

CATALOG = Path(__file__).resolve().parents[1] / 'data' / 'songs.csv'
PREFS = {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}


def test_csv_converts_numbers_and_preserves_unique_ids():
    songs = load_songs(CATALOG)
    assert len(songs) == 18
    assert len({song['id'] for song in songs}) == 18
    assert isinstance(songs[0]['id'], int)
    assert isinstance(songs[0]['energy'], float)
    assert songs[0]['tempo_bpm'] == 118


def test_score_exact_match_and_energy_distance():
    song = asdict(make_small_recommender().songs[0])
    score, reasons = score_song(PREFS, song)
    assert score == pytest.approx(4.5)
    assert len(reasons) == 3
    song['energy'] = 0.2
    assert score_song(PREFS, song)[0] == pytest.approx(3.9)


def test_ranking_scores_every_song_and_preserves_input():
    songs = load_songs(CATALOG)[::-1]
    ids = [song['id'] for song in songs]
    results = recommend_songs(PREFS, songs, 3)
    assert [song['title'] for song, _, _ in results] == ['Sunrise City', 'Gym Hero', 'Rooftop Lights']
    assert [song['id'] for song in songs] == ids
    assert all(results[i][1] >= results[i + 1][1] for i in range(len(results) - 1))


def test_energy_weight_experiment_changes_ranking():
    songs = load_songs(CATALOG)
    baseline = recommend_songs(PREFS, songs)
    experiment = recommend_songs(PREFS, songs, genre_weight=1, energy_weight=2)
    assert baseline[1][0]['title'] == 'Gym Hero'
    assert experiment[1][0]['title'] == 'Rooftop Lights'
    assert experiment[0][1] == pytest.approx(4.46)


def test_object_and_dictionary_interfaces_agree():
    songs = [Song(**song) for song in load_songs(CATALOG)]
    user = UserProfile('lofi', 'chill', 0.35, True)
    objects = Recommender(songs).recommend(user)
    dictionaries = recommend_songs(asdict(user), [asdict(song) for song in songs])
    assert [song.id for song in objects] == [song['id'] for song, _, _ in dictionaries]
    assert objects[0].title == 'Library Rain'


def test_ties_empty_and_k_boundaries():
    song = asdict(make_small_recommender().songs[0])
    other = dict(song, id=99)
    assert [item[0]['id'] for item in recommend_songs(PREFS, [other, song])] == [99, 1]
    assert recommend_songs(PREFS, []) == []
    assert recommend_songs(PREFS, [song], 0) == []
    assert len(recommend_songs(PREFS, [song], 100)) == 1
    with pytest.raises(ValueError):
        recommend_songs(PREFS, [song], -1)


@pytest.mark.parametrize('energy', [-0.1, 1.1, math.nan, math.inf])
def test_invalid_energy_rejected(energy):
    song = asdict(make_small_recommender().songs[0])
    with pytest.raises(ValueError):
        score_song(dict(PREFS, energy=energy), song)


def test_acoustic_bonus_only_when_requested():
    song = asdict(make_small_recommender().songs[0])
    baseline = score_song(PREFS, song)[0]
    assert score_song(dict(PREFS, likes_acoustic=True), song)[0] == pytest.approx(baseline + 0.1)


def test_cli_runs_and_prints_five_explained_results():
    import subprocess
    import sys
    result = subprocess.run([sys.executable, '-m', 'src.main'], cwd=CATALOG.parents[1], capture_output=True, text=True, check=True)
    assert 'Loaded songs: 18' in result.stdout
    assert '1. Sunrise City' in result.stdout
    assert result.stdout.count('Because:') == 5

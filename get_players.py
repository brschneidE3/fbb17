__author__ = 'brsch'

import read_projections
import add_total_projections
import add_fantrax
import pickle


def update_players():
    # Add projections
    batters = read_projections.read_batter_projections()
    pitchers = read_projections.read_pitcher_projections()

    # Add season totals, 1B's, season-to-date and calculate fantasy points and ppg
    add_total_projections.add_batter_total_projections(batters)
    add_total_projections.add_pitcher_total_projections(pitchers)

    # Merge into players
    players = batters.copy()
    players.update(pitchers)

    # Add Fantrax info
    add_fantrax.add_fantrax(players)

    # Save to pkl
    with open('batters.pkl', 'wb') as batter_file:
        pickle.dump(batters, batter_file, pickle.HIGHEST_PROTOCOL)

    with open('pitchers.pkl', 'wb') as pitcher_file:
        pickle.dump(pitchers, pitcher_file, pickle.HIGHEST_PROTOCOL)

    print 'Players successfully updated.', '\n'


def load_players():
    with open('batters.pkl', 'rb') as batter_file:
        batters = pickle.load(batter_file)

    with open('pitchers.pkl', 'rb') as pitcher_file:
        pitchers = pickle.load(pitcher_file)

    players = batters.copy()
    players.update(pitchers)

    return players, batters, pitchers
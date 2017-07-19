__author__ = 'brsch'

import TeamClass
import LeagueClass
import pickle


def update_league(players):

    teams = {}
    free_agents = []

    for player in players.values():
        team_name = player.status

        if team_name in ['WW', 'FA']:
            free_agents.append(player)

        else:
            if team_name in teams.keys():
                team = teams[team_name]
            else:
                team = TeamClass.Team(team_name)
                teams[team_name] = team

            team.add_player(player)

    league = LeagueClass.League(teams, free_agents, players)

    with open('league.pkl', 'wb') as league_file:
        pickle.dump(league, league_file, pickle.HIGHEST_PROTOCOL)

    print 'League successfully updated.', '\n'

    return league


def load_league():

    with open('league.pkl', 'rb') as league_file:
        league = pickle.load(league_file)

    return league
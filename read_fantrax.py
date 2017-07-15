__author__ = 'brsch'

import csv
import PlayerClass
import TeamClass
from read_ros import ros
from constants import fantrax_to_fangraphs_teams, fx_to_fg_name_conversions

players, teams = {}, {}

with open('Fantrax-players-Navy and Goldschmidt.csv', 'rb') as fntrx_file:
    reader = csv.reader(fntrx_file)
    first_row = True
    players_found = 0

    for row in reader:
        if first_row:
            name_i = row.index('Player')
            team_i = row.index('Team')
            pos_i = row.index('Position')
            status_i = row.index('Status')
            first_row = False
        else:
            name = row[name_i]
            try:
                last_name, first_name = name.rsplit(', ')
            except ValueError:
                pass
            name = '%s %s' % (first_name, last_name)

            fx_team = row[team_i]
            fg_team = fantrax_to_fangraphs_teams[fx_team]
            positions = row[pos_i].rsplit(',')
            status = row[status_i]

            if (name, fg_team) in ros.keys():
                player_ros = ros[(name, fg_team)]
                player = \
                    PlayerClass.Player(first_name, last_name, name, fx_team, fg_team, positions, status, player_ros)

                if status not in teams.keys():
                    team = TeamClass.Team(status)
                    teams[status] = team

                players[name] = player
                player_team = teams[status]
                player_team.add_player(player)

                del ros[(name, fg_team)]
            else:
                try:
                    first_name, last_name = fx_to_fg_name_conversions[name]
                    name = '%s %s' % (first_name, last_name)
                    player_ros = ros[(name, fg_team)]
                    player = \
                        PlayerClass.Player(first_name, last_name, name, fx_team, fg_team, positions, status, player_ros)

                    if status not in teams.keys():
                        team = TeamClass.Team(status)
                        teams[status] = team

                    players[name] = player
                    player_team = teams[status]
                    player_team.add_player(player)

                    del ros[(name, fg_team)]
                except KeyError:
                    pass  # We don't have projections for this player

if len(ros.keys()) > 0:
    for key in ros:
        print key, ros[key]
        print '%s players unmapped' % len(ros.keys())
        exit()

print 'Projections for %s players compiled' % len(players)

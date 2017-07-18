__author__ = 'brsch'

import csv
import PlayerClass
import TeamClass
from read_ros import ros, true_rps
from constants import fantrax_to_fangraphs_teams, fx_to_fg_name_conversions

"""
THIS SCRIPT IS USED TO READ IN THE MLB PLAYERS, THEIR POSITIONS AND CURRENT STATUSES (TEAM ASSIGNMENT, FREE AGENT OR 
WAIVER WIRE) AND COMBINE THIS WITH THE ros DICTIONARY FROM read_ros.py.

EACH PLAYER IS MADE INTO AN INSTANCE OF THE PLAYER CLASS AND ASSIGNED TO EITHER A TEAM, FREE AGENCY OR THE WAIVER WIRE.

EACH PLAYER IS PLACED INTO THE players DICTIONARY, WHOSE KEYS ARE PLAYER NAMES AND MLB TEAMS AND WHOSE VALUES ARE
PLAYER OBJECTS.

EACH TEAM IS PLACED INTO THE teams DICTIOANRY, WHOSE KEYS ARE THE NAME OF THE TEAMS ('FA' FOR FREE AGENCY, 'WW' FOR 
WAIVER WIRE') AND WHOSE VALUES ARE TEAM OBJECTS.
"""

players, teams = {}, {}

with open('Fantrax-players-Navy and Goldschmidt.csv', 'rb') as fntrx_file:
    reader = csv.reader(fntrx_file)
    first_row = True
    players_found = 0

    for row in reader:
        if first_row:
            # Grab header indices
            name_i = row.index('Player')
            team_i = row.index('Team')
            pos_i = row.index('Position')
            status_i = row.index('Status')
            first_row = False

        else:
            # Get player name
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

            # If name is found in Fangraphs database, create player
            if (name, fg_team) in ros.keys():
                player_ros = ros[(name, fg_team)]
                player = \
                    PlayerClass.Player(first_name, last_name, name, fx_team, fg_team, positions, status, player_ros)

                if (name, fg_team) in true_rps:
                    player.true_RP = True

                if status not in teams.keys():
                    team = TeamClass.Team(status)
                    teams[status] = team

                if (name, fg_team) in players.keys():
                    print 'DUPLICATE DETECTED: %s - %s' % (name, team)
                    print 'Current player: \n', players[(name, team)].__dict__
                    print 'Possible duplicate: \n', player.__dict__
                    exit()

                players[(name, fg_team)] = player
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
                    if (name, fg_team) in true_rps:
                        player.true_RP = True

                    if status not in teams.keys():
                        team = TeamClass.Team(status)
                        teams[status] = team
                    if (name, team) in players.keys():
                        print 'DUPLICATE DETECTED: %s - %s' % (name, team)
                        print 'Current player: \n', players[(name, team)].__dict__
                        print 'Possible duplicate: \n', player.__dict__
                        exit()

                    players[(name, fg_team)] = player
                    player_team = teams[status]
                    player_team.add_player(player)

                    del ros[(name, fg_team)]

                except KeyError:
                    pass  # We don't have projections for this player

if len(ros.keys()) > 0:
    for key in ros:
        print 'FANGRAPHS PLAYER %s, %s UNMAPPED' % (key, ros[key])
        # print '%s players unmapped' % len(ros.keys())
        # exit()
print '\n'

print 'Projections for %s players compiled \n' % len(players)


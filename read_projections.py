__author__ = 'brsch'

import csv
import PlayerClass
import constants

def read_batter_projections(players=None):
    players = {} if players is None else players

    with open('Batters DC.csv', 'rb') as batter_projections_file:
        players = read_projections_file(players, batter_projections_file, is_batter=True)

    print 'Depth Charts batter projections successfully loaded.', '\n'

    return players


def read_pitcher_projections(players=None):
    players = {} if players is None else players

    with open('Pitchers DC.csv', 'rb') as pitcher_projections_file:
        players = read_projections_file(players, pitcher_projections_file, is_batter=False)

    print 'Depth Charts pitcher projections successfully loaded.', '\n'

    return players


def read_projections_file(players, projections_file, is_batter):
    reader = csv.reader(projections_file)
    first_row = True

    for row in reader:
        if first_row:
            headers = row
            first_row = False

        else:
            playerid = row[headers.index('playerid')]

            if playerid in constants.nonfantrax_playerids:
                pass
            else:
                player = PlayerClass.Player(playerid)
                player.is_batter = is_batter

                for header in headers:

                    if header == 'playerid':
                        value = row[headers.index(header)]
                    else:
                        try:
                            value = float(row[headers.index(header)])
                        except ValueError:
                            value = row[headers.index(header)]

                    if '/' in header:
                        header = header.replace('/', '')

                    if header not in ['Name', 'Team', 'playerid']:
                        attr_str = 'proj_%s' % header
                    else:
                        attr_str = header
                    setattr(player, attr_str, value)

                if player.playerid in players.keys():
                    print 'Duplicate player detected: %s' % player.Name
                    if player.proj_G > players[player.playerid].proj_G:
                        players[player.playerid] = player
                    else:
                        pass
                else:
                    players[player.playerid] = player

                player.add_singles('proj')
                player.calc_points('proj')
                player.is_true_rp()

    return players
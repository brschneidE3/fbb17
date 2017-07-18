import csv

def add_batter_total_projections(players):

    with open('Batters TOT.csv', 'rb') as batter_total_projections_file:
        players = add_total_projections_file(players, batter_total_projections_file)

    return players

def add_pitcher_total_projections(players):

    with open('Pitchers TOT.csv', 'rb') as pitcher_total_projections_file:
        players = add_total_projections_file(players, pitcher_total_projections_file)

    return players

def add_total_projections_file(players, total_projections_file):
    reader = csv.reader(total_projections_file)
    first_row = True

    for row in reader:
        if first_row:
            headers = row
            first_row = False

        else:
            playerid = float(row[headers.index('playerid')])

            try:
                player = players[playerid]
            except KeyError:
                print 'playerid %s not found in total projections file.' % playerid
                exit()

            for header in headers:
                try:
                    value = float(row[headers.index(header)])
                except ValueError:
                    value = row[headers.index(header)]

                if header not in ['Name', 'Team', 'playerid']:
                    attr_str = 'tot_%s' % header
                    setattr(player, attr_str, value)

            player.add_singles()
            player.calc_seasontodate()
            player.calc_points()

    return players
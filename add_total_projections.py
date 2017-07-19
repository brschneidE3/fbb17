import csv


def add_batter_total_projections(players):

    with open('Batters DC ROS.csv', 'rb') as batter_total_projections_file:
        players = add_total_projections_file(players, batter_total_projections_file)

    return players


def add_pitcher_total_projections(players):

    with open('Pitchers DC ROS.csv', 'rb') as pitcher_total_projections_file:
        players = add_total_projections_file(players, pitcher_total_projections_file)

    return players


def add_total_projections_file(players, total_projections_file):
    reader = csv.reader(total_projections_file)
    first_row = True
    totals_missing = 0

    for row in reader:
        if first_row:
            headers = row
            first_row = False

        else:
            playerid = row[headers.index('playerid')]

            try:
                player = players[playerid]
            except KeyError:
                totals_missing += 1
                pass

            for header in headers:
                try:
                    value = float(row[headers.index(header)])
                except ValueError:
                    value = row[headers.index(header)]

                if header not in ['Name', 'Team', 'playerid']:
                    attr_str = 'tot_%s' % header
                    setattr(player, attr_str, value)

            player.add_singles('tot')
            player.calc_seasontodate()
            player.calc_points('tot')

    if player.is_batter:
        print '%s batters missing remaining projections.' % totals_missing
    else:
        print '%s pitchers missing remaining projections.' % totals_missing
    return players
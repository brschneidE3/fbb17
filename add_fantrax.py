
import csv

def add_fantrax(players):

    fantrax_data = load_fantrax_data()
    name_i = fantrax_data[0].index('Player')
    team_i = fantrax_data[0].index('Team')
    position_i = fantrax_data[0].index('Position')
    status_i = fantrax_data[0].index('Status')

    for player in players.values():
        name = player.Name
        team = find_fantrax_team(player.Team)

        data_row = get_fantrax_row(name, team, name_i, team_i, fantrax_data[1:])
        positions = data_row[position_i].rsplit(',')
        status = data_row[status_i]

        player.positions = positions
        player.status = status

def load_fantrax_data():
    fantrax_data = []

    with open('Fantrax-players-Navy and Goldschmidt.csv', 'rb') as fantrax_file:
        reader = csv.reader(fantrax_file)
        for row in reader:
            fantrax_data.append(row)

    return fantrax_data

def find_fantrax_team(fangraphs_team):
    fg_to_fx = {
        'Yankees': 'NYY',
        'Brewers': 'MIL',
        'Twins': 'MIN',
        'Marlins': 'MIA',
        'Braves': 'ATL',
        'Red Sox': 'BOS',
        'Athletics': 'OAK',
        'Reds': 'CIN',
        'Mets': 'NYM',
        'Orioles': 'BAL',
        'Rockies': 'COL',
        'Tigers': 'DET',
        'Rangers': 'TEX',
        'Blue Jays': 'TOR',
        'Mariners': 'SEA',
        'Pirates': 'PIT',
        'Cubs': 'CHC',
        'Cardinals': 'STL',
        'Indians': 'CLE',
        'Astros': 'HOU',
        'White Sox': 'CHW',
        'Nationals': 'WAS',
        '': '(N/A)',
        'Royals': 'KC',
        'Phillies': 'PHI',
        'Dodgers': 'LAD',
        'Rays': 'TB',
        'Angels': 'LAA',
        'Diamondbacks': 'ARI',
        'Giants': 'SF',
        'Padres': 'SD'}

    return fg_to_fx[fangraphs_team]

def name_match(fx_name, fg_name):
    try:
        if fx_name in ['Rougned Odor (Minors)', 'Zimmerman, Jordan P,']:
            pass

        else:
            last, first = fx_name.rsplit(', ')
            first = first.replace('.', '')
            last = last.replace('.', '')
            fg_name = fg_name.replace('.', '')

            if '%s %s' % (first, last) == fg_name:
                return True
            else:
                return False
    except:
        print 'Error when comparing %s and %s' % (fx_name, fg_name)
        exit()

def team_match(fx_team, fg_team):
    return fx_team == fg_team

def match(fx_name, fx_team, fg_name, fg_team):

    fg_to_fx = {
        ('Adam Wilk', 'MIN'): ('Wilk, Adam', '(N/A)'),
        ('Kiké Hernandez', 'LAD'): ('Hernandez, Kike', 'LAD')
    }

    if name_match(fx_name, fg_name) and team_match(fx_team, fg_team):
        return True
    elif (fg_name, fg_team) in fg_to_fx.keys():
        if (fx_name, fx_team) == fg_to_fx[(fg_name, fg_team)]:
            return True
    else:
        return False

def get_fantrax_row(fg_name, fg_team, name_i, team_i, fantrax_data):

    for row in fantrax_data:

        fx_name = row[name_i]
        fx_team = row[team_i]

        if match(fx_name, fx_team, fg_name, fg_team):
            return row
        else:
            pass

    print '%s on %s not found in Fantrax data.' % (fg_name, fg_team)
    exit()

import csv
import constants


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

    print 'Fantrax data successfully injected.', '\n'


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
        elif fx_name == 'Torres, Jose M.' and fg_name == 'Jose Torres':
            return True
        elif fx_name == 'Taylor, Michael A.' and fg_name == 'Michael Taylor':
            return True
        else:
            # Parse into first and last
            last, first = fx_name.rsplit(', ')

            # Change nickname
            first = first.replace('Matthew', 'Matt')
            fg_name = fg_name.replace('Matthew ', 'Matt ')
            fg_name = fg_name.replace('Cameron ', 'Cam ')
            first = first.replace('Cameron', 'Cam')
            first = first.replace('Samuel', 'Sam')
            fg_name = fg_name.replace('Samuel ', 'Sam ')
            first = first.replace('Michael', 'Mike')
            fg_name = fg_name.replace('Michael ', 'Mike ')
            first = first.replace('Jakob', 'Jake')
            fg_name = fg_name.replace('Jakob ', 'Jake ')
            first = first.replace('Nicholas', 'Nick')
            fg_name = fg_name.replace('Nicholas ', 'Nick ')
            first = first.replace('Daniel', 'Dan')
            fg_name = fg_name.replace('Daniel ', 'Dan ')
            first = first.replace('Gregory', 'Greg')
            fg_name = fg_name.replace('Gregory ', 'Greg ')
            first = first.replace('Zack', 'Zach')
            fg_name = fg_name.replace('Zack ', 'Zach ')
            first = first.replace('Joseph', 'Joe')
            fg_name = fg_name.replace('Joseph ', 'Joe ')
            first = first.replace('Mitchell', 'Mitch')
            fg_name = fg_name.replace('Mitchell ', 'Mitch ')
            first = first.replace('Chasen', 'Chase')
            fg_name = fg_name.replace('Chasen ', 'Chase ')

            if first != 'Jacoby':
                first = first.replace('Jacob', 'Jake')
            fg_name = fg_name.replace('Jacob ', 'Jake ')

            # Remove periods
            first = first.replace('.', '')
            last = last.replace('.', '')
            fg_name = fg_name.replace('.', '')

            # Remove Jr's
            last = last.replace(' Jr', '')
            fg_name = fg_name.replace(' Jr', '')

            # All lowercase
            first = first.lower()
            last = last.lower()
            fg_name = fg_name.lower()

            # Remove -'s
            first = first.replace('-', '')
            last = last.replace('-', '')
            fg_name = fg_name.replace('-', '')

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

    if name_match(fx_name, fg_name) and team_match(fx_team, fg_team):
        return True
    elif (fg_name, fg_team) in constants.fg_to_fx.keys():
        if (fx_name, fx_team) == constants.fg_to_fx[(fg_name, fg_team)]:
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
    print "('%s', '%s'): ('%s', '')," % (fg_name, fg_team, ', '.join(fg_name.rsplit(' ')[::-1]))
    exit()

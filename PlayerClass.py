from read_ros import ros


class Player:

    fantrax_to_fangraphs_teams = {
        '(N/A)': '',
        'ARI': 'Diamondbacks',
        'ATL': 'Braves',
        'BAL': 'Orioles',
        'BOS': 'Red Sox',
        'CHC': 'Cubs',
        'CHW': 'White Sox',
        'CIN': 'Reds',
        'CLEV': 'Indians',
        'COL': 'Rockies',
        'DET': 'Tigers',
        'HOU': 'Astros',
        'KC': 'Royals',
        'LAA': 'Angels',
        'LAD': 'Dodgers',
        'MIA': 'Marlins',
        'MIL': 'Brewers',
        'MIN': 'Twins',
        'NYM': 'Mets',
        'NYY': 'Yankees',
        'OAK': 'Athletics',
        'PHI': 'Phillies',
        'PIT': 'Pirates',
        'SD': 'Padres',
        'SEA': 'Mariners',
        'SF': 'Giants',
        'STL': 'Cardinals',
        'TB': 'Rays',
        'TEX': 'Rangers',
        'TOR': 'Blue Jays',
        'WAS': 'Nationals'
    }

    def __init__(self, first_name, last_name, fx_team, positions, status, ros):

        self.first_name = first_name
        self.last_name = last_name
        self.name = '%s %s' % (first_name, last_name)
        self.fx_team = fx_team
        self.fg_team = self.fantrax_to_fangraphs_teams[self.fx_team]
        self.positions = positions
        self.status = status

        self.ros_pts = ros[(self.name, self.fg_team)]
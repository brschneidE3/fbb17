__author__ = 'brsch'

fantrax_to_fangraphs_teams = {
    '(N/A)': '',
    'ARI': 'Diamondbacks',
    'ATL': 'Braves',
    'BAL': 'Orioles',
    'BOS': 'Red Sox',
    'CHC': 'Cubs',
    'CHW': 'White Sox',
    'CIN': 'Reds',
    'CLE': 'Indians',
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

fx_to_fg_name_conversions = {
    'Lance McCullers Jr.': ('Lance', 'McCullers'),
    'Shin-soo Choo': ('Shin-Soo', 'Choo'),
    'Yuli Gurriel': ('Yulieski', 'Gurriel'),
    'Nicholas Castellanos': ('Nick', 'Castellanos'),
    'Michael A. Taylor': ('Michael', 'Taylor'),
    'J.C. Ramirez': ('JC', 'Ramirez'),
    'Kike Hernandez': ('Kik\xc3\xa9', 'Hernandez'),
    'AJ Ramos': ('A.J.', 'Ramos'),
    'Jake Faria': ('Jacob', 'Faria'),
    'JT Riddle': ('J.T.', 'Riddle'),
    'Norichika Aoki': ('Nori', 'Aoki'),
    'Jose M. Torres': ('Jose', 'Torres'),
    'Nate Karns': ('Nathan', 'Karns'),
    'Daniel Vogelbach': ('Dan', 'Vogelbach'),
    'Eric Young Jr.': ('Eric', 'Young'),
    'Mike Martinez': ('Michael', 'Martinez'),
    'Cameron Perkins': ('Cam', 'Perkins'),
    'Sam Tuivailala': ('Samuel', 'Tuivailala'),
    'Jorge De La Rosa': ('Jorge', 'de la Rosa'),
    'Jake Junis': ('Jakob', 'Junis'),
    'Zack Granite': ('Zach', 'Granite'),
    'Dwight Smith Jr.': ('Dwight', 'Smith'),
    'Greg Bird': ('Gregory', 'Bird'),
    'Matthew Boyd': ('Matt', 'Boyd'),
    'Rubby De La Rosa': ('Rubby', 'de la Rosa'),
    'Mark Leiter Jr.': ('Mark', 'Leiter')
    }

starting_roster = {
    'C': 2,
    '1B': 1,
    '2B': 1,
    '3B': 1,
    'SS': 1,
    'CI': 1,
    'MI': 1,
    'OF': 5,
    'UT': 2,

    'SP': 3,
    'RP': 2,
    'P': 3
}

pos_scalar = {
    'C': 1.00001,
    '1B': 1.00001,
    '2B': 1.00001,
    '3B': 1.00001,
    'SS': 1.00001,
    'CI': 1,
    'MI': 1,
    'OF': 1.00001,
    'UT': 1,

    'SP': 1.00001,
    'RP': 1.00001,
    'P': 1
}
ordered_pos = ['C', '1B', '2B', '3B', 'SS', 'CI', 'MI', 'OF', 'UT', 'SP', 'RP', 'P']
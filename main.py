__author__ = 'brsch'

import get_players
import get_league
import constants
from coopr import pyomo

# players = get_players.update_players()
players, batters, pitchers = get_players.load_players()

# league = get_league.update_league(players)
league = get_league.load_league()

for player in players.values():
    if player.Name in ['Travis Shaw', 'Mike Moustakas', 'Yu Darvish']:
        print '%s : %s' % (player.Name, player.proj_points)
    elif 'Ryu' in player.Name:
        print '%s : %s' % (player.Name, player.proj_points)

# team = league.teams['MC']
# solved_opt = team.solve_max_points()
# max_points = team.get_max_points(solved_opt)
# for position in constants.ordered_pos:
#     print position
#     for player in solved_opt.players:
#         gp = pyomo.value(solved_opt.games_played[player, position])
#         if gp > 0:
#             print '\t %s:' % (player.Name)
#             print '\t games played: %s' % gp
#             print '\t proj g: %s' % player.proj_G
# exit()

# league.print_league_projections()
# league.find_optimal_lineup()
# league.value_by_position_heatmap(normalize_by_position=False)
# league.evaluate_trade('MC', give_playerids=['4892', '14444'], get_playerids=['11982', '13074'])
# league.print_FA_values('SP')



# for position in list(set([element.rsplit('_')[0] for element in constants.ordered_pos])):
#     league.teams['WHIT'].print_points_by_position(position, 'proj')
# league.teams['MC'].print_proj_by_position('P')

# league.print_mvp()
# solved_opt = league.teams['MC'].solve_max_points()
# league.teams['MC'].print_used(solved_opt)
# team = league.teams['MC']
# solved_opt = team.solve_max_points(team.players)
# team.print_used_by_pos(solved_opt, used_only=True)

# league.test_opt_size(upto=500, by=1)
# player = league.find_player_by_name('Anthony Alford')
# for element in player.__dict__:
#     print element, player.__dict__[element]


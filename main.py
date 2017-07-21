__author__ = 'brsch'

import get_players
import get_league
import operator

# players = get_players.update_players()
players, batters, pitchers = get_players.load_players()

# league = get_league.update_league(players)
league = get_league.load_league()
# league.print_league_projections()
# league.find_optimal_lineup()
# league.value_by_position_heatmap(normalize_by_position=False)
league.evaluate_trade('MC', give_playerids=['5401', '10816', '4810'], get_playerids=['9166', '4153'])
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

__author__ = 'brsch'

import get_players
import get_league

# players = get_players.update_players()
players, batters, pitchers = get_players.load_players()

# league = get_league.update_league(players)
league = get_league.load_league()

# league.value_by_position_heatmap(normalize_by_position=False)

# league.print_mvp()
# league.teams['MC'].print_games_played()

league.test_opt_size()
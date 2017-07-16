__author__ = 'brsch'

# For player in Fantrax:
    # Get position(s)
    # Get status

    # Find player in Pitchers/Batters ROS
        # Get ROS

    # Assign player to team (create team if doesn't exist)

# For team in league
    # Calculate optimal roster
        # Save to league results

    # Calculate remaining points by position
        # Team x Position heat map

    # Calculate impact of acquiring each player for each other player
        # fa_only param

# Trade calculator

from read_fantrax import players, teams
import LeagueClass

league = LeagueClass.League(teams=[team for team in teams.values() if team.name not in ['WW','FA']],
                            freeagencies=[team for team in teams.values() if team.name in ['WW', 'FA']])
# league.print_league_projections()
league.print_value_by_position()
# league.value_by_position_heatmap()

fa_team = teams['FA']
ww_team = teams['WW']

for team in league.teams:
    if team.name == 'MC':
        players = team.players + fa_team.players + ww_team.players
        solved_opt = team.solve_max_points(players)
        team.print_lineup()
        team.print_lineup(solved_opt)
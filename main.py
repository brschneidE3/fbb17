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

for team in teams.values():
    if team not in ['WW', 'FA']:
        print team.name.upper(), len(team.players)
        # for player in team.players:
        #     print player.name
        # print '\n'
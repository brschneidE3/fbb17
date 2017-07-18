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

import read_projections
import add_total_projections
import add_fantrax

# Add projections
batters = read_projections.read_batter_projections()
pitchers = read_projections.read_pitcher_projections()

# Add season totals, 1B's, season-to-date and calculate fantasy points and ppg
add_total_projections.add_batter_total_projections(batters)
add_total_projections.add_pitcher_total_projections(pitchers)

# Merge into players
players = batters.copy()
players.update(pitchers)

add_fantrax.add_fantrax(players)
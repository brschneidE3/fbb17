
import os
import csv

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

cwd = os.getcwd()

batters_ros = {}
with open('Batters ROS.csv', 'rb') as batterfile:
    reader = csv.reader(batterfile)
    first_row = True
    for row in reader:

        if first_row:
            name_i = row.index('Name')
            team_i = row.index('Team')
            h_i = row.index('H')
            doub_i = row.index('2B')
            trip_i = row.index('3B')
            hr_i = row.index('HR')
            r_i = row.index('R')
            rbi_i = row.index('RBI')
            bb_i = row.index('BB')
            k_i = row.index('SO')
            sb_i = row.index('SB')
            cs_i = row.index('CS')
            first_row = False

        else:
            name = row[name_i]
            team = row[team_i]
            h = float(row[h_i])
            doub = float(row[doub_i])
            trip = float(row[trip_i])
            hr = float(row[hr_i])
            r = float(row[r_i])
            rbi = float(row[rbi_i])
            bb = float(row[bb_i])
            k = float(row[k_i])
            sb = float(row[sb_i])
            cs = float(row[cs_i])

            sing = h - doub - trip - hr

            ros = calc_ros(sing=sing, doub=doub, trip=trip, hr=hr, r=r, rbi=rbi, b_bb=bb, b_k=k, sb=sb, sb=cs)
            batters_ros[(name, team)] = ros


class Player:

    def __init__(self, first_name, last_name, fg_playerid, positions, status, ros):

        self.first_name = first_name
        self.last_name = last_name
        self.fg_playerid = fg_playerid
        self.positions = positions
        self.status = status

        self.ros_pts = self.get_ros()

    def get_ros(self):

        if 'p' in self.positions:
            return
        else:
            return batters_ros[(name, team)]
__author__ = 'brsch'

import csv


def calc_batter_ros(sing, doub, trip, hr, r, rbi, bb, k, sb, cs):
    return 2*doub + 3*trip + hr*4 + r + rbi + bb - 0.5*k + 2*sb - cs + sing


def calc_pitcher_ros(w, l, ip, h, er, k, bb):
    return 5*w - 3*l + 2*ip - 0.5*h - 2*er + k - 0.5*bb

ros = {}
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

            player_ros = calc_batter_ros(sing=sing, doub=doub, trip=trip, hr=hr, r=r, rbi=rbi, bb=bb, k=k, sb=sb, cs=cs)
            if (name, team) in ros.keys():
                print 'Duplicate player: %s - %s' % (name, team)
            else:
                ros[(name, team)] = player_ros

pitchers_ros = {}
with open('Pitchers ROS.csv', 'rb') as pitcherfile:
    reader = csv.reader(pitcherfile)
    first_row = True

    for row in reader:
        if first_row:
            name_i = row.index('Name')
            team_i = row.index('Team')
            w_i = row.index('W')
            l_i = row.index('L')
            ip_i = row.index('IP')
            h_i = row.index('H')
            er_i = row.index('ER')
            k_i = row.index('SO')
            bb_i = row.index('BB')
            first_row = False

        else:
            name = row[name_i]
            team = row[team_i]
            w = float(row[w_i])
            l = float(row[l_i])
            ip = float(row[ip_i])
            h = float(row[h_i])
            er = float(row[er_i])
            k = float(row[k_i])
            bb = float(row[bb_i])

            player_ros = calc_pitcher_ros(w, l, ip, h, er, k, bb)
            if (name, team) in ros.keys():
                print 'Duplicate player: %s - %s' % (name, team)
            else:
                ros[(name, team)] = player_ros
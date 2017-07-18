
import numpy

class Player:

    cumulative_attrs = ['G', 'H', 'HR', 'SO', 'BB', 'WAR', # Batters & pitchers
                        'PA', 'AB', '1B', '2B', '3B', 'R', 'RBI', 'HBP', 'SB', 'CS',  # Just batters
                        'W', 'L', 'GS', 'IP', 'ER']  # Just pitchers

    calculated_attrs = ['AVG', 'OBP', 'SLG', 'OPS',  # Just batters
                        'ERA', 'WHIP', 'K/9', 'BB/9']  # Just pitchers

    batter_scored_stats = {
        '1B':  1,
        '2B': 2,
        '3B': 3,
        'HR': 4,
        'R': 1,
        'RBI': 1,
        'BB': 1,
        'SO': -0.5,
        'SB': 2,
        'CS': -1
    }

    pitcher_scored_stats = {
        'W': 5,
        'L': 3,
        'IP': 2,
        'H': -0.5,
        'ER': -2,
        'SO': 1,
        'BB': -0.5
    }

    def __init__(self, playerid):

        self.playerid = playerid

    def add_singles(self):
        try:
            self.proj_1B = self.proj_H - self.proj_2B - self.proj_3B - self.proj_HR
            self.tot_1B = self.tot_H - self.tot_2B - self.tot_3B - self.tot_HR
        except AttributeError:
            pass

    def calc_seasontodate(self):

        for attr in self.cumulative_attrs:
            tot_attr = 'tot_%s' % attr
            proj_attr = 'proj_%s' % attr

            try:
                tot = getattr(self, tot_attr)
                proj = getattr(self, proj_attr)
                std = tot - proj
                setattr(self, 'std_%s' % attr, std)

            except AttributeError:
                pass

        self.calc_std_avg()
        self.calc_std_obp()
        self.calc_std_slg()
        self.calc_std_ops()
        self.calc_std_era()
        self.calc_std_whip()
        self.calc_std_k9()
        self.calc_std_bb9()

    def calc_points(self):
        for portion in ['tot', 'proj', 'std']:
            points = 0

            if self.is_batter:
                stat_weights = self.batter_scored_stats
            else:
                stat_weights = self.pitcher_scored_stats

            for stat in stat_weights.keys():
                weight = stat_weights[stat]
                stat_name = '%s_%s' % (portion, stat)

                try:
                    quantity = getattr(self, stat_name)
                    points += quantity*weight

                except AttributeError:
                    pass

            points_name = '%s_points' % portion
            setattr(self, points_name, points)

            ppg_name = '%s_ppg' % portion
            g_name = '%s_G' % portion
            g = getattr(self, g_name)
            ppg = points / g
            setattr(self, ppg_name, ppg)

    def calc_std_avg(self):
        try:
            self.std_AVG = self.std_H / self.std_AB
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_AVG = numpy.nan

    def calc_std_obp(self):
        try:
            self.std_OBP = (self.std_H + self.std_BB + self.std_HBP) / self.std_PA
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_OBP = numpy.nan

    def calc_std_slg(self):
        try:
            self.std_SLG = (self.std_1B + 2.0*self.std_2B + 3.0*self.std_3B + 4.0*self.std_HR) / self.std_AB
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_SLG = numpy.nan

    def calc_std_ops(self):
        try:
            self.std_OPS = self.std_OBP + self.std_SLG
        except AttributeError:
            pass

    def calc_std_era(self):
        try:
            self.std_ERA = (self.std_ER/self.std_IP) * 9.0
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_ERA = numpy.nan

    def calc_std_whip(self):
        try:
            self.std_WHIP = (self.std_H + self.std_BB) / self.std_IP
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_WHIP = numpy.nan

    def calc_std_k9(self):
        try:
            self.std_K9 = (self.std_K / self.std_IP) * 9.0
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_K9 = numpy.nan

    def calc_std_bb9(self):
        try:
            self.std_BB9 = (self.std_BB / self.std_IP) * 9.0
        except AttributeError:
            pass
        except ZeroDivisionError:
            self.std_BB9 = numpy.nan
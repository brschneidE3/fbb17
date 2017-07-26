__author__ = 'brsch'

from coopr import pyomo
from tabulate import tabulate
import constants
import operator
import numpy


class Team:

    def __init__(self, name):

        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def solve_max_points(self, players=None):
        model = self.maximize_points(players)
        opt = pyomo.SolverFactory('cbc')
        opt.solve(model)
        return model

    def get_max_points(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt
        return pyomo.value(solved_opt.objective)

    def print_points_by_position(self, pos='P', portion='proj'):
        players_points = []

        for player in self.players:
            if pos in player.positions:
                try:
                    points = getattr(player, '%s_points' % portion)
                except AttributeError:
                    points = numpy.nan
                players_points.append((player.Name, points))

        sorted_pp = sorted(players_points, key=operator.itemgetter(1), reverse=True)
        print '%s - %s' % ("Player", pos)
        for name, points in sorted_pp:
            print '%s - %s' % (name, points)
        print '\n'

    def print_games_played(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt

        for player in solved_opt.players:
            player_total = 0
            for position in solved_opt.positions:
                games_played = pyomo.value(solved_opt.games_played[player, position])
                if games_played > 0:
                    print '%s - %s: %s' % (player.Name, position, games_played)
                player_total += games_played

    def get_games_played(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt
        games_played_dict = {}

        for player in solved_opt.players:
            player_total = 0
            for position in solved_opt.positions:
                games_played = pyomo.value(solved_opt.games_played[player, position])
                player_total += games_played
            games_played_dict[player] = player_total
        return games_played_dict

    def get_lineup(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt
        lineup = {}

        for position in constants.ordered_pos:
            new_row = []
            for player in solved_opt.players:
                if pyomo.value(solved_opt.games_played[player, position]) > 0:
                    new_row.append(player)
            lineup[position] = new_row

        return lineup

    def print_lineup(self, solved_opt=None):
        lineup = self.get_lineup(solved_opt)

        for position in constants.ordered_pos:
            starters = [player.Name for player in lineup[position]]
            print '%s: %s' % (position, tuple(starters))

    def print_used(self, solved_opt=None, used_only=False):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt
        total_used = 0
        for player in solved_opt.players:
            used = pyomo.value(solved_opt.used[player])
            if used:
                print '%s - %s' % (player.Name, used)
            else:
                if not used_only:
                    print '%s - %s' % (player.Name, used)
            total_used += used
        print 'Total - %s' % total_used

    def print_used_by_pos(self, solved_opt=None, used_only=False):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt
        total_used = 0
        for position in constants.ordered_pos:
            print position
            for player in solved_opt.players:
                gp = pyomo.value(solved_opt.games_played[player, position])
                if gp:
                    print '\t %s - %s' % (player.Name, gp)
                else:
                    if not used_only:
                        print '\t %s - %s' % (player.Name, gp)
                total_used += (gp > 0)
        print 'Total - %s' % total_used

    def value_by_position(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt

        val_by_pos = {}
        for position in solved_opt.positions:
            val_by_pos[position] = 0
            for player in solved_opt.players:
                val_by_pos[position] += pyomo.value(solved_opt.games_played[player, position])*player.proj_ppg
            val_by_pos[position] = val_by_pos[position]/constants.starting_roster[position]  # per player
        return val_by_pos

    def maximize_points(self, players=None):
        model = pyomo.ConcreteModel()
        model.starting_roster = constants.starting_roster
        model.positions = [position for position in model.starting_roster.keys()]

        model.players = self.players if players is None else players

        # Decision variable: who is being used?
        model.used = pyomo.Var(model.players, within=pyomo.Binary)
        model.used_by_pos = pyomo.Var(model.players, model.positions, within=pyomo.Binary)

        # Decision variable: who is playing what position?
        model.games_played = pyomo.Var(model.players, model.positions, within=pyomo.NonNegativeIntegers)

        # Limit number of players used
        model.cap_players_used = pyomo.Constraint(rule=self.cap_players_used)

        # Limit starting roster
        model.limit_roster_rule = pyomo.Constraint(model.positions, rule=self.limit_roster)

        # Limit positions players can play
        model.limit_positions_rule = pyomo.Constraint(model.players, model.positions, rule=self.limit_positions)

        # Limit to 1 position per player
        model.limit_playtime_rule = pyomo.Constraint(model.players, rule=self.limit_playtime)
        model.limit_playtime_bypos_rule1 = \
            pyomo.Constraint(model.players, model.positions, rule=self.limit_playtime_bypos1)
        model.limit_playtime_bypos_rule2 = \
            pyomo.Constraint(model.players, model.positions, rule=self.limit_playtime_bypos2)

        # Only true RP play RP - due to starts limit
        model.only_true_rp_rule1 = pyomo.Constraint(model.players, rule=self.only_true_rp1)
        model.only_true_rp_rule2 = pyomo.Constraint(model.players, rule=self.only_true_rp2)

        # Constrain which players can be modeled as 'replaceable' to fill out remaining playing time at position
        model.limit_replaceability = pyomo.Constraint(model.players, model.positions, rule=self.limit_replaceability)

        # Objective function
        model.objective = pyomo.Objective(rule=self.objective, sense=pyomo.maximize)

        return model

    @staticmethod
    def objective(model):
        # Maximize the points scored by the roster
        return sum(
            player.proj_ppg*model.games_played[player, position]*constants.pos_scalar[position]
               for position in model.positions
               for player in model.players
            )

    @staticmethod
    def only_true_rp1(model, player):
        # Only pitchers with no projected GS can play RP
        if player.true_rp:
            return pyomo.Constraint.Feasible
        else:
            return model.games_played[player, 'RP_1'] == 0

    @staticmethod
    def only_true_rp2(model, player):
        # Only pitchers with no projected GS can play RP
        if player.true_rp:
            return pyomo.Constraint.Feasible
        else:
            return model.games_played[player, 'RP_2'] == 0

    @staticmethod
    def limit_playtime(model, player):
        # Players can't play more than their projected games
        return sum(model.games_played[player, position] for position in model.positions) <= player.proj_G*model.used[player]

    @staticmethod
    def cap_players_used(model):
        return sum(model.used[player] for player in model.players) <= 32

    @staticmethod
    def limit_roster(model, position):
        # Players can't play more games than remain in the schedule
        return sum(model.games_played[player, position] for player in model.players) <= constants.games_per_pos[position]

    @staticmethod
    def limit_positions(model, player, position):
        # Players can only play at eligible positions
        if position.rsplit('_')[0] in player.positions:
            return pyomo.Constraint.Feasible
        else:
            return model.used_by_pos[player, position] == 0

    @staticmethod
    def limit_playtime_bypos2(model, player, position):
        # Creates a used variable indexed by position; superfluous constraint
        return model.used_by_pos[player, position] <= model.games_played[player, position]

    @staticmethod
    def limit_playtime_bypos1(model, player, position):
        # Creates a used variable indexed by position; superfluous constraint
        return model.games_played[player, position] <= player.proj_G*model.used_by_pos[player, position]

    @staticmethod
    def limit_replaceability(model, player, position):
        if not player.replaceable:
            return \
                sum(model.used_by_pos[otherplayer, position] for otherplayer in model.players if otherplayer != player) \
                <= (1 - model.used_by_pos[player, position])*constants.games_per_pos[position]
        else:
            return pyomo.Constraint.Feasible
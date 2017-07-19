__author__ = 'brsch'

from coopr import pyomo
from tabulate import tabulate
import constants


class Team:

    def __init__(self, name):

        self.name = name
        self.players = []

    def add_player(self, player):

        self.players.append(player)

    def solve_max_points(self, players=None):
        model = self.maximize_points(players)
        opt = pyomo.SolverFactory('cbc')
        results = opt.solve(model)
        return model

    def get_max_points(self, players=None):
        model = self.solve_max_points(players)
        return pyomo.value(model.objective)

    def print_games_played(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt

        for player in solved_opt.players:
            for position in solved_opt.positions:
                games_played = pyomo.value(solved_opt.games_played[player, position])
                if games_played > 0:
                    print '%s - %s: %s' % (player.Name, position, games_played)

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
        model.positions = {position for position in model.starting_roster.keys()}

        model.players = self.players if players is None else players

        # Decision variable: who is playing what position?
        model.games_played = pyomo.Var(model.players, model.positions, within=pyomo.NonNegativeIntegers)

        # Limit starting roster
        model.limit_roster_rule = pyomo.Constraint(model.positions, rule=self.limit_roster)

        # Limit positions players can play
        model.limit_positions_rule = pyomo.Constraint(model.players, model.positions, rule=self.limit_positions)

        # Limit to 1 position per player
        model.limit_playtime_rule = pyomo.Constraint(model.players, rule=self.limit_playtime)

        # Only true RP play RP - due to starts limit
        model.only_true_rp_rule = pyomo.Constraint(model.players, rule=self.only_true_rp)

        # Objective function
        model.objective = pyomo.Objective(rule=self.objective, sense=pyomo.maximize)

        return model

    @staticmethod
    def objective(model):
        # Maximize the points scored by the roster
        return sum(player.proj_ppg*model.games_played[player, position]*constants.pos_scalar[position]
                   for position in model.positions
                   for player in model.players)

    @staticmethod
    def limit_roster(model, position):
        # Players can't play more games than remain in the schedule
        return sum(model.games_played[player, position] for player in model.players) <= \
            model.starting_roster[position]*constants.games_per_pos[position]

    @staticmethod
    def limit_positions(model, player, position):
        # Players can only play at eligible positions
        if position in player.positions:
            return pyomo.Constraint.Satisfied
        else:
            return model.games_played[player, position] == 0

    @staticmethod
    def limit_playtime(model, player):
        # Players can't play more than their projected games
        return sum(model.games_played[player, position] for position in model.positions) <= player.proj_G

    @staticmethod
    def only_true_rp(model, player):
        # Only pitchers with no projected GS can play RP
        if player.true_rp:
            return pyomo.Constraint.Satisfied
        else:
            return model.games_played[player, 'RP'] == 0

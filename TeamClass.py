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

    def maximize_points(self, players=None):
        model = pyomo.ConcreteModel()
        model.starting_roster = constants.starting_roster
        model.positions = {position for position in model.starting_roster.keys()}

        model.players = self.players if players is None else players

        # Decision variable: who is playing what position?
        model.playing = pyomo.Var(model.players, model.positions, within=pyomo.Binary)

        # Limit starting roster
        model.limit_roster = pyomo.Constraint(model.positions, rule=self.limit_roster)

        # Limit positions players can play
        model.limit_positions = pyomo.Constraint(model.players, model.positions, rule=self.limit_positions)

        # Limit to 1 position per player
        model.limit_playtime = pyomo.Constraint(model.players, rule=self.limit_playtime)

        # Only true RP play RP - due to starts limit
        model.only_true_rp = pyomo.Constraint(model.players, rule=self.only_true_rp)

        # Objective function
        model.objective = pyomo.Objective(rule=self.objective, sense=pyomo.maximize)

        return model

    def solve_max_points(self, players=None):
        model = self.maximize_points(players)
        opt = pyomo.SolverFactory('cbc')
        results = opt.solve(model)
        return model

    def get_max_points(self, players=None):
        model = self.solve_max_points(players)
        return pyomo.value(model.objective)

    def print_playing_table(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt

        starting_players = []
        for player in solved_opt.players:
            for position in solved_opt.positions:
                if pyomo.value(solved_opt.playing[player, position]) > 0:
                    starting_players.append(player)

        headers = ['Pos'] + [player.name for player in starting_players]
        playing_assignments = []
        for position in constants.ordered_pos:
            new_row = [position]
            for player in starting_players:
                new_row.append(pyomo.value(solved_opt.playing[player, position]))
            playing_assignments.append(new_row)
        print tabulate(playing_assignments, headers=headers)

    def print_lineup(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt
        lineup = []

        for position in constants.ordered_pos:
            new_row = [position]
            for player in solved_opt.players:
                if pyomo.value(solved_opt.playing[player, position]) > 0:
                    new_row.append('%s - %s' % (player.name, player.ros_pts))
            lineup.append(new_row)

        for row in lineup:
            print row

    def value_by_position(self, solved_opt=None):
        solved_opt = self.solve_max_points() if solved_opt is None else solved_opt

        val_by_pos = {}
        for position in solved_opt.positions:
            val_by_pos[position] = 0
            for player in solved_opt.players:
                val_by_pos[position] += pyomo.value(solved_opt.playing[player, position])*player.ros_pts
            val_by_pos[position] = val_by_pos[position]/constants.starting_roster[position] # per player
        return val_by_pos


    @staticmethod
    def objective(model):
        return sum(player.ros_pts*model.playing[player, position]*constants.pos_scalar[position]
                   for position in model.positions
                   for player in model.players)

    @staticmethod
    def limit_roster(model, position):
        return sum(model.playing[player, position] for player in model.players) <= model.starting_roster[position]

    @staticmethod
    def limit_positions(model, player, position):
        return model.playing[player, position] <= (position in player.positions)

    @staticmethod
    def limit_playtime(model, player):
        return sum(model.playing[player, position] for position in model.positions) <= 1

    @staticmethod
    def only_true_rp(model, player):
        return model.playing[player, 'RP'] <= player.true_RP
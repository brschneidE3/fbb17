import operator
import time
import matplotlib.pyplot as plt
import constants
from tabulate import tabulate
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='brschneid7', api_key='VATAGfhAqpMWkkSd0j8l')


class League:

    def __init__(self, teams, freeagents, players):

        self.teams = teams
        self.freeagents = freeagents
        self.players = players

    def get_league_projections(self):
        projections = {}
        for team in self.teams.values():
            max_pts = team.get_max_points()
            projections[team.name] = max_pts

        return projections

    def print_league_projections(self, projections=None):

        projections = self.get_league_projections() if projections is None else projections

        sorted_projections = sorted(projections.items(), key=operator.itemgetter(1), reverse=True)
        place = 1
        for team, total in sorted_projections:
            print '(%s) %s - %s' % (place, team, total)
            place += 1

    def get_value_by_position(self):
        val_by_pos = {}

        for team in self.teams.values():
            team_val_by_pos = team.value_by_position()
            val_by_pos[team.name] = team_val_by_pos

        return val_by_pos

    def print_FA_values(self, pos):
        pos_players = {}
        for player in self.players.values():
            if pos in player.positions and player.status == 'FA':
                pos_players[player.Name] = player.proj_points
        sorted_players = sorted(pos_players.items(), key=operator.itemgetter(1), reverse=True)
        for name, points in sorted_players:
            print name, points


    def print_value_by_position(self):
        val_by_pos = self.get_value_by_position()

        headers = ['Pos'] + [team.name for team in self.teams.values()]
        val_by_pos_table = []
        for position in constants.ordered_pos:
            new_row = [position]
            for team in self.teams.values():
                new_row.append(val_by_pos[team.name][position])
            val_by_pos_table.append(new_row)

        print tabulate(val_by_pos_table, headers), '\n'

    def value_by_position_heatmap(self, normalize_by_position=False):
        val_by_pos = self.get_value_by_position()

        if normalize_by_position:
            val_by_pos_norm = {}

            for team_name in val_by_pos.keys():
                val_by_pos_norm[team_name] = {}

                for pos in val_by_pos[team_name].keys():
                    pos_total = 0

                    for name in self.teams.keys():
                        pos_total += val_by_pos[name][pos]

                    norm_value = val_by_pos[team_name][pos] / pos_total
                    val_by_pos_norm[team_name][pos] = norm_value

            val_by_pos = val_by_pos_norm

        trace = go.Heatmap(z=[[val_by_pos[team.name][position] for team in self.teams.values()]
                              for position in constants.ordered_pos],
                           x=[team.name for team in self.teams.values()],
                           y=constants.ordered_pos)
        data = [trace]
        py.iplot(data, filename='labelled-heatmap')

    def get_lineups(self):
        lineups = {}

        for team in self.teams.values():
            team_name = team.name
            lineup = team.get_lineup()
            lineups[team_name] = lineup

        return lineups

    def find_player_by_name(self, name):
        for player in self.players.values():
            if player.Name == name:
                return player

    def test_opt_size(self, upto=500, by=1):
        team = self.teams.values()[0]

        players = []
        times = []

        for fas_added in range(0, upto, by):
            num_players = len(team.players) + fas_added + 1
            next_player_added = self.freeagents[fas_added]
            print 'adding player %s' % next_player_added.Name
            start = time.time()
            opt_result = team.solve_max_points(team.players + self.freeagents[0:fas_added + 1])
            finish = time.time()
            elapsed = finish - start
            print '%s seconds to solve for %s players' % (elapsed, num_players)
            players.append(num_players)
            times.append(elapsed)

        plt.plot(players, times)
        plt.show()

    def find_optimal_lineup(self, team_name='MC', starting_opt=None):
        team = self.teams[team_name]
        best_opt = team.solve_max_points() if starting_opt is None else starting_opt
        best_value = team.get_max_points(best_opt)
        best_team = best_opt.players
        freeagents_inspected = 0

        for freeagent in self.freeagents:
            if freeagent.proj_ppg < min(player.proj_ppg for player in team.players) and \
                freeagent.proj_points < min(player.proj_points for player in team.players):
                pass
            else:
                try:
                    new_opt = team.solve_max_points(best_team + [freeagent])
                    new_value = team.get_max_points(new_opt)

                except ValueError:
                    print freeagent.proj_ppg

                if new_value > best_value:
                    best_value = new_value
                    best_opt = new_opt
                    print '%s free agents inspected. Current best value: %s' % (freeagents_inspected, best_value)

                    least_used_player = sorted(team.get_games_played(new_opt).items(), key=operator.itemgetter(1),
                                                 reverse=True)[-1][0]
                    best_team = [element for element in best_team if element != least_used_player]
                else:
                    best_team = [element for element in best_team if element != freeagent]

            freeagents_inspected += 1


        team.print_used_by_pos(best_opt, used_only=True)
        return best_opt

    def evaluate_trade(self, team_name, get_playerids, give_playerids):
        team = self.teams[team_name]
        without_trade_opt = self.find_optimal_lineup(team_name)
        without_trade_value = team.get_max_points(without_trade_opt)

        get_players = [self.players[playerid] for playerid in get_playerids]
        give_players = [self.players[playerid] for playerid in give_playerids]
        with_trade_players = [player for player in team.players if player not in give_players] + get_players
        starting_with_trade_opt = team.solve_max_points(with_trade_players)
        with_trade_opt = self.find_optimal_lineup(starting_opt=starting_with_trade_opt)
        with_trade_value = team.get_max_points(solved_opt=with_trade_opt)

        trade_value = with_trade_value - without_trade_value
        print 'Proposed trade:'
        print [player.Name for player in give_players]
        print 'for'
        print [player.Name for player in get_players]
        print ' is worth %s points' % int(trade_value)

    def find_mvp(self):
        mvps = {}

        for team in self.teams.values():
            opt_solution = team.solve_max_points(team.players + self.freeagents)
            points = team.get_max_points(opt_solution)
            print 'Optimizing for %s' % team.name

            total_players = len(team.players)
            players_evaluated = 0

            for i in range(total_players):
                player = team.players[i]
                players_minus_one = team.players[:i] + team.players[i+1:] + self.freeagents
                solution_minus_one = team.solve_max_points(players_minus_one)
                points_minus_one = team.get_max_points(solution_minus_one)
                value = points - points_minus_one
                mvps[(team.name, player.Name)] = value

                players_evaluated += 1
                print '\t %s of %s players evaluated (%s worth %s)' % \
                      (players_evaluated, total_players, player.Name, int(value))

        return mvps

    def print_mvp(self):
        mvps = self.find_mvp()
        sorted_mvps = sorted(mvps.items(), key=operator.itemgetter(1), reverse=True)

        for key, value in sorted_mvps:
            team_name, player_name = key
            print '%s - %s, %s' % (value, player_name, team_name)
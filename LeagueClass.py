import operator
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

    def find_mvp(self):
        mvps = {}

        for team in self.teams.values():
            points = team.get_max_points(team.players + self.freeagents)
            print 'Optimizing for %s' % team.name

            total_players = len(team.players)
            players_evaluated = 0

            for i in range(total_players):
                player = team.players[i]
                players_minus_one = team.players[:i] + team.players[i+1:] + self.freeagents
                points_minus_one = team.get_max_points(players_minus_one)
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
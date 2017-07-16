import operator
import constants
from tabulate import tabulate
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='brschneid7', api_key='VATAGfhAqpMWkkSd0j8l')

class League:

    def __init__(self, teams, freeagencies):
        self.teams = teams
        self.freeagencies = freeagencies

    def print_league_projections(self):
        projections = {}
        for team in self.teams:
            max_pts = team.get_max_points()
            projections[team.name] = max_pts
        sorted_projections = sorted(projections.items(), key=operator.itemgetter(1), reverse=True)
        place = 1
        for team, total in sorted_projections:
            print '(%s) %s - %s' % (place, team, total)
            place += 1

    def get_value_by_position(self):
        val_by_pos = {}

        for team in self.teams:
            team_val_by_pos = team.value_by_position()
            val_by_pos[team.name] = team_val_by_pos

        return val_by_pos

    def print_value_by_position(self):
        val_by_pos = self.get_value_by_position()

        headers = ['Pos'] + [team.name for team in self.teams]
        val_by_pos_table = []
        for position in constants.ordered_pos:
            new_row = [position]
            for team in self.teams:
                new_row.append(val_by_pos[team.name][position])
            val_by_pos_table.append(new_row)

        print tabulate(val_by_pos_table, headers)

    def value_by_position_heatmap(self):
        val_by_pos = self.get_value_by_position()
        trace  = go.Heatmap(z=[[val_by_pos[team.name][position] for team in self.teams]
                               for position in constants.ordered_pos],
                            x=[team.name for team in self.teams],
                            y=constants.ordered_pos)
        data = [trace]
        py.iplot(data, filename='labelled-heatmap')
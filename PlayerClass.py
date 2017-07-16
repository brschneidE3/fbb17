

class Player:

    def __init__(self, first_name, last_name, name, fx_team, fg_team, positions, status, player_ros):

        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.fx_team = fx_team
        self.fg_team = fg_team
        self.positions = positions
        self.status = status

        self.ros_pts = player_ros

        self.true_RP = False  # Flag to tell if an actual RP

    def __init__(self, name, team, positions, status):

        pass

    def add_stats(self, g):
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt

class HexGame:
    def __init__(self):
        self.possible_node_pairs = ['AB', 'BA', 'AC', 'CA', 'AD', 'DA', 'AE', 'EA', 'AF', 'FA',
                                    'BC', 'CB', 'BD', 'DB', 'BE', 'EB', 'BF', 'FB', 'CD', 'DC',
                                    'CE', 'EC', 'CF', 'FC', 'DE', 'ED', 'DF', 'FD', 'EF', 'FE']
        self.node_set = ['A', 'B', 'C', 'D', 'E', 'F']
        self.bad_pair = False
        self.coord_dict = {'A': [0, 2], 'B': [1, 0], 'C': [3, 0], 'D': [4, 2], 'E': [3, 4], 'F': [1, 4]}
        #Arrays used for the matplotlib display:
        self.x = [0, 1, 3, 4, 3, 1]
        self.y = [2, 0, 0, 2, 4, 4]
        self.n = ['A', 'B', 'C', 'D', 'E', 'F']
        self.past_plays = []

    def _reset_map(self):
        self.map = {"A": ' ',
                    'B': ' ',
                    'C': ' ',
                    'D': ' ',
                    'E': ' ',
                    'F': ' '}
        self.possible_node_pairs = ['AB', 'BA', 'AC', 'CA', 'AD', 'DA', 'AE', 'EA', 'AF', 'FA',
                                    'BC', 'CB', 'BD', 'DB', 'BE', 'EB', 'BF', 'FB', 'CD', 'DC',
                                    'CE', 'EC', 'CF', 'FC', 'DE', 'ED', 'DF', 'FD', 'EF', 'FE']

    def _triangle_formed(self):
        node0 = self.node_pair[0]
        node1 = self.node_pair[1]
        for i in self.map[node0]:
            if i == node1:
                continue
            if i in self.map[node1]:
                return True
        return False  # this should check whether or not someone won

    def _show_map_state(self):
        print(self.map)
        print(f'Available node pairs to play:{self.possible_node_pairs}')

    def _find_unconnectables(self):
        # these are the node pairs that can no longer be used as a result of the latest line being formed
        ind1, ind2 = self.node_set.index(self.node_pair[0]), self.node_set.index(self.node_pair[1])
        start_index = max(ind1, ind2)
        end_index = min(ind1, ind2)
        # print("start and end letters:", self.node_set[start_index],self.node_set[end_index])
        unconnected1 = []
        for i in range(start_index + 1, 6):
            unconnected1.append(self.node_set[i])
        for i in range(0, end_index):
            unconnected1.append(self.node_set[i])
        # print("unc1:",unconnected1)
        unconnected2 = [self.node_set[i] for i in range(end_index + 1, start_index)]
        # print("unc2:",unconnected2)
        unconnectables = [self.node_pair, self.node_pair[::-1]]
        for i in unconnected1:
            for j in unconnected2:
                unconnectables.append(f'{i}{j}')
                unconnectables.append(f'{j}{i}')
        # print(f"unconnnectables = {unconnectables}")
        self.possible_node_pairs = [item for item in self.possible_node_pairs if item not in unconnectables]

    def _check_node_pair(self):
        if self.node_pair not in self.possible_node_pairs: #the pair cannot be played
            self.node_pair = input(
                "The two provided nodes are invalid given the current game state; try a different set of nodes:")
            self._check_node_pair()
        return

    def _update_map(self):
        self._find_unconnectables()
        if self.map[self.node_pair[0]] != ' ':
            self.map[self.node_pair[0]] = self.map[self.node_pair[0]] + self.node_pair[1]
        else:
            self.map[self.node_pair[0]] = self.node_pair[1]
        if self.map[self.node_pair[1]] != ' ':
            self.map[self.node_pair[1]] = self.map[self.node_pair[1]] + self.node_pair[0]
        else:
            self.map[self.node_pair[1]] = self.node_pair[0]

    def _update_display(self):
        fig, ax = plt.subplots()
        ax.scatter(self.x, self.y, s=100)
        plt.axis('off')
        for i, txt in enumerate(self.n):
            ax.annotate(txt, (self.x[i] - 0.1, self.y[i] + 0.2))
        if len(self.past_plays)>0:
            for j in self.past_plays:
                start_coord = self.coord_dict[j[0]]
                end_coord = self.coord_dict[j[1]]
                ax.plot([start_coord[0], end_coord[0]], [start_coord[1], end_coord[1]], color="black")
        plt.show()

    def _play_a_pair(self):
        self.past_plays.append(self.node_pair)
        self._update_map()
        self._update_display()

    def _instructions(self):
        if input('The goal of the game is to force your opponent to be the one to form a triangle. \n'
                 'When prompted, enter the nodes you want to connect in capital letters. \n'
                 'If you\'re ready, enter "OK": ') == 'OK':
            return
        else:
            self._instructions()

    def play_a_game(self):
        self._reset_map()
        self._instructions()
        self._update_display()
        turn = 1
        while True:
            print(f"Player {turn},")
            self.node_pair = input("Enter a node pair to play, enter X to quit game, or S to show the available pairs: ")
            if self.node_pair == 'X':
                print(f"Game ended by player {turn}")
                return
            if self.node_pair == 'S':
                print("Formal map info:")
                self._show_map_state()
                continue
            self._check_node_pair()
            self._play_a_pair()
            if self._triangle_formed():
                print(f"Game Over! Player {2 if (turn == 1) else 1} wins" )
                return
            turn = 2 if (turn == 1) else 1

if __name__ == '__main__':
    game1 = HexGame()
    game1.play_a_game()

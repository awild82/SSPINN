import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


class Visualizer:

    def __init__(self, full, empirical):

        # Test input types
        if not isinstance(full, np.ndarray):
            raise TypeError('Input "full" is not a numpy matrix')
        if not isinstance(empirical, dict):
            raise TypeError('Input "empirical" is not a dictionary')

        self.full_mat = full
        self.empirical = empirical
        self.shift = {'H': 0, 'C': 183, 'N': 327, 'O': 346, 'F': 385,
                      'Cl': 397, 'Br': 407, 'I': 413, 'P': 419,
                      'B': 421, 'S': 424}
        # self.shift = {'H': 0, 'C': 5, 'N': 9, 'O': 11} #FOR TEST CASE BELOW
        self._genLabels()
        self._truncate()

    def _truncate(self):
        '''
        Takes NN output matrix and truncates it to a minimal size
        adjacency matrix, used for plotting the output molecular
        graph.
        '''

        # Get total atom count
        atomcount = 0
        for key in self.empirical:
            atomcount += self.empirical[key]

        # initialize numpy matrices
        # tempmat = np.zeros((13,atomcount),dtype=int) #FOR TEST CASE BELOW
        tempmat = np.zeros((432, atomcount))
        adjmat = np.zeros((atomcount, atomcount))

        # Get the non-zero columns from the NN output adjacency matrix
        total = 0
        row_list = []
        for key in self.empirical:
            shift = self.shift[key]
            atoms = self.empirical[key]
            tempmat[:, total:atoms+total] = self.full_mat[:, shift:shift+atoms]
            row_list.append([shift, shift+atoms])
            total += atoms

        # Use row_list to populate a truncated square adjacency matrix with
        # all of the non-zero values from the NN output
        rowshift = 0
        for i in range(len(row_list)):
            start = row_list[i][0]
            end = row_list[i][1]
            length = end - start
            adjmat[rowshift:length+rowshift, :] = tempmat[start:end, :]
            rowshift += length

        # Round to integers
        rmat = np.around(adjmat, 0)
        rmat = rmat.astype(int)

        self.adjmat = rmat

    def _genLabels(self):
        '''
        Uses the empirical formula input to generate list of atomic
        labels for use by draw2Dstructure().
        '''
        labels = []
        for key in self.empirical:
            for i in range(self.empirical[key]):
                labels.append(key)

        self.labels = labels

    def draw2Dstructure(self):
        '''
        Uses the networkx package to draw a chemical graph using the
        truncated adjacency matrix from the neural net output.
        '''

        # Get labels into dictionary listing each node
        label_dict = {}
        for i in range(len(self.labels)):
            label_dict[i] = self.labels[i]

        # Atom color keys
        atomcolor = {'C': 'grey', 'O': 'r', 'N': 'b', 'H': 'w',
                     'S': 'orange', 'F': 'y', 'Cl': 'g', 'Br': 'purple',
                     'P': 'c', 'I': 'brown', 'B': 'pink'}

        # Generate graph
        G = nx.from_numpy_matrix(self.adjmat)
        pos = graphviz_layout(G)

        # Get list of node colors
        color_list = []
        for i in range(len(self.labels)):
            color_list.append(atomcolor[self.labels[i]])

        # Draw Nodes with color list
        nx.draw_networkx_nodes(G, pos, node_size=450, node_color=color_list)

        # Label bond order as weights from self.adjmat
        triple = [(a, b) for (a, b, d) in G.edges(data=True)
                  if d['weight'] > 2.0 and d['weight'] <= 3.0]
        double = [(a, b) for (a, b, d) in G.edges(data=True)
                  if d['weight'] > 1.0 and d['weight'] <= 2.0]
        single = [(a, b) for (a, b, d) in G.edges(data=True)
                  if d['weight'] <= 1.0]

        # Draw Atom labels
        nx.draw_networkx_labels(G, pos, label_dict, font_size=12)

        # Draw triple bonds
        nx.draw_networkx_edges(G, pos, edgelist=triple, width=14)
        nx.draw_networkx_edges(G, pos, edgelist=triple, width=8,
                               edge_color='w')
        nx.draw_networkx_edges(G, pos, edgelist=triple, width=3)

        # Draw double bonds
        nx.draw_networkx_edges(G, pos, edgelist=double, width=10)
        nx.draw_networkx_edges(G, pos, edgelist=double, width=4,
                               edge_color='w')

        # Draw single bonds
        nx.draw_networkx_edges(G, pos, edgelist=single, width=3)

        # Show Graph to user
        plt.axis('off')
        plt.show()


# Test Case
'''
empirical = {'H': 3, 'C': 2, 'N': 1, 'O': 1}
orgo = np.zeros((13,13))
orgo[5,0] = 1
orgo[6,1] = 1
orgo[9,2] = 1
orgo[0,5] = 1
orgo[6,5] = 1
orgo[11,5] = 2
orgo[1,6] = 1
orgo[7,6] = 1
orgo[9,6] = 2
orgo[2,9] = 1
orgo[6,9] = 2
orgo[5,11] = 2

vis = visualizer(orgo,empirical)
vis.draw2Dstructure()
'''

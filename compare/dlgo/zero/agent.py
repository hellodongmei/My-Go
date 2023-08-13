import numpy as np
from tensorflow.keras.optimizers import SGD
from dlgo import encoders
from dlgo.agent.base import Agent
import h5py
from dlgo import kerasutil

__all__ = [
    'ZeroAgent',
    'load_prediction_agent',
]


# tag::branch_struct[]
class Branch:
    def __init__(self, prior):
        self.prior = prior
        self.visit_count = 0
        self.total_value = 0.0
# end::branch_struct[]


# tag::node_class_defn[]
class ZeroTreeNode:
# end::node_class_defn[]
# tag::node_class_body[]
    def __init__(self, state, value, priors, parent, last_move):
        self.state = state
        self.value = value
        self.parent = parent                      # <1>
        self.last_move = last_move                # <1>
        self.total_visit_count = 1
        self.branches = {}
        for move, p in priors.items():
            if state.is_valid_move(move):
                self.branches[move] = Branch(p)
        self.children = {}                        # <2>

    def moves(self):                              # <3>
        return self.branches.keys()               # <3>

    def add_child(self, move, child_node):        # <4>
        self.children[move] = child_node          # <4>

    def has_child(self, move):                    # <5>
        return move in self.children              # <5>

    def get_child(self, move):                    # <6>
        return self.children[move]                # <6>
# end::node_class_body[]

# <1> in the root of the tree, the parent and last_move will be none
# <2> Later, children will map from a Move to another ZeroTreeNode.
# <3> Returns a list of all possible moves from this code
# <4> Allows adding new nodes into the tree
# <5> checks whether there's a child node for a particular move and returns a particular child move

# tag::node_record_visit[]
    def record_visit(self, move, value):
        self.total_visit_count += 1
        self.branches[move].visit_count += 1
        self.branches[move].total_value += value
# end::node_record_visit[]

# tag::node_class_helpers[]
    def expected_value(self, move):
        branch = self.branches[move]
        if branch.visit_count == 0:
            return 0.0
        return branch.total_value / branch.visit_count

    def prior(self, move):
        return self.branches[move].prior

    def visit_count(self, move):
        if move in self.branches:
            return self.branches[move].visit_count
        return 0
# end::node_class_helpers[]


# tag::zero_defn[]
class ZeroAgent(Agent):
# end::zero_defn[]
    # def __init__(self, model, encoder, rounds_per_move=1600, c=2.0):
    def __init__(self, model, encoder, rounds_per_move=100, c=2.0):
        self.model = model
        self.encoder = encoder

        self.collector = None

        self.num_rounds = rounds_per_move
        self.c = c

# tag::zero_select_move_defn[]
    def select_move(self, game_state):
# end::zero_select_move_defn[]
# tag::zero_walk_down[]
        root = self.create_node(game_state)           # <1>

        for i in range(self.num_rounds):              # <2>
            node = root
            next_move = self.select_branch(node)
            while node.has_child(next_move):          # <3>
                node = node.get_child(next_move)
                next_move = self.select_branch(node)
# end::zero_walk_down[]

# tag::zero_back_up[]
            new_state = node.state.apply_move(next_move)
            child_node = self.create_node(
                new_state, parent=node)

            move = next_move
            value = -1 * child_node.value             # <1>
            while node is not None:
                node.record_visit(move, value)
                move = node.last_move
                node = node.parent
                # should be 
                # root = child_node
                value = -1 * value
# end::zero_back_up[]

# <1> At each level in the tree, you switch perspective between the two players. Therefore, 
# <1> you must multiply the value by –1: what’s good for black is bad for white, and vice versa.

# tag::zero_record_collector[]
        if self.collector is not None:
            root_state_tensor = self.encoder.encode(game_state)
            visit_counts = np.array([
                root.visit_count(
                    self.encoder.decode_move_index(idx))
                for idx in range(self.encoder.num_moves())
            ])
            self.collector.record_decision(
                root_state_tensor, visit_counts)
# end::zero_record_collector[]

# tag::zero_select_max_visit_count[]
        return max(root.moves(), key=root.visit_count)
# end::zero_select_max_visit_count[]

    def set_collector(self, collector):
        self.collector = collector

    def set_paras(self, rounds_per_move, c):
        self.num_rounds = rounds_per_move
        self.c = c

# tag::zero_select_branch[]
    def select_branch(self, node):
        total_n = node.total_visit_count

        def score_branch(move):
            q = node.expected_value(move)
            p = node.prior(move)
            n = node.visit_count(move)
            return q + self.c * p * np.sqrt(total_n) / (n + 1)

        return max(node.moves(), key=score_branch)             # <1>
# end::zero_select_branch[]

# <1> node.moves() is a list of moves. When you pass in key=score_branch, then max will 
#     return the move with the highest value of the score_branch function.

# tag::zero_create_node[]
    def create_node(self, game_state, move=None, parent=None):
        state_tensor = self.encoder.encode(game_state)
        model_input = np.array([state_tensor])                 # <1>
        priors, values = self.model.predict(model_input)
        priors = priors[0]                                     # <2>
        # Add Dirichlet noise to the root node.
        if parent is None:
            noise = np.random.dirichlet(
                0.03 * np.ones_like(priors))
            priors = 0.75 * priors + 0.25 * noise
        value = values[0][0]                                   # <2>
        move_priors = {                                        # <3>
            self.encoder.decode_move_index(idx): p             # <3>
            for idx, p in enumerate(priors)                    # <3>
        }                                                      # <3>
        new_node = ZeroTreeNode(
            game_state, value,
            move_priors,
            parent, move)
        if parent is not None:
            parent.add_child(move, new_node)
        return new_node
# end::zero_create_node[]

# <1> The Keras predict function is a batch function that takes an array of examples. You must wrap 
# <1> your board_tensor in an array.
# <2> Likewise, predict returns arrays with multiple results, so you must pull out the first item.


# tag::zero_train[]
    def train(self, experience, learning_rate, batch_size):     # <1>
        num_examples = experience.states.shape[0]

        model_input = experience.states

        visit_sums = np.sum(                                    # <2>
            experience.visit_counts, axis=1).reshape(           # <2>
            (num_examples, 1))                                  # <2>
        action_target = experience.visit_counts / visit_sums    # <2>

        value_target = experience.rewards

        self.model.compile(
            SGD(lr=learning_rate),
            loss=['categorical_crossentropy', 'mse'])
        self.model.fit(
            model_input, [action_target, value_target],
            batch_size=batch_size)
# end::zero_train[]


    def serialize(self, h5file):
        #h5file.require_group('encoder')
        f = h5py.File(h5file,'w')
        f.create_group('encoder')
        f['encoder'].attrs['name'] = self.encoder.name()
        f['encoder'].attrs['board_size'] = self.encoder.board_size
        # f['encoder'].attrs['board_height'] = self.encoder.board_height
        f.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, f['model'])
        f.close()

# tag::dl_agent_deserialize[]
def load_prediction_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    if not isinstance(encoder_name, str):
        encoder_name = encoder_name.decode('ascii')
    board_size = h5file['encoder'].attrs['board_size']
    
    encoder = encoders.get_encoder_by_name(
        encoder_name, board_size)
    return ZeroAgent(model, encoder)
# tag::dl_agent_deserialize[]
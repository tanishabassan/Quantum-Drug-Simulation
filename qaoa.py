from pyquil.quil import Program
from pyquil.gates import H
from pyquil.paulis import sI, sX, sZ, exponentiate_commuting_pauli_sum
from pyquil.api import QVMConnection

# Create a 4-node array graph: 0-1-2-3.
graph = [(0, 1), (1, 2), (2, 3)]
# Nodes [0, 1, 2, 3].
nodes = range(4)

# Create the initial state program, a sum over all bitstrings, via Hadamards on all qubits.
init_state_prog = Program([H(i) for i in nodes])

# The cost Hamiltonian is sum of the application of 0.5 * (1 - \sigma_z^i * \sigma_z^j) for all
# qubit pairs (i, j).
h_cost = -0.5 * sum(sI(nodes[0]) - sZ(i) * sZ(j) for i, j in graph)

# The driver Hamiltonian is the sum of the application of \sigma_x^i for all qubits i.
h_driver = -1. * sum(sX(i) for i in nodes)

def qaoa_ansatz(gammas, betas):
    """
    Function that returns a QAOA ansatz program for a list of angles betas and gammas. len(betas) ==
    len(gammas) == P for a QAOA program of order P.
    :param list(float) gammas: Angles over which to parameterize the cost Hamiltonian.
    :param list(float) betas: Angles over which to parameterize the driver Hamiltonian.
    :return: The QAOA ansatz program.
    :rtype: Program.
    """
    return Program([exponentiate_commuting_pauli_sum(h_cost)(g) + exponentiate_commuting_pauli_sum(h_driver)(b) \
        for g, b in zip(gammas, betas)])

# Create a program, the state initialization plus a QAOA ansatz program, for P = 2.
program = init_state_prog + qaoa_ansatz([0., 0.5], [0.75, 1.])

# Initialize the QVM and run the program.


qvm = QVMConnection()
from mock import patch
with patch("pyquil.api.QVMConnection") as qvm:
    qvm.run_and_measure.return_value = [
        [1, 0, 1, 0],
        [1, 0, 1, 0]
    ]

results = qvm.run_and_measure(program, qubits=nodes, trials=2)

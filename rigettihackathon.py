from pyquil.quil import Program
import pyquil.api as api
from pyquil.gates import *
from grove.pyvqe.vqe import VQE
from scipy.optimize import minimize
import numpy as np

qvm = api.QVMConnection()



def small_ansatz(params):
    return Program(RX(params[0], 0))



print(small_ansatz([1.0]))

from pyquil.paulis import sZ
initial_angle = [4.0]

hamiltonian = sZ(0) #Sigma_z on zeroth qubit


vqe_inst = VQE(minimizer=minimize,
               minimizer_kwargs={'method': 'nelder-mead'})

angle_range = np.linspace(0.0, 2 * np.pi, 20)
data = [vqe_inst.expectation(small_ansatz([angle]), hamiltonian, 1000, qvm)
        for angle in angle_range]


result = vqe_inst.vqe_run(small_ansatz, hamiltonian, initial_angle, None, qvm=qvm)
print(result)

grove.alpha.phaseestimation.phase_estimation.controlled(m)


import matplotlib.pyplot as plt
plt.xlabel('Angle [radians]')
plt.ylabel('Expectation value')
plt.plot(angle_range, data)
plt.show()

### setup the pyquil environment
from pyquil.quil import Program
### imprort gates to run
from pyquil.gates import X, MEASURE

prog = Program(X(0))
print(prog)

prog+= MEASURE(0,[0])
print(prog)

from pyquil.api import QVMConnection
qvm = QVMConnection()
results = qvm.run(prog, classical_addresses = [0], trials = 10)
print (results)

from pyquil.gates import H, CNOT

prog = Program(H(0), CNOT (0,1), MEASURE (0,0), MEASURE (1,1))

print (prog)
results = qvm.run(prog, classical_addresses = [0, 1], trials = 10)

print(results)

from pyquil.api import QVMConnection

frm pyquil.api import get_devices

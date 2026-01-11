import pennylane as qml
import numpy as np
from functools import partial
import matplotlib.pyplot as plt

bitstrings = ["01", "11", "11", "00", "01", "11", "11", "00"]

control_wires = [0, 1, 2]
target_wires = [3, 4]

Ui = [qml.BasisState(int(bitstring, 2), target_wires) for bitstring in bitstrings]

dev = qml.device("default.qubit")


# This line is included for drawing purposes only.
@partial(qml.transforms.decompose, max_expansion=1)
@qml.set_shots(1)
@qml.qnode(dev)
def circuit(index):
    qml.BasisState(index, wires=control_wires)
    qml.Select(Ui, control=control_wires)
    return qml.sample(wires=target_wires)


qml.draw_mpl(circuit, style="pennylane")(3)
plt.show()
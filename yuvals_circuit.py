import cirq

# Define qubits
ctrl_reg = cirq.LineQubit.range(2)   # 0,1
trgt_reg = cirq.LineQubit.range(2, 5)  # 2,3,5

# Element 0
element_zero = cirq.Circuit(
    cirq.X(ctrl_reg[0]),
    cirq.X(ctrl_reg[1]),
    cirq.TOFFOLI(ctrl_reg[0], ctrl_reg[1], trgt_reg[2]),
    cirq.X(ctrl_reg[1]),
    cirq.X(ctrl_reg[0]),
)

# Element 1
element_one = cirq.Circuit(
    cirq.X(ctrl_reg[0]),
    cirq.TOFFOLI(ctrl_reg[0], ctrl_reg[1], trgt_reg[1]),
    cirq.X(ctrl_reg[0]),
)

# Element 2
element_two = cirq.Circuit(
    cirq.X(ctrl_reg[1]),
    cirq.TOFFOLI(ctrl_reg[0], ctrl_reg[1], trgt_reg[0]),
    cirq.X(ctrl_reg[1]),
)

# Combine circuits
yuval_circuit = element_zero + element_one + element_two


print(yuval_circuit)

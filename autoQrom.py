#!/usr/bin/env python3

# Give the program a list of bit strings and it will output a QROM circuit from it. 
import cirq
import math
import numpy as np


def tensor_product(matrices):
    result = matrices[0]
    for matrix in matrices[1:]:
        result = np.kron(result, matrix)
    return result


def _validate_square_power_of_two(matrix, index):
    if matrix.ndim != 2:
        raise ValueError(f"Matrix {index} must be 2-dimensional.")
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"Matrix {index} must be square.")
    dim = matrix.shape[0]
    if dim == 0 or (dim & (dim - 1)) != 0:
        raise ValueError(
            f"Matrix {index} dimension must be a power of two, got {dim}."
        )
    return dim


def generate_qrom_circuit(matrices):
    if not matrices:
        raise ValueError("At least one matrix must be provided.")

    num_of_elements = len(matrices)
    dim = _validate_square_power_of_two(matrices[0], 0)
    num_target_qubits = int(math.log2(dim))

    print(f"Number of elements: {num_of_elements}")

    # Makes sure all matrices are the same shape and valid
    for index, matrix in enumerate(matrices):
        matrix_dim = _validate_square_power_of_two(matrix, index)
        if matrix_dim != dim:
            raise ValueError("All matrices must be the same shape.")

    if num_of_elements == 1:
        num_ctrl_qubits = 0
    else:
        num_ctrl_qubits = math.ceil(math.log(num_of_elements, 2))

    print(f"Number of control qubits: {num_ctrl_qubits}")

    ctrl_reg = cirq.NamedQubit.range(num_ctrl_qubits, prefix="ctrl ")
    trgt_reg = cirq.NamedQubit.range(num_target_qubits, prefix="trgt ")
    
    circuit = cirq.Circuit()

    # Use multi-controlled gates to set the target qubits based on the control qubits
    for index, matrix in enumerate(matrices):
        part_circuit = cirq.Circuit()
        if num_ctrl_qubits > 0:
            i_in_binary = bin(index)[2:].zfill(num_ctrl_qubits)
        else:
            i_in_binary = ""

        #Creating anti-controls
        for i, bit in enumerate(i_in_binary):
            if bit == "0":
                part_circuit.append(cirq.X(ctrl_reg[i]))

        #Setting target bits
        print(f"Target matrix for index {index}:\n{matrix}")
        matrix_gate = cirq.MatrixGate(matrix)
        if num_ctrl_qubits > 0:
            part_circuit.append(matrix_gate.on(*trgt_reg).controlled_by(*ctrl_reg))
        else:
            part_circuit.append(matrix_gate.on(*trgt_reg))
                
        #Removing anti-controls
        for i, bit in enumerate(i_in_binary):
            if bit == "0":
                 part_circuit.append(cirq.X(ctrl_reg[i]))

        circuit += part_circuit


    return circuit



if __name__ == "__main__":
    print("Enter matrices (blank line to separate, double blank to finish):")

    matrices = []
    current_rows = []

    while True:
        line = input().strip()

        # Double blank line → finish
        if line == "":
            if current_rows:
                matrices.append(np.array(current_rows, dtype=complex))
                current_rows = []
            else:
                break
        else:
            current_rows.append([complex(x) for x in line.split()])
    print("Input Matrices:")
    for matrix in matrices:
        print(matrix)
    qrom_circuit = generate_qrom_circuit(matrices)
    print("Generated QROM Circuit:")
    print(qrom_circuit)

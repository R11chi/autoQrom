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



gates = {
    "X": cirq.X,
    "Y": cirq.Y,
    "Z": cirq.Z,
    "I": cirq.I,
}

def generate_qrom_circuit(bitstrings):
    num_of_elements = len(bitstrings)
    num_target_qubits = len(bitstrings[0]) 

    print(f"Number of elements: {num_of_elements}")

    # Makes sure all bitstrings are of the same length
    for bs in bitstrings:
        if len(bs) != num_target_qubits:
            raise ValueError("All bitstrings must be of the same length.")

    if num_of_elements == 1:
        num_ctrl_qubits = 1
    else:    
        num_ctrl_qubits =  math.ceil(math.log(num_of_elements, 2))

    print(f"Number of control qubits: {num_ctrl_qubits}")

    ctrl_reg = cirq.NamedQubit.range(num_ctrl_qubits, prefix="ctrl ")
    trgt_reg = cirq.NamedQubit.range(num_target_qubits, prefix="trgt ")
    
    circuit = cirq.Circuit()

    # Use multi-controlled X gates to set the target qubits based on the control qubits
    for index, bitstring in enumerate(bitstrings):
        part_circuit = cirq.Circuit()
        i_in_binary = bin(index)[2:].zfill(num_ctrl_qubits) 

        #Creating anti-controls
        for i, bit in enumerate(i_in_binary):
            if bit == "0":
                part_circuit.append(cirq.X(ctrl_reg[i]))

        #Setting target bits
        for target_i, target_bit in enumerate(bitstring):
                if target_bit in gates:
                    part_circuit.append(gates[target_bit](trgt_reg[target_i]).controlled_by(*ctrl_reg))
                else:
                    raise ValueError(f"Invalid Pauli operator: {target_bit}")
                
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
    qrom_circuit = generate_qrom_circuit(matrices)
    print("Generated QROM Circuit:")
    print(qrom_circuit)
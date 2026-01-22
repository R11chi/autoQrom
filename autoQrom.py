#!/usr/bin/env python3

# Give the program a list of bit strings and it will output a QROM circuit from it. 
import cirq
import math
import numpy as np


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
    user_input = input("Enter Pauli strings (X, Y, Z, I)^* separated by commas: ").strip()
    bitstrings = [bs.strip() for bs in user_input.split(",") if bs.strip()]
    qrom_circuit = generate_qrom_circuit(bitstrings)
    print("Generated QROM Circuit:")
    print(qrom_circuit)
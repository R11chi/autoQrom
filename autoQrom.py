#!/usr/bin/env python3

# Give the program a list of bit strings and it will output a QROM circuit from it. 
import cirq
import math


def generate_qrom_circuit(bitstrings):
    num_of_elements = len(bitstrings)
    num_target_qubits = len(bitstrings[0]) 

    # Makes sure all bitstrings are of the same length
    for bs in bitstrings:
        if len(bs) != num_target_qubits:
            raise ValueError("All bitstrings must be of the same length.")
        
    # The amount of control qubits is determined by the number of bitstrings in the list
    num_ctrl_qubits =  int(math.log(num_of_elements, 2))


    print(f"Number of control qubits: {num_ctrl_qubits}")
    print(f"Number of bitstrings (n): {num_of_elements}")
    print(f"Length of each bitstring (m): {num_target_qubits}")



    ctrl_reg = cirq.LineQubit.range(num_ctrl_qubits)  # Control qubits
    trgt_reg = cirq.LineQubit.range(num_ctrl_qubits, num_ctrl_qubits + num_target_qubits)  # Target qubits


    
    # Use a multi-controlled Toffoli gate to set the target qubits based on the control qubits
    for i in num_ctrl_qubits:
        cirq.X(ctrl_reg[i])
    
    
    mcx = cirq.X(trgt_reg[0]).controlled_by(*ctrl_reg)
    circuit = cirq.Circuit(mcx)
    return circuit



# Example usage
if __name__ == "__main__":
    bitstrings = [
        '001',
        '010',
        '100',
        '111',
        '000',
        '101',
        '011',
        '110'
    ]
    qrom_circuit = generate_qrom_circuit(bitstrings)
    print("Generated QROM Circuit:")
    print(qrom_circuit)

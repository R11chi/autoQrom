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
        
    num_ctrl_qubits =  math.ceil(math.log(num_of_elements, 2))

    print(f"Number of control qubits: {num_ctrl_qubits}")

    ctrl_reg = cirq.LineQubit.range(num_ctrl_qubits)  # Control qubits
    trgt_reg = cirq.LineQubit.range(num_ctrl_qubits, num_ctrl_qubits + num_target_qubits)  # Target qubits


    
    circuit = cirq.Circuit()

    # Use multi-controlled X gates to set the target qubits based on the control qubits
    for index, bitstring in enumerate(bitstrings):
        part_circuit = cirq.Circuit()
        print(f"Processing bitstring index {index}: {bitstring}")
        i_in_binary = bin(index)[2:].zfill(num_ctrl_qubits) 
        print(f"Control bits: {i_in_binary}")

        #Creating anti-controls
        for i, bit in enumerate(i_in_binary):
            if bit == "0":
                part_circuit.append(cirq.X(ctrl_reg[i]))
        
        print(f"Applying X gates to control qubits: {[ctrl_reg[i] for i, bit in enumerate(i_in_binary) if bit == '0']}")

        for target_i, target_bit in enumerate(bitstring):
            if target_bit == "1":
                part_circuit.append(cirq.X(trgt_reg[target_i]).controlled_by(*ctrl_reg))
        
        #Removing anti-controls
        for i, bit in enumerate(i_in_binary):
            if bit == "0":
                 part_circuit.append(cirq.X(ctrl_reg[i]))
                 
        circuit += part_circuit


    return circuit


if __name__ == "__main__":
    user_input = input("Enter bitstrings separated by commas: ").strip()
    bitstrings = [bs.strip() for bs in user_input.split(",") if bs.strip()]
    qrom_circuit = generate_qrom_circuit(bitstrings)
    print("Generated QROM Circuit:")
    print(qrom_circuit)

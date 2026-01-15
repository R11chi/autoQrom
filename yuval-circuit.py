#!/usr/bin/env python

import cirq
import cirq_google

ctrl_reg = cirq.LineQubit(2)
trgt_reg = cirq.LineQubit(3)

element_zero = cirq.Circuit()
element_zero.append(cirq.X(ctrl_reg[0])
element_zero.append(cirq.X(ctrl_reg[1])
element_zero.append(cirq.TOFFOLI(ctrl_reg[0], ctrl_reg[1], trgt_reg[-1])
element_zero.append(cirq.X(ctrl_reg[1])
element_zero.append(cirq.X(ctrl_reg[0])

element_one = cirq.circuit()
element_one.append(cirq.X(ctrl_reg[0])
element_one.append(cirq.TOFFOLI(ctrl_reg[0], ctrl_reg[1], trgt_reg[-2])
element_one.append(cirq.X(ctrl_reg[0])

element_two = cirq.Circuit()
element_two.append(cirq.X(ctrl_reg[1])
element_two.append(cirq.TOFFOLI(ctrl_reg[0], ctrl_reg[1], trgt_reg[-3])
element_two.append(cirq.X(ctrl_reg[1])

yuval_circuit = element_zero + element_one + element_two


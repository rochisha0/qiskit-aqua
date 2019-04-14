# -*- coding: utf-8 -*-

# Copyright 2019 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
Relative Phase Toffoli Gates.
"""

from qiskit import QuantumCircuit
from qiskit.qasm import pi

from qiskit.aqua import AquaError
from qiskit.aqua.utils.circuit_utils import is_qubit


def _apply_rccx(circ, a, b, c):
    circ.u2(0, pi, c)  # h
    circ.u1(pi / 4, c)  # t
    circ.cx(b, c)
    circ.u1(-pi / 4, c)  # tdg
    circ.cx(a, c)
    circ.u1(pi / 4, c)  # t
    circ.cx(b, c)
    circ.u1(-pi / 4, c)  # tdg
    circ.u2(0, pi, c)  # h


def _apply_rcccx(circ, a, b, c, d):
    circ.u2(0, pi, d)  # h
    circ.u1(pi / 4, d)  # t
    circ.cx(c, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.u2(0, pi, d)  # h
    circ.cx(a, d)
    circ.u1(pi / 4, d)  # t
    circ.cx(b, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.cx(a, d)
    circ.u1(pi / 4, d)  # t
    circ.cx(b, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.u2(0, pi, d)  # h
    circ.u1(pi / 4, d)  # t
    circ.cx(c, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.u2(0, pi, d)  # h


def rccx(self, q_control_1, q_control_2, q_target):
    """
    Apply Relative Phase Toffoli gate from q_control_1 and q_control_2 to q_target.

    https://arxiv.org/pdf/1508.03273.pdf Figure 3
    """
    if not is_qubit(q_control_1):
        raise AquaError('A qubit is expected for the first control.')
    if not self.has_register(q_control_1[0]):
        raise AquaError('The first control qubit is expected to be part of the circuit.')

    if not is_qubit(q_control_2):
        raise AquaError('A qubit is expected for the second control.')
    if not self.has_register(q_control_2[0]):
        raise AquaError('The second control qubit is expected to be part of the circuit.')

    if not is_qubit(q_target):
        raise AquaError('A qubit is expected for the target.')
    if not self.has_register(q_target[0]):
        raise AquaError('The target qubit is expected to be part of the circuit.')
    self._check_dups([q_control_1, q_control_2, q_target])
    _apply_rccx(self, q_control_1, q_control_2, q_target)


def rcccx(self, q_control_1, q_control_2, q_control_3, q_target):
    """
    Apply 3-Control Relative Phase Toffoli gate from ctl1, ctl2, and ctl3 to tgt.

    https://arxiv.org/pdf/1508.03273.pdf Figure 4
    """
    if not is_qubit(q_control_1):
        raise AquaError('A qubit is expected for the first control.')
    if not self.has_register(q_control_1[0]):
        raise AquaError('The first control qubit is expected to be part of the circuit.')

    if not is_qubit(q_control_2):
        raise AquaError('A qubit is expected for the second control.')
    if not self.has_register(q_control_2[0]):
        raise AquaError('The second control qubit is expected to be part of the circuit.')

    if not is_qubit(q_target):
        raise AquaError('A qubit is expected for the target.')
    if not self.has_register(q_target[0]):
        raise AquaError('The target qubit is expected to be part of the circuit.')

    self._check_dups([q_control_1, q_control_2, q_control_3, q_target])
    _apply_rcccx(self, q_control_1, q_control_2, q_control_3, q_target)


QuantumCircuit.rccx = rccx
QuantumCircuit.rcccx = rcccx

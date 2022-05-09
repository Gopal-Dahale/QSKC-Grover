/** Incomplete implementation of the SAES encryption algorithm.*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <quantum.h>

void squarer(quantum_reg *reg, int in[4]) {
  int qubits[5][2] = {
      {in[1], in[3]}, {in[1], in[2]}, {in[2], in[1]}, {in[1], in[2]}, {in[0], in[1]},
  };
  for (int i = 0; i < 5; i++) {
    quantum_cnot(qubits[i][0], qubits[i][1], reg);
  }
}

void multiplier(quantum_reg *reg, int in[12]) {
  int qubits[19][3] = {{in[0], in[6], in[11]}, {in[1], in[5], in[11]}, {in[2], in[4], in[11]},
                       {in[0], in[5], in[10]}, {in[1], in[4], in[10]}, {in[0], in[4], in[9]},
                       {in[9], in[8], -1},     {in[10], in[9], -1},    {in[11], in[10], -1},
                       {in[0], in[7], in[8]},  {in[1], in[6], in[8]},  {in[2], in[5], in[8]},
                       {in[3], in[4], in[8]},  {in[1], in[7], in[9]},  {in[2], in[6], in[9]},
                       {in[3], in[5], in[9]},  {in[2], in[7], in[10]}, {in[3], in[6], in[10]},
                       {in[3], in[7], in[11]}};

  for (int i = 0; i < 19; i++) {
    if (qubits[i][2] == -1) {
      quantum_cnot(qubits[i][0], qubits[i][1], reg);
    } else {
      quantum_toffoli(qubits[i][0], qubits[i][1], qubits[i][2], reg);
    }
  }
}

void affine(quantum_reg *reg, int in[4]) {
  int qubits[8][2] = {{in[2], in[3]}, {in[1], in[3]}, {in[1], in[2]}, {in[0], in[2]},
                      {in[1], in[0]}, {in[3], in[0]}, {in[2], in[1]}, {in[3], in[1]}};
  for (int i = 0; i < 8; i++) {
    quantum_cnot(qubits[i][0], qubits[i][1], reg);
  }

  quantum_sigma_x(in[0], reg);
  quantum_sigma_x(in[3], reg);
}

void sbox(quantum_reg *reg, int in[4], int out[4], int ancilla[8]) {
  squarer(reg, in);
  for (int i = 0; i < 4; i++) {
    quantum_cnot(in[i], in[i + 4], reg);
  }
  squarer(reg, in);
  // multiplier(reg, )
}

int main() {
  quantum_reg reg;

  srand(time(0));
  reg = quantum_new_qureg(0, 64 + 8);
  char msg[16] = "1101011100101000";
  char key[16] = "0100101011110101";

  // Initialize key
  for (int i = 0; i < 16; i++) {
    if (key[i] == '1') {
      quantum_sigma_x(i, &reg);
    }
  }

  // Initialize message
  for (int i = 0; i < 16; i++) {
    if (msg[i] == '1') {
      quantum_sigma_x(i, &reg);
    }
  }

  int in[4] = {0, 1, 2, 3};
  int out[4] = {40, 41, 42, 43};
  int ancilla[4] = {64, 65, 66, 67, 68, 69, 70, 71};
  sbox(&reg, in, out, ancilla);

  // quantum_hadamard(0, &reg);
  // quantum_cnot(0, 1, &reg);
  // result[0] = quantum_bmeasure_bitpreserve(0, &reg);
  // result[1] = quantum_bmeasure_bitpreserve(1, &reg);

  // printf("The Quantum RNG returned %i!\n", result[0]);
  // printf("The Quantum RNG returned %i!\n", result[1]);

  return 0;
}

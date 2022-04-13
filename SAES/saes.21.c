#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <quantum.h>
#include <assert.h>
#include <unistd.h>

quantum_matrix swap;
int mix_col[2][2];

void quantum_swap(int qubit_1, int qubit_2, quantum_reg *reg) {
  quantum_cnot(qubit_1, qubit_2, reg);
  quantum_cnot(qubit_2, qubit_1, reg);
  quantum_cnot(qubit_1, qubit_2, reg);
}

/*********************************** HELPER FUNCTIONS ***********************************/

int galois_mult(int b, int a) {
  int p = 0;
  for (int i = 0; i < 4; i++) {
    if (b & 1) {
      p = (p ^ a);
    }
    a = (a << 1);
    int hi_bit_set = (a & 0x10);
    if (hi_bit_set) {
      a = (a ^ (0x13));
    }
    b = (b >> 1);
  }
  return p;
}

void mix_column(int state[2][2]) {
  int res[2][2] = {{0, 0}, {0, 0}};
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 2; j++) {
      for (int k = 0; k < 2; k++) {
        res[i][j] = (res[i][j] ^ galois_mult(mix_col[i][k], state[k][j]));
      }
    }
  }
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 2; j++) {
      state[i][j] = res[i][j];
    }
  }
}
/****************************************************************************************/

/************************************* SAES *********************************************/

int measure_key(quantum_reg *reg) {
  int out[16] = {quantum_bmeasure_bitpreserve(0, reg),  quantum_bmeasure_bitpreserve(1, reg),
                 quantum_bmeasure_bitpreserve(2, reg),  quantum_bmeasure_bitpreserve(3, reg),
                 quantum_bmeasure_bitpreserve(4, reg),  quantum_bmeasure_bitpreserve(5, reg),
                 quantum_bmeasure_bitpreserve(6, reg),  quantum_bmeasure_bitpreserve(7, reg),
                 quantum_bmeasure_bitpreserve(8, reg),  quantum_bmeasure_bitpreserve(9, reg),
                 quantum_bmeasure_bitpreserve(10, reg), quantum_bmeasure_bitpreserve(11, reg),
                 quantum_bmeasure_bitpreserve(12, reg), quantum_bmeasure_bitpreserve(13, reg),
                 quantum_bmeasure_bitpreserve(14, reg), quantum_bmeasure_bitpreserve(15, reg)};

  // Display out array
  int res = 0;
  for (int i = 0; i < 16; i++) {
    res += (out[i] * (1 << (15 - i)));
    printf("%d", out[i]);
  }
  printf("\n");
  return res;
}

void add_round_key(quantum_reg *reg) {
  for (int i = 0; i < 16; i++) {
    quantum_cnot(i, 16 + i, reg);
  }
}

void sbox(quantum_reg *reg, int in[4]) {
  int qubits[12][4] = {
      {in[2], in[1], -1, -1},    {in[3], in[1], in[0], -1},    {in[0], in[2], in[3], -1},
      {in[0], in[3], in[1], -1}, {in[0], in[1], in[3], in[2]}, {in[3], in[0], -1, -1},
      {in[2], -1, -1, -1},       {in[3], -1, -1, -1},          {in[0], in[2], -1, -1},
      {in[1], in[2], in[0], -1}, {in[0], in[3], in[1], -1},    {in[0], in[1], in[3], -1}};
  for (int i = 0; i < 12; i++) {
    if (qubits[i][1] == -1) {
      quantum_sigma_x(qubits[i][0], reg);
    } else if (qubits[i][2] == -1) {
      quantum_cnot(qubits[i][0], qubits[i][1], reg);
    } else if (qubits[i][3] == -1) {
      quantum_toffoli(qubits[i][0], qubits[i][1], qubits[i][2], reg);
    } else {
      quantum_unbounded_toffoli(3, reg, qubits[i][0], qubits[i][1], qubits[i][2], qubits[i][3]);
    }
  }

  quantum_swap(in[0], in[2], reg);
  quantum_swap(in[0], in[3], reg);
  quantum_swap(in[1], in[2], reg);
}

void inv_sbox(quantum_reg *reg, int in[4]) {
  quantum_swap(in[1], in[2], reg);
  quantum_swap(in[0], in[3], reg);
  quantum_swap(in[0], in[2], reg);

  int qubits[12][4] = {
      {in[2], in[1], -1, -1},    {in[3], in[1], in[0], -1},    {in[0], in[2], in[3], -1},
      {in[0], in[3], in[1], -1}, {in[0], in[1], in[3], in[2]}, {in[3], in[0], -1, -1},
      {in[2], -1, -1, -1},       {in[3], -1, -1, -1},          {in[0], in[2], -1, -1},
      {in[1], in[2], in[0], -1}, {in[0], in[3], in[1], -1},    {in[0], in[1], in[3], -1}};

  for (int i = 11; i >= 0; i--) {
    if (qubits[i][1] == -1) {
      quantum_sigma_x(qubits[i][0], reg);
    } else if (qubits[i][2] == -1) {
      quantum_cnot(qubits[i][0], qubits[i][1], reg);
    } else if (qubits[i][3] == -1) {
      quantum_toffoli(qubits[i][0], qubits[i][1], qubits[i][2], reg);
    } else {
      quantum_unbounded_toffoli(3, reg, qubits[i][0], qubits[i][1], qubits[i][2], qubits[i][3]);
    }
  }
}

void round_key(quantum_reg *reg, int in[16], int round) {
  for (int i = 0; i < 4; i++) {
    quantum_swap(8 + in[i], 12 + in[i], reg);
  }

  sbox(reg, (int[]){in[8], in[9], in[10], in[11]});
  sbox(reg, (int[]){in[12], in[13], in[14], in[15]});

  for (int i = 0; i < 8; i++) {
    quantum_cnot(8 + in[i], in[i], reg);
  }

  // rcon 1 = 1000 0000
  // rcon 2 = 0011 0000
  assert((round == 1) || (round == 2));
  switch (round) {
    case 1:
      quantum_sigma_x(0, reg);
      break;
    case 2:
      quantum_sigma_x(2, reg);
      quantum_sigma_x(3, reg);
      break;
    default:
      break;
  }

  // Reverse
  inv_sbox(reg, (int[]){in[8], in[9], in[10], in[11]});
  inv_sbox(reg, (int[]){in[12], in[13], in[14], in[15]});

  for (int i = 0; i < 4; i++) {
    quantum_swap(8 + in[i], 12 + in[i], reg);
  }

  for (int i = 0; i < 8; i++) {
    quantum_cnot(in[i], 8 + in[i], reg);
  }
}

void mc(quantum_reg *reg, int in[8]) {
  int qubits[8][2] = {{in[0], in[6]}, {in[5], in[3]}, {in[4], in[2]}, {in[1], in[7]},
                      {in[7], in[4]}, {in[2], in[5]}, {in[3], in[0]}, {in[6], in[1]}};
  for (int i = 0; i < 8; i++) {
    quantum_cnot(qubits[i][0], qubits[i][1], reg);
  }

  int swap_qubits[9][2] = {{in[6], in[7]}, {in[6], in[4]}, {in[4], in[3]},
                           {in[3], in[2]}, {in[2], in[0]}, {in[0], in[7]},
                           {in[1], in[6]}, {in[2], in[5]}, {in[3], in[4]}};
  for (int i = 0; i < 9; i++) {
    quantum_swap(swap_qubits[i][0], swap_qubits[i][1], reg);
  }
}

void sr(quantum_reg *reg, int in[16]) {
  int qubits[4][2] = {{in[4], in[12]}, {in[5], in[13]}, {in[6], in[14]}, {in[7], in[15]}};
  for (int i = 0; i < 4; i++) {
    quantum_swap(qubits[i][0], qubits[i][1], reg);
  }
}

int measure_cipher(quantum_reg *reg) {
  int out[16] = {quantum_bmeasure_bitpreserve(16, reg), quantum_bmeasure_bitpreserve(17, reg),
                 quantum_bmeasure_bitpreserve(18, reg), quantum_bmeasure_bitpreserve(19, reg),
                 quantum_bmeasure_bitpreserve(20, reg), quantum_bmeasure_bitpreserve(21, reg),
                 quantum_bmeasure_bitpreserve(22, reg), quantum_bmeasure_bitpreserve(23, reg),
                 quantum_bmeasure_bitpreserve(24, reg), quantum_bmeasure_bitpreserve(25, reg),
                 quantum_bmeasure_bitpreserve(26, reg), quantum_bmeasure_bitpreserve(27, reg),
                 quantum_bmeasure_bitpreserve(28, reg), quantum_bmeasure_bitpreserve(29, reg),
                 quantum_bmeasure_bitpreserve(30, reg), quantum_bmeasure_bitpreserve(31, reg)};

  // Display out array
  int res = 0;
  for (int i = 0; i < 16; i++) {
    res += (out[i] * (1 << (15 - i)));
  }
  return res;
}

void init_key(char *key, quantum_reg *reg) {
  // Initialize key
  for (int i = 0; i < 16; i++) {
    if (key[i] == '1') {
      quantum_sigma_x(i, reg);
    }
  }
}

void init_msg(char *msg, quantum_reg *reg) {
  // Initialize message
  for (int i = 0; i < 16; i++) {
    if (msg[i] == '1') {
      quantum_sigma_x(i + 16, reg);
    }
  }
}

void sub_nibbles(quantum_reg *reg) {
  int sbox_bits[4];
  for (int i = 0; i < 4; i++) {
    sbox_bits[i] = 16 + i;
  }
  sbox(reg, sbox_bits);
  for (int i = 0; i < 4; i++) {
    sbox_bits[i] += 4;
  }
  sbox(reg, sbox_bits);
  for (int i = 0; i < 4; i++) {
    sbox_bits[i] += 4;
  }
  sbox(reg, sbox_bits);
  for (int i = 0; i < 4; i++) {
    sbox_bits[i] += 4;
  }
  sbox(reg, sbox_bits);
}

void mix_column_op(quantum_reg *reg) {
  int mc_bits[8];
  for (int i = 0; i < 8; i++) {
    mc_bits[i] = 16 + i;
  }
  mc(reg, mc_bits);
  for (int i = 0; i < 8; i++) {
    mc_bits[i] += 8;
  }
  mc(reg, mc_bits);
}

void encrypt(quantum_reg *reg) {
  int sr_bits[16];
  int round_key_bits[16];

  for (int i = 0; i < 16; i++) {
    sr_bits[i] = 16 + i;
    round_key_bits[i] = i;
  }

  add_round_key(reg);
  printf("ADDED ROUND KEY\n");
  sub_nibbles(reg);
  printf("SUB NIBBLES\n");
  sr(reg, sr_bits);
  printf("SR\n");
  mix_column_op(reg);
  printf("MIX COLUMN OP\n");

  round_key(reg, round_key_bits, 1);
  printf("ROUND KEY 1\n");
  add_round_key(reg);
  printf("ADD ROUND KEY 1\n");

  sub_nibbles(reg);
  printf("SUB NIBBLES\n");
  sr(reg, sr_bits);
  printf("SR\n");

  round_key(reg, round_key_bits, 2);
  printf("ROUND KEY 2\n");
  add_round_key(reg);
  printf("ADD ROUND KEY 2\n");
}

/****************************************************************************************/

/**************************************** TESTS *****************************************/

void swap_test() {
  int res[2];
  for (int i = 0; i < 4; i++) {
    quantum_reg reg = quantum_new_qureg(0, 2);
    if (i & 1) {
      quantum_sigma_x(0, &reg);
    }
    if ((i >> 1) & 1) {
      quantum_sigma_x(1, &reg);
    }
    quantum_swap(0, 1, &reg);

    res[0] = quantum_bmeasure_bitpreserve(0, &reg);
    res[1] = quantum_bmeasure_bitpreserve(1, &reg);

    assert(res[0] == ((i >> 1) & 1));
    assert(res[1] == (i & 1));
    quantum_delete_qureg(&reg);
  }
  printf("SWAP TEST SUCCEEDED\n");
}

void sbox_test() {
  int sbox_actual[16] = {9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7};

  int in[4] = {0, 1, 2, 3};
  for (int i = 0; i < 16; i++) {
    quantum_reg reg = quantum_new_qureg(0, 4);

    if ((i >> 3) & 1) {
      quantum_sigma_x(0, &reg);
    }
    if ((i >> 2) & 1) {
      quantum_sigma_x(1, &reg);
    }
    if ((i >> 1) & 1) {
      quantum_sigma_x(2, &reg);
    }
    if ((i >> 0) & 1) {
      quantum_sigma_x(3, &reg);
    }

    sbox(&reg, in);
    int out[4] = {quantum_bmeasure_bitpreserve(0, &reg), quantum_bmeasure_bitpreserve(1, &reg),
                  quantum_bmeasure_bitpreserve(2, &reg), quantum_bmeasure_bitpreserve(3, &reg)};

    // Convert out array from binary to decimal

    int res = 0;
    for (int j = 0; j < 4; j++) {
      res += (out[j] * (1 << (3 - j)));
    }

    assert(res == sbox_actual[i]);
    quantum_delete_qureg(&reg);
  }
  printf("SBOX TEST SUCCEEDED\n");
}

void inv_sbox_test() {
  int inv_sbox_actual[16] = {10, 5, 9, 11, 1, 7, 8, 15, 6, 0, 2, 3, 12, 4, 13, 14};

  int in[4] = {0, 1, 2, 3};
  for (int i = 0; i < 16; i++) {
    quantum_reg reg = quantum_new_qureg(0, 4);

    if ((i >> 3) & 1) {
      quantum_sigma_x(0, &reg);
    }
    if ((i >> 2) & 1) {
      quantum_sigma_x(1, &reg);
    }
    if ((i >> 1) & 1) {
      quantum_sigma_x(2, &reg);
    }
    if ((i >> 0) & 1) {
      quantum_sigma_x(3, &reg);
    }

    inv_sbox(&reg, in);
    int out[4] = {quantum_bmeasure_bitpreserve(0, &reg), quantum_bmeasure_bitpreserve(1, &reg),
                  quantum_bmeasure_bitpreserve(2, &reg), quantum_bmeasure_bitpreserve(3, &reg)};

    // Convert out array from binary to decimal

    int res = 0;
    for (int j = 0; j < 4; j++) {
      res += (out[j] * (1 << (3 - j)));
    }

    assert(res == inv_sbox_actual[i]);
    quantum_delete_qureg(&reg);
  }
  printf("INV SBOX TEST SUCCEEDED\n");
}

void mc_test() {
  int state[2][2] = {{0, 0}, {0, 0}};
  int in[8] = {0, 1, 2, 3, 4, 5, 6, 7};
  for (int i = 0; i < 16; i++) {
    for (int j = 0; j < 16; j++) {
      state[0][0] = i;
      state[1][0] = j;

      mix_column(state);
      int actual = ((state[0][0] << 12) | (state[1][0] << 8) | (state[0][1] << 4) | state[1][1]);
      quantum_reg reg = quantum_new_qureg(0, 8);
      int num = ((i << 12) | (j << 8) | (0 << 4) | (0));

      for (int k = 0; k < 8; k++) {
        if ((num >> (15 - k)) & 1) {
          quantum_sigma_x(k, &reg);
        }
      }

      mc(&reg, in);

      int out[8] = {quantum_bmeasure_bitpreserve(0, &reg), quantum_bmeasure_bitpreserve(1, &reg),
                    quantum_bmeasure_bitpreserve(2, &reg), quantum_bmeasure_bitpreserve(3, &reg),
                    quantum_bmeasure_bitpreserve(4, &reg), quantum_bmeasure_bitpreserve(5, &reg),
                    quantum_bmeasure_bitpreserve(6, &reg), quantum_bmeasure_bitpreserve(7, &reg)};

      int res = 0;
      for (int k = 0; k < 8; k++) {
        res += (out[k] * (1 << (15 - k)));
      }
      assert(actual == res);
      quantum_delete_qureg(&reg);
    }
  }
  printf("MC TEST SUCCEEDED\n");
}

void verification_test() {
  char msg[16] = "0110111101101011";
  char key[16] = "1010011100111011";
  char cipher[16] = "0000011100111000";

  int res = 0;
  for (int i = 0; i < 16; i++) {
    res += ((cipher[i] - 48) * (1 << (15 - i)));
  }

  quantum_reg reg = quantum_new_qureg(0, 32);
  init_key(key, &reg);
  init_msg(msg, &reg);
  encrypt(&reg);
  int out = measure_cipher(&reg);

  assert(res == out);
  quantum_delete_qureg(&reg);
  printf("BASIC TEST SUCCEEDED\n");
}

void prob_test() {
  char msg[16] = "0110111101101011";
  quantum_reg reg = quantum_new_qureg(0, 32);

  quantum_hadamard(0, &reg);
  quantum_hadamard(1, &reg);
  // quantum_hadamard(2, &reg);
  init_msg(msg, &reg);
  printf("INIT MSG TEST SUCCEEDED\n");
  encrypt(&reg);
  FILE *fp = fopen("prob_test.txt", "w");
  printf("%d\n", reg.size);
  // for (int i = 0; i < reg.size; i++) {
  //   fprintf("%lld %d\n", reg.state[i], quantum_prob(reg.amplitude[i]));
  // }
  fclose(fp);
  printf("PROB TEST SUCCEEDED\n");
}

/****************************************************************************************/

int main() {
  srand(time(0));

  swap = quantum_new_matrix(4, 4);
  int swap_set_indices[4] = {0, 6, 9, 15};
  int j = 0;
  for (int i = 0; i < 16; i++) {
    if (i == swap_set_indices[j]) {
      swap.t[i] = 1;
    } else {
      swap.t[i] = 0;
    }
  }

  mix_col[0][0] = 1;
  mix_col[0][1] = 4;
  mix_col[1][0] = 4;
  mix_col[1][1] = 1;

  // swap_test();
  // sbox_test();
  // mc_test();
  // inv_sbox_test();
  // verification_test();
  prob_test();

  return 0;
}
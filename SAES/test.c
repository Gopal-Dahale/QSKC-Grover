#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <quantum.h>
#include <complex.h>

int main() {
  quantum_reg reg;
  int result;
  srand(time(0));
  reg = quantum_new_qureg(0, 1);
  quantum_hadamard(0, &reg);
  printf("%d\n", reg.size);
  // result = quantum_bmeasure(0, &reg);
  for (int i = 0; i < reg.size; i++) {
    printf("%lld %f\n", reg.state[i], creal(reg.amplitude[i]));
  }
  // printf("The Quantum RNG returned %i!\n", result);

  return 0;
}
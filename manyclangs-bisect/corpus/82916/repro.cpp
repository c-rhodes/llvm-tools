#include <complex.h>
#include <math.h>

using namespace std;

void cmul2(complex<double> *__restrict a, complex<double> *__restrict b,
           complex<double> *__restrict c) {
  for (int i = 0; i < 1000; i++) {
    c[i] = a[i] * b[i];
  }
}

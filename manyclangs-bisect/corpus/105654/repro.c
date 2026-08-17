float foo(float *a) {
  float sum = 0.;
  for (int i = 0; i < 32000; i++) {
    if (a[i] > (float)0.)
      sum += a[i];
  }
  return sum;
}

#include <arm_neon.h>

uint16x8_t vec_fma(uint16x8_t a, uint16x8_t b, uint16_t c) {
  return vmlaq_n_u16(a, b, c);
}

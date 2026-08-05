#include <arm_neon.h>

float32x4_t zip(const float* a, const float* b) {
    float32x4_t va = vcombine_f32(vld1_f32(a), vdup_n_f32(0.0f));
    float32x4_t vb = vcombine_f32(vld1_f32(b), vdup_n_f32(0.0f));
    return vzip1q_f32(va, vb);
}

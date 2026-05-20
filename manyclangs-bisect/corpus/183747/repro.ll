define double @u256_to_f64(i256 %val) {
  %result = uitofp i256 %val to double
  ret double %result
}

define i256 @f64_to_u256(double %val) {
  %result = fptoui double %val to i256
  ret i256 %result
}

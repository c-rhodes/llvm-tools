define half @f16_return(float %arg) {
  %fptrunc = fptrunc float %arg to half
  ret half %fptrunc
}

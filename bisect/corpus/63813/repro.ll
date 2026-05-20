define void @test(ptr %0) {
  %V1 = load <8 x i8>, ptr %0
  %V2 = srem <8 x i8> %V1, <i8 -1, i8 -1, i8 -1, i8 -1, i8 -1, i8 -1, i8 -1, i8 -1>
  store <8 x i8> %V2, ptr %0
  ret void
}

define void @foo() {
  %1 = call i32 asm sideeffect "", "={x0},0"(i32 435)
  ret void
}

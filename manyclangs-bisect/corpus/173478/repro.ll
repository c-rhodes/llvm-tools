; Reproducer for https://github.com/llvm/llvm-project/issues/173478

target triple = "aarch64-unknown-linux-gnu"

%struct.si_qi_1 = type { [2 x i8], i16 }

define void @f_si_qi_0(<16 x i8> %x) {
entry:
  %x.addr = alloca <16 x i8>, align 16
  %y = alloca %struct.si_qi_1, align 2
  store <16 x i8> %x, ptr %x.addr, align 16
  %0 = call i32 asm sideeffect "", "={v1}"()
  store i32 %0, ptr %y, align 2
  %1 = load <16 x i8>, ptr %x.addr, align 16
  %vecext = extractelement <16 x i8> %1, i32 0
  %c = getelementptr inbounds %struct.si_qi_1, ptr %y, i32 0, i32 0
  %arrayidx = getelementptr inbounds [2 x i8], ptr %c, i64 0, i64 0
  store i8 %vecext, ptr %arrayidx, align 2
  %2 = load i32, ptr %y, align 2
  call void asm sideeffect "", "{v1}"(i32 %2)
  ret void
}

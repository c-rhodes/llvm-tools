; Reduced from llvm/llvm-project#77222.

define i16 @rev16(i16 %x) {
entry:
  %r = call i16 @llvm.bswap.i16(i16 %x)
  ret i16 %r
}

declare i16 @llvm.bswap.i16(i16)

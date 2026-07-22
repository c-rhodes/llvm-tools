declare void @llvm.init.trampoline(i8*, i8*, i8*);
declare i8* @llvm.adjust.trampoline(i8*);
declare void @__enable_execute_stack(i8* %tramp)

define i32 @foo(i32* nest %ptr, i32 %val) {
    %x = load i32, i32* %ptr
    %sum = add i32 %x, %val
    ret i32 %sum
}

define i32 @main(i32, i8**) {
    %closure = alloca i32
    store i32 13, i32* %closure
    %closure_ptr = bitcast i32* %closure to i8*

    %tramp_buf = alloca [72 x i8], align 16
    %tramp_ptr = getelementptr [72 x i8], [72 x i8]* %tramp_buf, i32 0, i32 0
    call void @__enable_execute_stack(i8* %tramp_ptr)
    call void @llvm.init.trampoline(
            i8* %tramp_ptr,
            i8* bitcast (i32 (i32*, i32)* @foo to i8*),
            i8* %closure_ptr)
    %ptr = call i8* @llvm.adjust.trampoline(i8* %tramp_ptr)
    %fp = bitcast i8* %ptr to i32(i32)*
    %res = call i32 %fp (i32 13)

    ret i32 1
}

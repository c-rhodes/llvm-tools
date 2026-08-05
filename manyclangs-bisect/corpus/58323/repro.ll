define <2 x i32> @vget_high32(ptr %A) nounwind {
	%a = load <4 x i32>, ptr %A
    %b = shufflevector <4 x i32> %a, <4 x i32> undef, <2 x i32> <i32 2, i32 3>
    %c = shufflevector <4 x i32> %a, <4 x i32> undef, <2 x i32> <i32 0, i32 1>
    %d = add <2 x i32> %b, %c
    ret <2 x i32> %d
}

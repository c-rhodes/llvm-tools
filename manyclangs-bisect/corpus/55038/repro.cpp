typedef bool bool4 __attribute__((ext_vector_type(4)));
typedef char char4 __attribute__((ext_vector_type(4)));

void foo(bool4 mask, char4 one, char4 two) {
  auto output = mask ? one : two;
}

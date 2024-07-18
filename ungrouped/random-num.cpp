#include <cstdio>
#include <memory>

int main(void) {
    std::unique_ptr<int> ptr = std::make_unique<int>(42);
    printf("Memory address of the int: %p\n", ptr.get());
    return 0;
}

#include <iostream>
#include <iomanip>

int main()
{
    int n = 10;
    char character = '*';
    std::cout << std::setw(n);
    std::cout << std::setfill(character);
    std::cout << "";
    return 0;
}

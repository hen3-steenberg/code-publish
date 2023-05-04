#include <iostream>

int main()
{
    while(true)
    {
        double a, b, result;
        char op;
        std::cin >> a >> op >> b;
        switch (op)
        {
        case '+':
            result = a + b;
            break;
        case '-':
            result = a - b;
            break;
        case '*':
            result = a * b;
            break;
        case '/':
            result = a / b;
            break;
        }
        std::cout << a << ' ' << op << ' ' << b << " = " << result << std::endl;
    }
    
}
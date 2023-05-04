#include <iostream>
double power(double base, int exponent)
{
    if(exponent)
    {
        int exp = (exponent > 0)? exponent : -exponent;
        double res = 1;
        for(int i = 0; i < exp;i++)
        {
            res *= base;
        }
        return (exponent > 0)? res : 1/res;
    }
    else return 1.0;
}


int main()
{
    for(int i = 0; i < 10;i++)
    {
        std::cout << "2^" << i << " = " << power(2,i) << std::endl;
    }
    return 0;
}
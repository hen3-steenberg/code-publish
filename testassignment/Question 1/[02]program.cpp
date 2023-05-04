#include <tuple>
#include <iostream>

std::tuple<int,int,int> somefunc()
{
	return {1, 2, 3};
}

int main()
{
	auto& [a, b, c] = somefunc();
	std::cout << a << b << c << std::endl;
	return 0;
}
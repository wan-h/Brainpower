#include <iostream>
#include <cmath>
#include "MathFunctions.h"
#include "Table.h"

double mysqrt(double x){
    if (x <= 0){
        return 0;
    }

    // use the table to help find an initial value
    double result = x;
    if (x >= 1 && x < 10) {
    std::cout << "Use the table to help find an initial value " << std::endl;
    result = sqrtTable[static_cast<int>(x)];
    }
    // if we have both log and exp then use them
#if defined(HAVE_LOG) && defined(HAVE_EXP)
    result = exp(log(x) * 0.5);
    std::cout << "Computing sqrt of " << x << " to be " << result
                << " using log and exp" << std::endl;
#else
    double result = x;

    for (int i = 0; i < 10; i++){
        if (result <= 0){
            result = 0.1;
        }
        double delta = x - (result * result);
        result = result + 0.5 * delta / result;
        std::cout << "Computing sqrt of " << x << " to be " << result << std::endl;
    }
#endif
    return result;
}
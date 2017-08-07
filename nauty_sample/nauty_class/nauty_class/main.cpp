//
//  main.cpp
//  nauty_class
//
//  Created by 熊田聖也 on 2017/02/27.
//  Copyright © 2017年 熊田聖也. All rights reserved.
//

#if(UNIT_TEST)
#define BOOST_TEST_MAIN
#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>

#else // UNIT_TEST

#include <iostream>

int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "Hello, World!\n";
    return 0;
}

#endif // UNIT_TEST

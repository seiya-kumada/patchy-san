//
//  main.cpp
//  centrality
//
//  Created by Seiya KUMADA on 2017/02/10.
//  Copyright (c) 2017年 kumada. All rights reserved.
//

#include <iostream>
#include <boost/graph/graphml.hpp>
#include <boost/filesystem.hpp>
#include <boost/graph/adjacency_list.hpp>

std::string TORUS_PATH = "/Users/seiya_kumada/Projects/topology-retrieval/centrality/lattice_periodic.graphml";
std::string LATTICE_PATH = "/Users/seiya_kumada/Projects/topology-retrieval/centrality/lattice.graphml";

namespace fs = boost::filesystem;

int main(int argc, const char * argv[])
{
    fs::exists(TORUS_PATH);
    fs::exists(LATTICE_PATH);
    
    using Graph = boost::adjacency_list<>;
    try
    {
        Graph g0;
        std::ifstream ifs0(LATTICE_PATH);
        boost::dynamic_properties dp;
        boost::read_graphml(ifs0, g0, dp);
    }
    catch(const std::exception& e)
    {
        std::cout << e.what() << std::endl;
    }
    return 0;
}

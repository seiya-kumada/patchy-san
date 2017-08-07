//
//  Nauty.hpp
//  nauty_class
//
//  Created by 熊田聖也 on 2017/02/27.
//  Copyright © 2017年 熊田聖也. All rights reserved.
//

#ifndef NautyGraph_hpp
#define NautyGraph_hpp

#include <nauty.h>
#include <vector>

class NautyGraph
{
public:
    using int_vector = std::vector<int>;
    
    NautyGraph(const NautyGraph&) = default;
    NautyGraph& operator=(const NautyGraph&) = delete;
    
    NautyGraph();
    ~NautyGraph();
    
    // get options
    const optionblk& get_options() const;
    
    // set/get the number of vertices
    void set_vertex_number(int n);
    int get_vertex_number() const;
    
    void set_partition(const std::vector<int>& lab, const std::vector<int>& ptn);
    
    // get m
    int get_m() const;
    
    void make_graph();
    
    void add_edge(int src, int dst);
    void execute_dense_nauty();
    
    const int_vector& get_label() const;
    const int_vector& get_easy_label() const;
    const int_vector& get_ptn() const;
    
private:
    
    int                 vertex_number_;
    int                 m_;
    std::vector<graph>  graph_;
    std::vector<graph>  canonical_graph_;
    int_vector          label_;
    int_vector          ptn_;
    int_vector          easy_label_;
    optionblk           options_;
};
#endif /* NautyGraph_hpp */

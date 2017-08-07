//
//  examples.cpp
//  static_allocation
//
//  Created by Seiya KUMADA on 2017/02/23.
//  Copyright (c) 2017年 熊田聖也. All rights reserved.
//

#include "sample.h"
#include <nauty.h>
#include <cpplinq.hpp>
#include <vector>
#include <boost/range/combine.hpp>


// 図1上段左側のグラフを作成する。
std::vector<graph> make_graph_1(int n, int m)
{
    // 0で初期化する。
    std::vector<graph> g(n * m, 0);
    
    // 以下は辺の登録である。無向グラフなので向きは任意である。
    
    ADDONEEDGE(g.data(), 7, 4, m);
    ADDONEEDGE(g.data(), 4, 0, m);
    ADDONEEDGE(g.data(), 0, 2, m);
    ADDONEEDGE(g.data(), 2, 7, m);
    
    ADDONEEDGE(g.data(), 0, 5, m);
    ADDONEEDGE(g.data(), 5, 1, m);
    ADDONEEDGE(g.data(), 1, 2, m);
    ADDONEEDGE(g.data(), 2, 5, m);
    ADDONEEDGE(g.data(), 0, 1, m);
    
    ADDONEEDGE(g.data(), 5, 3, m);
    ADDONEEDGE(g.data(), 3, 6, m);
    ADDONEEDGE(g.data(), 6, 1, m);

    return g;
}


// 図1上段右側のグラフを作成する。
std::vector<graph> make_graph_2(int n, int m)
{
    std::vector<graph> g(n * m, 0);
    
    ADDONEEDGE(g.data(), 5, 4, m);
    ADDONEEDGE(g.data(), 4, 2, m);
    ADDONEEDGE(g.data(), 2, 3, m);
    ADDONEEDGE(g.data(), 3, 5, m);
    
    ADDONEEDGE(g.data(), 2, 6, m);
    ADDONEEDGE(g.data(), 6, 1, m);
    ADDONEEDGE(g.data(), 1, 3, m);
    ADDONEEDGE(g.data(), 3, 6, m);
    ADDONEEDGE(g.data(), 1, 2, m);
    
    ADDONEEDGE(g.data(), 6, 7, m);
    ADDONEEDGE(g.data(), 7, 0, m);
    ADDONEEDGE(g.data(), 0, 1, m);

    return g;
}


// 隣接関係が等しいか見る。
bool is_identical(const std::vector<graph>& cg1, const std::vector<graph>& cg2)
{
    auto is_identical = true;
    for (const auto& p : boost::combine(cg1, cg2))
    {
        if (boost::get<0>(p) != boost::get<1>(p))
        {
            is_identical = false;
            break;
        }
    }
    return is_identical;
}


void sample_1()
{
    DEFAULTOPTIONS_GRAPH(options);
    
    // canonical labellingを行うことをNautyに教える。
    options.getcanon = true;
    
    // 頂点の数
    const auto n = 8;
    
    // n個の頂点を保持するのに必要なバイト数はn*mである。Nautyが採用しているグラフの構造はユーザガイドを参照のこと。
    const auto m = SETWORDSNEEDED(n);
    
    // The following optional call verifies that we are linking to compatible versions of the nauty routines.
    // これはなくても動くが、おまじないとして書いておく。
    nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
    
    // Nautyがメモリを動的に確保する手順は、クラシカルなC言語の手法である。ここではstd::vectorを用いて、これを置き換えた。
    
    std::vector<graph> cg1(n * m, 0); // 図1下段左側のcanonical graph
    std::vector<int> relabelling1(n); // canonize後のラベル
    {
        // 図1上段左側のグラフを作成する（入力）。
        auto g = make_graph_1(n, m);
        
        // 各種出力バッファ
        std::vector<int> lab(n);
        std::vector<int> ptn(n);
        std::vector<int> orbits(n);
        statsblk stats;
        
        // Nautyのインタフェースを呼び出す。
        densenauty(g.data(), lab.data(), ptn.data(), orbits.data(), &options, &stats, m, n, cg1.data());
        
        // 答え合わせ。
        const std::vector<int> answer {3, 6, 4, 7, 5, 1, 0, 2};
        cpplinq::from(lab) >>
            cpplinq::zip_with(cpplinq::from(answer)) >>
            cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
        
        // canonize後のラベリングを作る。
        cpplinq::range(0, n) >>
            cpplinq::for_each([&relabelling1, &lab](auto i){ relabelling1[lab[i]] = i; });
    }
    
    std::vector<graph> cg2(n * m, 0); // 図1下段右側のcanonical graph
    std::vector<int> relabelling2(n); // canonize後のラベル
    {
        // 図1上段右側のグラフを作成する（入力）。
        std::vector<graph> g = make_graph_2(n, m);
        
        // 各種出力バッファ
        std::vector<int> lab(n);
        std::vector<int> ptn(n);
        std::vector<int> orbits(n);
        statsblk stats;
        
        // Nautyのインタフェースを呼び出す。
        densenauty(g.data(), lab.data(), ptn.data(), orbits.data(), &options, &stats, m, n, cg2.data());
        
        // 答え合わせ。
        const std::vector<int> answer {0, 7, 4, 5, 1, 6, 2, 3};
        cpplinq::from(lab) >>
            cpplinq::zip_with(cpplinq::from(answer)) >>
            cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
        
        // canonize後のラベリングを作る。
        cpplinq::range(0, n) >>
            cpplinq::for_each([&relabelling2, &lab](auto i){ relabelling2[lab[i]] = i; });
    }
    
    // 2つのグラフの隣接関係が全て等しいか見る。
    assert(is_identical(cg1, cg2));

    // 答え合わせ。
    
    const std::vector<int> answers1 {6, 5, 7, 0, 2, 4, 1, 3};
    const std::vector<int> answers2 {0, 4, 6, 7, 2, 3, 5, 1};
    
    cpplinq::from(relabelling1) >>
        cpplinq::zip_with(cpplinq::from(answers1)) >>
        cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
    
    cpplinq::from(relabelling2) >>
        cpplinq::zip_with(cpplinq::from(answers2)) >>
        cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
}


void sample_2()
{
    DEFAULTOPTIONS_GRAPH(options);
    
    // canonical labellingを行うことをNautyに教える。
    options.getcanon = true;
    
    // partitioning(colouring)を行うことをNautyに教える。
    options.defaultptn = false;
    
    // 頂点の数
    const auto n = 8;
    
    // n個の頂点を保持するのに必要なバイト数はn*mである。Nautyが採用しているグラフの構造はユーザガイドを参照のこと。
    const auto m = SETWORDSNEEDED(n);
    
    // The following optional call verifies that we are linking to compatible versions of the nauty routines.
    // これはなくても動くが、おまじないとして書いておく。
    nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
    
    // Nautyがメモリを動的に確保する手順は、クラシカルなC言語の手法である。ここではstd::vectorを用いて、これを置き換えた。
    
    std::vector<graph> cg1(n * m, 0); // 図4下段左側のcanonical graph
    std::vector<int> relabelling1(n); // canonize後のラベル
    {
        // 図4上段左側のグラフを作成する（入力）。図1上段左側のグラフと同じ。
        auto g = make_graph_1(n, m);
        
        // partitioning(coloring)を行う（入力）。
        std::vector<int> lab {0, 2, 1, 3, 4, 5, 6, 7};
        std::vector<int> ptn {1, 0, 1, 1, 1, 1, 1, 0};
        
        // 出力バッファ
        std::vector<int> orbits(n);
        statsblk stats;
        
        // Nautyのインタフェースを呼び出す。
        densenauty(g.data(), lab.data(), ptn.data(), orbits.data(), &options, &stats, m, n, cg1.data());
        
        // 答え合わせ。
        const std::vector<int> answer {0, 2, 3, 6, 4, 7, 5, 1};
        cpplinq::from(lab) >>
            cpplinq::zip_with(cpplinq::from(answer)) >>
            cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
        
        // canonize後のラベリングを作る。
        cpplinq::range(0, n) >> cpplinq::for_each([&relabelling1, &lab](auto i){ relabelling1[lab[i]] = i; });
    }
    
    std::vector<graph> cg2(n * m, 0); // 図4下段右側のcanonical graph
    std::vector<int> relabelling2(n); // canonize後のラベル
    {
        // 図4上段右側のグラフを作成する（入力）。図1上段右側のグラフと同じ。
        auto g = make_graph_2(n, m);
        
        // partioning(coloring)を行う（入力）。
        std::vector<int> lab {3, 6, 2, 1, 4, 5, 0, 7};
        std::vector<int> ptn {1, 0, 1, 1, 1, 1, 1, 0};
        
        // 出力バッファ
        std::vector<int> orbits(n);
        statsblk stats;
        
        // Nautyのインタフェースを呼び出す。
        densenauty(g.data(), lab.data(), ptn.data(), orbits.data(), &options, &stats, m, n, cg2.data());
        
        // 答え合わせ。
        const std::vector<int> answer {3, 6, 0, 4, 7, 5, 1, 2};
        cpplinq::from(lab) >>
        cpplinq::zip_with(cpplinq::from(answer)) >>
        cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });

        // canonize後のラベリングを作る。
        cpplinq::range(0, n) >>
        cpplinq::for_each([&relabelling2, &lab](auto i){ relabelling2[lab[i]] = i; });
    }
    
    // 2つのグラフの隣接関係が全て等しいか見る。
    assert(!is_identical(cg1, cg2));
    
    // 答え合わせ。

    const std::vector<int> answers1 {0, 7, 1, 2, 4, 6, 3, 5};
    const std::vector<int> answers2 {2, 6, 7, 0, 3, 5, 1, 4};

    cpplinq::from(relabelling1) >>
    cpplinq::zip_with(cpplinq::from(answers1)) >>
    cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
    
    cpplinq::from(relabelling2) >>
    cpplinq::zip_with(cpplinq::from(answers2)) >>
    cpplinq::for_each([](const auto& pair){ assert(pair.first == pair.second); });
}

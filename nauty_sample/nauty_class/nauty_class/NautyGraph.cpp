//
//  NautyGraph.cpp
//  NautyGraph_class
//
//  Created by 熊田聖也 on 2017/02/27.
//  Copyright © 2017年 熊田聖也. All rights reserved.
//

#include "NautyGraph.hpp"
#include <cpplinq.hpp>

NautyGraph::NautyGraph()
    : vertex_number_{0}
    , m_{0}
    , graph_{}
    , canonical_graph_{}
    , label_{}
    , ptn_{}
    , easy_label_{}
{
    DEFAULTOPTIONS_GRAPH(options);
    options_ = options;
    options_.getcanon = true;
}

void NautyGraph::set_partition(const std::vector<int>& label, const std::vector<int>& ptn)
{
    label_ = label;
    ptn_ = ptn;
    options_.defaultptn = false;
}

NautyGraph::~NautyGraph()
{
    
}

const optionblk& NautyGraph::get_options() const
{
    return options_;
}

void NautyGraph::set_vertex_number(int n)
{
    vertex_number_ = n;
}

int NautyGraph::get_vertex_number() const
{
    return vertex_number_;
}

int NautyGraph::get_m() const
{
    return m_;
}

void NautyGraph::make_graph()
{
    m_ = SETWORDSNEEDED(vertex_number_);
    nauty_check(WORDSIZE, m_, vertex_number_, NAUTYVERSIONID);
    graph_ = std::vector<graph>(vertex_number_ * m_, 0);
}

void NautyGraph::add_edge(int src, int dst)
{
    ADDONEEDGE(graph_.data(), src, dst, m_);
}

void NautyGraph::execute_dense_nauty()
{
    if (options_.defaultptn)
    {
        label_ = std::vector<int>(vertex_number_);
        ptn_ = std::vector<int> (vertex_number_);
    }
    else
    {
        // do nothing
    }
    std::vector<int> orbits(vertex_number_);
    statsblk stats;
    canonical_graph_ = std::vector<graph>(m_ * vertex_number_, 0);
    
    densenauty(
       graph_.data(),
       label_.data(),
       ptn_.data(),
       orbits.data(),
       &options_,
       &stats,
       m_,
       vertex_number_,
       canonical_graph_.data());
    
    easy_label_ = std::vector<int>(vertex_number_);
    cpplinq::range(0, vertex_number_) >>
        cpplinq::for_each([this](auto i){ easy_label_[label_[i]] = i; });
}

const NautyGraph::int_vector& NautyGraph::get_label() const
{
    return label_;
}

const NautyGraph::int_vector& NautyGraph::get_easy_label() const
{
    return easy_label_;
}

const NautyGraph::int_vector& NautyGraph::get_ptn() const
{
    return ptn_;
}

#if(BOOST_PYTHON)
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

namespace
{
    // C++ -> Python
    template<typename T>
    class vector_to_pylist_converter
    {
    public:
        using native_type = T;
        
        // convert a C++ object to a Python one
        static PyObject* convert(const native_type& v)
        {
            namespace py = boost::python;
            py::list retval;
            
            for (const auto& i: v)
            {
                retval.append(py::object(i));
            }
            return py::incref(retval.ptr());
        }
    };
    
    // Python -> C++
    template<typename T>
    class pylist_to_vector_converter
    {
    public:
        using native_type = T;
        
        // judge whether a Python object can be converted to C++ one or not
        static void* convertible(PyObject* pyo)
        {
            if (!PySequence_Check(pyo))
            {
                return nullptr;
            }
            return pyo;
        }
        
        // convert a Python object to a C++ one
        static void construct(PyObject* pyo, boost::python::converter::rvalue_from_python_stage1_data* data)
        {
            namespace py = boost::python;
            native_type* storage = new(reinterpret_cast<py::converter::rvalue_from_python_storage<native_type>*>(data)->storage.bytes) native_type();
            for (py::ssize_t i = 0, l = PySequence_Size(pyo); i < l; ++i) {
                storage->push_back(
                    py::extract<typename boost::range_value<native_type>::type>(
                        PySequence_GetItem(pyo, i)));
            }
            data->convertible = storage;
        }
    };
}

BOOST_PYTHON_MODULE(libnauty_graph)
{
    using namespace boost::python;
    
    class_<NautyGraph>("NautyGraph")
        .def("set_vertex_number", &NautyGraph::set_vertex_number)
        .def("get_vertex_number", &NautyGraph::get_vertex_number)
        .def("make_graph", &NautyGraph::make_graph)
        .def("add_edge", &NautyGraph::add_edge)
        .def("execute_dense_nauty", &NautyGraph::execute_dense_nauty)
        .def("get_label", &NautyGraph::get_label, return_value_policy<copy_const_reference>())
        .def("get_ptn", &NautyGraph::get_ptn, return_value_policy<copy_const_reference>())
        .def("set_partition", &NautyGraph::set_partition)
    ;
    
    // C++ -> Python
    to_python_converter<NautyGraph::int_vector, vector_to_pylist_converter<NautyGraph::int_vector>>();
    
    // Python -> C++
    converter::registry::push_back(
        &pylist_to_vector_converter<NautyGraph::int_vector>::convertible,
        &pylist_to_vector_converter<NautyGraph::int_vector>::construct,
        boost::python::type_id<NautyGraph::int_vector>());

}

#endif // BOOST_PYTHON

#if(UNIT_TEST)
#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>
#include <iostream>

namespace
{
    void test_constructor()
    {
        NautyGraph nauty_graph {};
        BOOST_CHECK(true);
    }
    
    void test_set_vertex_number()
    {
        NautyGraph nauty_graph {};
        BOOST_CHECK(nauty_graph.get_options().getcanon);
        nauty_graph.set_vertex_number(8);
        BOOST_CHECK(nauty_graph.get_vertex_number() == 8);
    }
    
    void test_make_graph()
    {
        NautyGraph nauty_graph {};
        BOOST_CHECK(nauty_graph.get_options().getcanon);
        nauty_graph.set_vertex_number(8);
        BOOST_CHECK(nauty_graph.get_vertex_number() == 8);
        nauty_graph.make_graph();
        BOOST_CHECK(nauty_graph.get_m() == 1);
    }
    
    void test_add_edge()
    {
        NautyGraph nauty_graph {};
        BOOST_CHECK(nauty_graph.get_options().getcanon);
        nauty_graph.set_vertex_number(8);
        BOOST_CHECK(nauty_graph.get_vertex_number() == 8);
        nauty_graph.make_graph();
        BOOST_CHECK(nauty_graph.get_m() == 1);
        
        nauty_graph.add_edge(7, 4);
        nauty_graph.add_edge(4, 0);
        nauty_graph.add_edge(0, 2);
        nauty_graph.add_edge(2, 7);
        
        nauty_graph.add_edge(0, 5);
        nauty_graph.add_edge(5, 1);
        nauty_graph.add_edge(1, 2);
        nauty_graph.add_edge(2, 5);
        nauty_graph.add_edge(0, 1);
        
        nauty_graph.add_edge(5, 3);
        nauty_graph.add_edge(3, 6);
        nauty_graph.add_edge(6, 1);

        // what should i do?
    }
    
    void test_execute_dense_nauty_1()
    {
        NautyGraph nauty_graph {};
        BOOST_CHECK(nauty_graph.get_options().getcanon);
        nauty_graph.set_vertex_number(8);
        BOOST_CHECK(nauty_graph.get_vertex_number() == 8);
        nauty_graph.make_graph();
        BOOST_CHECK(nauty_graph.get_m() == 1);
        
        nauty_graph.add_edge(7, 4);
        nauty_graph.add_edge(4, 0);
        nauty_graph.add_edge(0, 2);
        nauty_graph.add_edge(2, 7);
        
        nauty_graph.add_edge(0, 5);
        nauty_graph.add_edge(5, 1);
        nauty_graph.add_edge(1, 2);
        nauty_graph.add_edge(2, 5);
        nauty_graph.add_edge(0, 1);
        
        nauty_graph.add_edge(5, 3);
        nauty_graph.add_edge(3, 6);
        nauty_graph.add_edge(6, 1);
        
        nauty_graph.execute_dense_nauty();
        const auto& label = nauty_graph.get_label();
     
        const std::vector<int> answer1 {3, 6, 4, 7, 5, 1, 0, 2};
        cpplinq::from(label) >>
        cpplinq::zip_with(cpplinq::from(answer1)) >>
        cpplinq::for_each([](const auto& pair){ BOOST_CHECK(pair.first == pair.second); });
        
        const auto& easy_label = nauty_graph.get_easy_label();
        const std::vector<int> answers2 {6, 5, 7, 0, 2, 4, 1, 3};
        cpplinq::from(easy_label) >>
            cpplinq::zip_with(cpplinq::from(answers2)) >>
            cpplinq::for_each([](const auto& pair){ BOOST_CHECK(pair.first == pair.second); });
    }
    
    void test_execute_dense_nauty_2()
    {
        NautyGraph nauty_graph {};
        nauty_graph.set_vertex_number(8);
        
        nauty_graph.make_graph();
        
        nauty_graph.add_edge(7, 4);
        nauty_graph.add_edge(4, 0);
        nauty_graph.add_edge(0, 2);
        nauty_graph.add_edge(2, 7);
        
        nauty_graph.add_edge(0, 5);
        nauty_graph.add_edge(5, 1);
        nauty_graph.add_edge(1, 2);
        nauty_graph.add_edge(2, 5);
        nauty_graph.add_edge(0, 1);
        
        nauty_graph.add_edge(5, 3);
        nauty_graph.add_edge(3, 6);
        nauty_graph.add_edge(6, 1);
        
        std::vector<int> src_label  {0, 2, 1, 3, 4, 5, 6, 7};
        std::vector<int> ptn        {1, 0, 1, 1, 1, 1, 1, 0};
        nauty_graph.set_partition(src_label, ptn);
        
        nauty_graph.execute_dense_nauty();
        const auto& dst_label = nauty_graph.get_label();
        const auto& dst_ptn = nauty_graph.get_ptn();
        
        const bool answer[] = {true, false, true, true, true, true, true, false};
        cpplinq::from(dst_ptn) >>
            cpplinq::zip_with(cpplinq::from_array(answer)) >>
            cpplinq::for_each(
                [](const auto& pair)
                {
                    BOOST_CHECK((pair.first != 0) == pair.second);
                }
            );
        
        const std::vector<int> answer1  {0, 2, 3, 6, 4, 7, 5, 1};
        cpplinq::from(dst_label) >>
            cpplinq::zip_with(cpplinq::from(answer1)) >>
            cpplinq::for_each([](const auto& pair){ BOOST_CHECK(pair.first == pair.second); });
        
        const auto& easy_label = nauty_graph.get_easy_label();
        const std::vector<int> answers2 {0, 7, 1, 2, 4, 6, 3, 5};
        cpplinq::from(easy_label) >>
            cpplinq::zip_with(cpplinq::from(answers2)) >>
            cpplinq::for_each([](const auto& pair){ BOOST_CHECK(pair.first == pair.second); });
    }

    void test_execute_dense_nauty_3()
    {
        NautyGraph nauty_graph {};
        nauty_graph.set_vertex_number(13);
        
        nauty_graph.make_graph();
        
        nauty_graph.add_edge(0, 2);
        nauty_graph.add_edge(1, 2);
        nauty_graph.add_edge(2, 3);
        nauty_graph.add_edge(3, 7);
        
        nauty_graph.add_edge(7, 11);
        nauty_graph.add_edge(11, 10);
        nauty_graph.add_edge(10, 9);
        nauty_graph.add_edge(9, 5);
        nauty_graph.add_edge(5, 1);
        
        nauty_graph.add_edge(10, 12);
        nauty_graph.add_edge(4, 5);
        nauty_graph.add_edge(7, 8);
        nauty_graph.add_edge(2, 6);
        nauty_graph.add_edge(5, 6);
        nauty_graph.add_edge(6, 7);
        nauty_graph.add_edge(6, 10);

        
        std::vector<int> src_label  {0, 1, 3, 4, 6, 8, 9, 11, 12, 2, 7, 5, 10};
        std::vector<int> ptn        {0, 0, 0, 0, 0, 0,  0, 0,  0, 1, 1,  1, 0};
        
        nauty_graph.set_partition(src_label, ptn);
        
        nauty_graph.execute_dense_nauty();
        const auto& dst_label = nauty_graph.get_label();
        const auto& dst_ptn = nauty_graph.get_ptn();

        cpplinq::from(dst_label) >> cpplinq::for_each([](auto i){ std::cout << i << ","; });
        std::cout << std::endl;
        cpplinq::from(dst_ptn) >> cpplinq::for_each([](auto i){ std::cout << i << ","; });
        std::cout << std::endl;
//        const bool answer[] = {true, false, true, true, true, true, true, false};
//        cpplinq::from(dst_ptn) >>
//            cpplinq::zip_with(cpplinq::from_array(answer)) >>
//            cpplinq::for_each(
//                [](const auto& pair)
//                {
//                    BOOST_CHECK((pair.first != 0) == pair.second);
//                }
//            );
//        
//        const std::vector<int> answer1  {0, 2, 3, 6, 4, 7, 5, 1};
//        cpplinq::from(dst_label) >>
//            cpplinq::zip_with(cpplinq::from(answer1)) >>
//            cpplinq::for_each([](const auto& pair){ BOOST_CHECK(pair.first == pair.second); });
//        
//        const auto& easy_label = nauty_graph.get_easy_label();
//        const std::vector<int> answers2 {0, 7, 1, 2, 4, 6, 3, 5};
//        cpplinq::from(easy_label) >>
//            cpplinq::zip_with(cpplinq::from(answers2)) >>
//            cpplinq::for_each([](const auto& pair){ BOOST_CHECK(pair.first == pair.second); });

/*

        0
    
    1   2*   3
 
4   5*   6   7*   8

    9   10*  11
    
        12


        0
    
    4   9*   10
 
2   5*   8   11*   3

    6   12*  7
    
         1

0->0,1->1,3->2,4->3,6->4,8->5,9->6,11->7,12->8,2->9,5->10,7->11,10->12,
 
0->0,12->1,4->2,8->3,1->4,3->5,9->6,11->7,6->8,2->9,5->10,7->11,10->12,
*/
    }
}

BOOST_AUTO_TEST_CASE(TEST_NautyGraph)
{
    std::cout << "NautyGraph\n";
    test_constructor();
    test_set_vertex_number();
    test_make_graph();
    test_add_edge();
    test_execute_dense_nauty_1();
    test_execute_dense_nauty_2();
    test_execute_dense_nauty_3();
}
#endif // UNIT_TEST

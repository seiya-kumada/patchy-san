//
//  main.cpp
//  opencascade_sample
//
//  Created by Seiya KUMADA on 2016/12/22.
//  Copyright (c) 2016年 kumada. All rights reserved.
//

//#include <opencascade/gp_Pnt.hxx>
//#include <opencascade/gp_Vec.hxx>
#include <iostream>
//#include <functional>
//#include <opencascade/Standard_Macro.hxx>
//#include <opencascade/TopAbs_ShapeEnum.hxx>
//#include <opencascade/TopoDS.hxx>
//#include <opencascade/TopoDS_Shape.hxx>
//#include <opencascade/TopoDS_Face.hxx>
//#include <opencascade/TopExp_Explorer.hxx>
//#include <opencascade/TColgp_Array1OfPnt.hxx>
//#include <opencascade/TColgp_HArray1OfPnt.hxx>
//#include <opencascade/IGESControl_Reader.hxx>
#include <opencascade/STEPControl_Reader.hxx>
//#include <opencascade/GeomAPI_Interpolate.hxx>
//#include <opencascade/Geom_BSplineCurve.hxx>
//#include <opencascade/BRepBuilderAPI_MakeEdge.hxx>
//#include <opencascade/BRepBuilderAPI_MakeVertex.hxx>
//#include <opencascade/BRepBuilderAPI_MakePolygon.hxx>
//#include <opencascade/BOPAlgo_BOP.hxx>
//#include <opencascade/BRepBuilderAPI_MakeFace.hxx>
//#include <opencascade/BRepGProp.hxx>
//#include <opencascade/GProp_GProps.hxx>
//#include <opencascade/BRepPrimAPI_MakeBox.hxx>
//#include <opencascade/BRepBuilderAPI_MakeWire.hxx>
//#include <opencascade/Geom_BezierSurface.hxx>
//#include <opencascade/TColgp_Array2OfPnt.hxx>
//#include <opencascade/BRepAlgoAPI_Common.hxx>
//#include <opencascade/gp_Pln.hxx>
//#include <opencascade/gp_Ax3.hxx>
//#include <string>
//#include <vector>
//#include <boost/range/irange.hpp>
//#include <boost/range/algorithm/for_each.hpp>
//#include <boost/range/adaptor/filtered.hpp>
//#include <cpplinq.hpp>
//#include <BRepPrimAPI_MakeBox.hxx>
//#include <BrepTools.hxx>
#include <boost/filesystem.hpp>
#include "processes.h"
#include <opencascade/BRepTools.hxx>

namespace fs = boost::filesystem;

/*
    There is no namespace.
    
    -lTKernel -lTKMath -lTKG2d -lTKG3d -lTKGeomBase -lTKBRep -lTKGeomAlgo -lTKTopAlgo -lTKPrim -lTKBO -lTKShHealing -lTKBool -lTKHLR -lTKFillet -lTKOffset -lTKFeat -lTKMesh -lTKXMesh -lTKService -lTKV3d -lTKOpenGl -lTKMeshVS -lTKCDF -lTKLCAF -lTKCAF -lTKBinL -lTKXmlL -lTKBin -lTKXml -lTKStdL -lTKStd -lTKTObj -lTKBinTObj -lTKXmlTObj -lTKVCAF -lTKXSBase -lTKSTEPBase -lTKSTEPAttr -lTKSTEP209 -lTKSTEP -lTKIGES -lTKXCAF -lTKXDEIGES -lTKXDESTEP -lTKSTL -lTKVRML -lTKXmlXCAF -lTKBinXCAF -lTKDraw -lTKTopTest -lTKViewerTest -lTKXSDRAW -lTKDCAF -lTKXDEDRAW -lTKTObjDRAW -lTKQADraw
    
    sample collections
    http://dyama.org/?s=opencascade
*/

//int sample_0()
//{
//    auto p1 = gp_Pnt{0, 0, 0};
//    auto p2 = gp_Pnt{1, 0, 0};
//    auto v1 = gp_Vec{p1, p2};
//
//    auto p3 = gp_Pnt{1, 2, 0};
//    auto p4 = gp_Pnt{2, 3, 0};
//    auto v2 = gp_Vec{p3, p4};
//    
//    if (v1.IsParallel(v2, 0) == Standard_True)
//    {
//        std::cout << "parallel!" << std::endl;
//    }
//    else
//    {
//        std::cout << "not parallel!" << std::endl;
//    }
//    return 0;
//}

const auto paths = std::vector<std::string>{
    "/Volumes/Untitled/mac/Data/3dmodel-retrieval/step/JPN2015100800926-1_orig.stp", // unknown entities
    "/Volumes/Untitled/mac/Data/3dmodel-retrieval/step/JPN2016021100025_orig.stp",
    "/Volumes/Untitled/mac/Data/3dmodel-retrieval/step/sample3.step",
    "/Volumes/Untitled/mac/Data/3dmodel-retrieval/step/stepped_pin.step",
};

//template<typename T>
//struct Type;
//
//int sample_1(const std::string& path)
//{
//    auto reader = IGESControl_Reader{};
//    if (reader.ReadFile(path.c_str()) != IFSelect_RetDone)
//    {
//        reader.PrintCheckLoad(Standard_True, IFSelect_ItemsByEntity);
//        return 1;
//    }
//    
//    std::cout << "number of roots = " << reader.NbRootsForTransfer() << std::endl;
//    
//    // convert igs format to OCC one.
//    reader.TransferRoots();
//    
//    std::cout << "number of shapes = " << reader.NbShapes() << std::endl;
//    
//    
//    
//    
//    const auto range = boost::irange(1, reader.NbShapes());
//    boost::for_each(range, [&reader](auto i){
//        auto s = reader.Shape(i);
//        if (s.ShapeType() == TopAbs_FACE)
//        {
//            const auto& f = TopoDS::Face(s); // downcast to TopoDS_Face
//            std::cout << "face: " << f.HashCode(0xffff) << std::endl;
//
//
//
//            auto c = 0;
//            auto explorer = TopExp_Explorer{f, TopAbs_EDGE};
//            for (; explorer.More(); explorer.Next())
//            {
//                const auto& e = TopoDS::Edge(explorer.Current());
//                std::cout << c << std::endl;
//                ++c;
//            }
            
//            while (explorer.More())
//            {
//                const auto& e = TopoDS::Edge(explorer.Current());
//                std::cout << c << std::endl;
//                ++c;
//                explorer.Next();
//                
//            }
            
//            auto explorer = TopExp_Explorer{f, TopAbs_VERTEX};
//            for (; explorer.More(); explorer.Next())
//            {
//                const auto v = TopoDS::Vertex(explorer.Current());
//                
//
//                const auto& u = TopoDS::Vertex(explorer.Current());
//                
//                
//                std::cout << c << std::endl;
//                ++c;
//            }
//            
//        }
//        
//        
//    
//    });
//    
//    std::cout << "---" << std::endl;
//    
//    auto result = range | boost::adaptors::filtered([&reader](auto i){ return reader.Shape(i).ShapeType() == TopAbs_FACE; });
//    boost::for_each(result, [&reader](auto i){
//        auto f = TopoDS::Face(reader.Shape(i));
//        std::cout << f.HashCode(0xffff) << std::endl;
//    });
//
//    std::cout << "---" << std::endl;
//
//    cpplinq::range(1, reader.NbShapes())
//        >> cpplinq::where([&reader](auto i){ return reader.Shape(i).ShapeType() == TopAbs_FACE; })
//        >> cpplinq::for_each([&reader](auto i){
//            auto f = TopoDS::Face(reader.Shape(i));
//            std::cout << f.HashCode(0xffff) << std::endl;
//        });
//    
//    auto s = reader.OneShape();
//    return 0;
//}
//
//void sample_2()
//{
//    // make a solid
//    auto opos = gp_Pnt{0.0, 0.0, 0.0};
//    auto box = BRepPrimAPI_MakeBox{opos, 10.0, 10.0, 10.0}; // BRepPrimAPI_MakeBox
//    auto solid = box.Solid(); // TopoDS_Solid
//    auto shell = box.Shell(); // TopoDS_Shell
//    
//
//    //TopoDS_Solid solid = BRepPrimAPI_MakeBox{opos, 10.0, 10.0, 10.0};
//    //TopoDS_Shell shell = BRepPrimAPI_MakeBox{opos, 10.0, 10.0, 10.0};
//    
//    
//    // write "solid"
//    const auto PATH = "/Users/seiya_kumada/Projects/opencascade_sample/opencascade_sample/test.brep";
//    BRepTools::Write(solid, PATH);
//    
//    // load "solid"
//    auto shape = TopoDS_Solid{};
//    auto bb = BRep_Builder{};
//    BRepTools::Read(shape, PATH, bb);
//
//    std::cout << "Readed shape type no is " << shape.ShapeType() << std::endl;
//}
//
//void sample_3()
//{
//    // make a solid
//    auto opos = gp_Pnt{0.0, 0.0, 0.0};
//    auto box = BRepPrimAPI_MakeBox{opos, 10.0, 10.0, 10.0}; // BRepPrimAPI_MakeBox
//    auto solid = box.Solid(); // TopoDS_Solid
//    auto shell = box.Shell(); // TopoDS_Shell
//    
//
//    //TopoDS_Solid solid = BRepPrimAPI_MakeBox{opos, 10.0, 10.0, 10.0};
//    //TopoDS_Shell shell = BRepPrimAPI_MakeBox{opos, 10.0, 10.0, 10.0};
//    
//    
//    // write "solid"
//    const auto PATH = "/Users/seiya_kumada/Projects/opencascade_sample/opencascade_sample/test_shell.brep";
//    BRepTools::Write(shell, PATH);
//    
//    // load "solid"
//    auto shape = TopoDS_Shell{};
//    auto bb = BRep_Builder{};
//    if (BRepTools::Read(shape, PATH, bb))
//    {
//        std::cout << "OK" << std::endl;
//    }
//
//    std::cout << "Readed shape type no is " << shell.ShapeType() << std::endl;
//}
//
//void sample_4()
//{
//    auto origin = gp_Pnt{0.0, 0.0, 1.0};
//    auto box = BRepPrimAPI_MakeBox{origin, 3, 5, 2};
//    auto solid = box.Solid();
//    
//    // write to string stream
//    std::ostringstream oss;
//    BRepTools::Write(solid, oss);
//    std::cout << oss.str() << std::endl;
//    
//    // read from string stream
//    std::istringstream iss{oss.str()};
//    auto shape = TopoDS_Solid{};
//    auto bb = BRep_Builder{};
//    BRepTools::Read(shape, iss, bb);
//    std::cout << "Read shape type no is " << shape.ShapeType() << std::endl;
//}
//
//void sample_5()
//{
//    auto origin = gp_Pnt{0.0, 0.0, 1.0};
//    auto box = BRepPrimAPI_MakeBox{origin, 3, 5, 2};
//    auto shell = box.Shell();
//    
//    // write to string stream
//    std::ostringstream oss;
//    BRepTools::Write(shell, oss);
//    std::cout << oss.str() << std::endl;
//    
//    // read from string stream
//    std::istringstream iss{oss.str()};
//    auto shape = TopoDS_Shell{};
//    auto bb = BRep_Builder{};
//    BRepTools::Read(shape, iss, bb);
//    std::cout << "Read shape type no is " << shape.ShapeType() << std::endl;
//}
//
//void sample_6()
//{
//    const auto nb_pts = Standard_Integer{4}; // the number of points
//    Handle(TColgp_HArray1OfPnt) pary = new TColgp_HArray1OfPnt(1, nb_pts); // [0,nb_pts]
//    
//    std::cout << pary->Size() << std::endl;
//    
//    // resigter 4 points
//    pary->SetValue(1, gp_Pnt{0, 0, 0});
//    pary->SetValue(2, gp_Pnt{10, 0, 0});
//    pary->SetValue(3, gp_Pnt{10, 10, 0});
//    pary->SetValue(4, gp_Pnt{20, 20, 0});
//    
//    cpplinq::range(1, pary->Size()) >> cpplinq::for_each([&pary](auto i){
//        const auto& p = pary->Value(i);
//        std::cout << p.X() << ", " << p.Y() << ", " << p.Z() << std::endl;
//    });
//    
//    // tolerance
//    const auto tol = Standard_Real{1.0e-7};
//
//    // make a bspline curve
//    auto intp = GeomAPI_Interpolate{pary, Standard_False, tol};
//    intp.Perform();
//    const auto& hgeom_bspc = intp.Curve(); // get a curve
//
//    // make an edge from the bspline curve
//    TopoDS_Edge e = BRepBuilderAPI_MakeEdge{hgeom_bspc};
//}
//
//void sample_7()
//{
//    auto poles = TColgp_Array1OfPnt{0, 3};
//    poles.SetValue(0, gp_Pnt{100,   0,  0});
//    poles.SetValue(1, gp_Pnt{ 70, -10, 10});
//    poles.SetValue(2, gp_Pnt{ 30,  40, 10});
//    poles.SetValue(3, gp_Pnt{  0,   0,  0});
//    
////    cpplinq::range(0, poles.Size()) >> cpplinq::for_each([&poles](auto i){
////        const auto& p = poles.Value(i);
////        std::cout << p.X() << ", " << p.Y() << ", " << p.Z() << std::endl;
////    });
//    
//    auto weights = TColStd_Array1OfReal{0, 3};
//    weights.SetValue(0, 1.0);
//    weights.SetValue(1, 1.0);
//    weights.SetValue(2, 1.2);
//    weights.SetValue(3, 1.0);
//
//    auto knots = TColStd_Array1OfReal{0,2};
//    knots.SetValue(0, 0.0);
//    knots.SetValue(1, 1.0);
//    knots.SetValue(2, 2.0);
//    
//    auto mults = TColStd_Array1OfInteger{0, 2};
//    mults.SetValue(0, 3);
//    mults.SetValue(1, 1);
//    mults.SetValue(2, 3);
//    
//    const auto dim = 2;
//    Handle(Geom_BSplineCurve) hgeom_bscurve = new Geom_BSplineCurve{poles, weights, knots, mults, dim, Standard_False};
//    
////    TopoDS_Edge e = BRepBuilderAPI_MakeEdge{hgeom_bscurve};
////    auto explorer = TopExp_Explorer{e, TopAbs_VERTEX};
////    
////    std::ofstream ofs{"/Users/seiya_kumada/Projects/opencascade_sample/opencascade_sample/hoge.txt"};
////    for (; explorer.More(); explorer.Next())
////    {
////        const auto& v = TopoDS::Vertex(explorer.Current());
////        const auto& p = BRep_Tool::Pnt(v);
////        ofs << p.X() << " " << p.Y() << " " << p.Z() << std::endl;
////        std::cout << p.X() << " " << p.Y() << " " << p.Z() << std::endl;
////    }
//
////    TopoDS_Edge e = BRepBuilderAPI_MakeEdge{hgeom_bscurve};
////    auto explorer = TopExp_Explorer{e, TopAbs_VERTEX};
////    
////    std::ofstream ofs{"/Users/seiya_kumada/Projects/opencascade_sample/opencascade_sample/hoge.txt"};
////    for (; explorer.More(); explorer.Next())
////    {
////        const auto& v = TopoDS::Vertex(explorer.Current());
////        const auto& p = BRep_Tool::Pnt(v);
////        ofs << p.X() << " " << p.Y() << " " << p.Z() << std::endl;
////        std::cout << p.X() << " " << p.Y() << " " << p.Z() << std::endl;
////    }
//
//
//    auto w = BRepBuilderAPI_MakeEdge{hgeom_bscurve};
//    
//}
//
//void sample_8()
//{
//    
//    auto p = gp_Pnt{10, 20, 0};
//    TopoDS_Vertex v = BRepBuilderAPI_MakeVertex{p};
//}
//
//void sample_9()
//{
//    const auto p = gp_Pnt{10, 20, 0};
//    auto mv = BRepBuilderAPI_MakeVertex{p};
//    if (mv.IsDone())
//    {
//        const auto& v = mv.Vertex();
//        const auto& s = mv.Shape();
//    } else
//    {
//        std::cout << "ERROR\n";
//    }
//}
//
//void sample_10()
//{
//    const auto start_point = gp_Pnt{0, 0, 0};
//    const auto end_point = gp_Pnt{10, 20, 0};
//    
//    auto me = BRepBuilderAPI_MakeEdge(start_point, end_point);
//    if (me.IsDone())
//    {
//        const auto& e = me.Edge();
//        const auto& s = me.Shape();
//    }
//    else
//    {
//        std::cout << "ERROR\n";
//    }
//}
//
//void sample_11()
//{
//    auto mp = BRepBuilderAPI_MakePolygon{};
//    mp.Add(gp_Pnt{0, 0, 0});
//    mp.Add(gp_Pnt{10, 0, 0});
//    mp.Add(gp_Pnt{10, 10, 0});
//    mp.Add(gp_Pnt{20, 10, 0});
//    
//    mp.Build();
//    if (mp.IsDone())
//    {
//        const auto& e = mp.Edge();
//        const auto& w = mp.Wire();
//        const auto& s = mp.Shape();
//        
//        auto explorer = TopExp_Explorer{e, TopAbs_VERTEX};
//        for (; explorer.More(); explorer.Next())
//        {
//            const auto& v = TopoDS::Vertex(explorer.Current());
//            const auto& p = BRep_Tool::Pnt(v);
////            std::cout << p.X() << " " << p.Y() << " " << p.Z() << std::endl;
//        }
//
//        
//        
//
//    }
//}
//
//void sample_12()
//{
//    constexpr auto umin = Standard_Real{-10};
//    constexpr auto umax = Standard_Real{ 10};
//    constexpr auto vmin = Standard_Real{-10};
//    constexpr auto vmax = Standard_Real{ 10};
//    
//    const auto pos = gp_Pnt{0, 0, 0};
//    const auto norm = gp_Dir{0, 0, 1};
//    const auto vdir = gp_Dir{0, 1, 0};
//    const auto ax = gp_Ax3{pos, norm, vdir};
//    const auto pln = gp_Pln{ax};
//    
//    TopoDS_Face f = BRepBuilderAPI_MakeFace{pln, umin, umax, vmin, vmax};
//}
//
//void sample_13()
//{
//    auto mp = BRepBuilderAPI_MakePolygon{};
//    mp.Add(gp_Pnt{0, 0, 0});
//    mp.Add(gp_Pnt{10, 0, 0});
//    mp.Add(gp_Pnt{10, 5, 0});
//    mp.Add(gp_Pnt{20, 5, 0});
//    mp.Add(gp_Pnt{20, 15, 0});
//    mp.Add(gp_Pnt{15, 12, 0});
//    mp.Add(gp_Pnt{5, 12, 0});
//    mp.Add(gp_Pnt{3, 10, 0});
//    mp.Add(gp_Pnt{0, 0, 0});
//    mp.Build();
//
//    if (mp.IsDone())
//    {
//        const auto& w = mp.Wire();
//        auto mf = BRepBuilderAPI_MakeFace(w, Standard_True); // closed face
//        mf.Build();
//        if (mf.IsDone())
//        {
//            const auto& f = mf.Face();
//        }
//    }
//}
//
//void sample_14()
//{
//    TColgp_Array2OfPnt poles(0, 3, 0, 3);
//    poles.SetValue(0, 0, gp_Pnt( 0,  0, 20));
//    poles.SetValue(0, 1, gp_Pnt( 0, 10, 20));
//    poles.SetValue(0, 2, gp_Pnt( 0, 20, 20));
//    poles.SetValue(0, 3, gp_Pnt( 0, 30, 20));
//    poles.SetValue(1, 0, gp_Pnt(10,  0, 10));
//    poles.SetValue(1, 1, gp_Pnt(10, 10, 10));
//    poles.SetValue(1, 2, gp_Pnt(10, 20,  5));
//    poles.SetValue(1, 3, gp_Pnt(10, 30,  0));
//    poles.SetValue(2, 0, gp_Pnt(20,  0,  0));
//    poles.SetValue(2, 1, gp_Pnt(20, 10,  5));
//    poles.SetValue(2, 2, gp_Pnt(20, 20, 10));
//    poles.SetValue(2, 3, gp_Pnt(20, 30, 10));
//    poles.SetValue(3, 0, gp_Pnt(30,  0, 20));
//    poles.SetValue(3, 1, gp_Pnt(30, 10, 20));
//    poles.SetValue(3, 2, gp_Pnt(30, 20, 20));
//    poles.SetValue(3, 3, gp_Pnt(30, 30, 20));
//    
//    Handle(Geom_BezierSurface) s = new Geom_BezierSurface{poles};
//    const TopoDS_Face f = BRepBuilderAPI_MakeFace{s, 1.0e-07};
//}
//
//void sample_15()
//{
//    // make s1
//    gp_Pnt opos1(0.0, 0.0, 0.0);
//    BRepPrimAPI_MakeBox box1(opos1, 10.0, 10.0, 10.0);
//    TopoDS_Solid s1 = box1.Solid();
//    
//    // make s2
//    gp_Pnt opos2(2.0, 3.0, 5.0);
//    BRepPrimAPI_MakeBox box2(opos2, 10.0, 10.0, 10.0);
//    TopoDS_Solid s2 = box2.Solid();
//    
//    BRepAlgoAPI_Common bo(s1, s2);
//    bo.SetOperation(BOPAlgo_CUT);
//    
//    bo.Build();
//    
//    if(!bo.ErrorStatus())
//    {
//        const auto& s = bo.Shape();
//        GProp_GProps gprops;
//        BRepGProp::VolumeProperties(s, gprops);
//        Standard_Real vol = gprops.Mass();
//        
//        std::cout << "volume: " << vol << std::endl;
//    }
//}

//https://www.opencascade.com/doc/occt-6.7.0/overview/html/occt_brep_format.html
int read_step_(const std::string& path)
{
    if (!fs::exists(path))
    {
        std::cout << "file not found\n";
        return 1;
    }
    else
    {
        std::cout << "file found\n";
    }

    auto fspath = fs::path{path};
    auto stem = fspath.stem();
    auto dirname = fspath.parent_path();
    auto output_path = dirname / (stem.string() + "_brep.txt");
    
    auto reader = STEPControl_Reader{};
    if (reader.ReadFile(path.c_str()) != IFSelect_RetDone)
    {
        reader.PrintCheckLoad(Standard_True, IFSelect_ItemsByEntity);
        std::cout << "something wrong\n";
        return 1;
    }
    
    reader.TransferRoots();
    const auto shape = reader.OneShape();
    BRepTools::Write(shape, output_path.c_str());
    return 0;
}

int read_step(const std::string& path)
{
    if (!fs::exists(path))
    {
        std::cout << "file not found\n";
        return 1;
    }
    else
    {
        std::cout << "file found\n";
    }

    auto fspath = fs::path{path};
    auto stem = fspath.stem();
    auto dirname = fspath.parent_path();
    auto output_path = dirname / (stem.string() + ".txt");
    
    //std::cout << output_path << std::endl;
    
    auto reader = STEPControl_Reader{};
    if (reader.ReadFile(path.c_str()) != IFSelect_RetDone)
    {
        reader.PrintCheckLoad(Standard_True, IFSelect_ItemsByEntity);
        std::cout << "something wrong\n";
        return 1;
    }
    
    auto ofs = std::ofstream{output_path.c_str()};
    reader.TransferRoots();
    const auto shape = reader.OneShape();
    const auto shapeType = shape.ShapeType();
    Process::processors[shapeType](shape, " ", ofs);
    return 0;
}


int main(int argc, const char * argv[])
{
    for (auto i = 0; i < paths.size(); ++i )
    {
        read_step_(paths[i]);
    }
    return 0;
}

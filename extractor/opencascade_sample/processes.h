//
//  processes.h
//  opencascade_sample
//
//  Created by Seiya KUMADA on 2017/01/09.
//  Copyright (c) 2017年 kumada. All rights reserved.
//

#ifndef opencascade_sample_processes_h
#define opencascade_sample_processes_h


#include <string>
#include <map>
#include <opencascade/TopAbs_ShapeEnum.hxx>


class TopoDS_Shape;

namespace detail
{
    class GeometryWatcher
    {
    public:
        virtual void operator()(const TopoDS_Shape& s, const std::string& offset, std::ostream& os) const {}
    };
}

class Process
{
public:
    static void process_TopAbs_COMPOUND(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_COMPSOLID(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_SOLID(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_SHELL(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_FACE(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_WIRE(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_EDGE(const TopoDS_Shape&, const std::string& msg, std::ostream&);
    static void process_TopAbs_VERTEX(const TopoDS_Shape&, const std::string& msg, std::ostream&);

    using ProcessFunc = std::function<void(const TopoDS_Shape&, const std::string& msg, std::ostream&)>;
    static std::map<TopAbs_ShapeEnum, ProcessFunc> processors;
    
private:
    static void process(
        const TopoDS_Shape& s,
        const std::string& offset,
        const std::string& src_shape,
        TopAbs_ShapeEnum senum,
        std::ostream&,
        const detail::GeometryWatcher& watcher);
};
#endif

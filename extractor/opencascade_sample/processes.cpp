//
//  processes.cpp
//  opencascade_sample
//
//  Created by Seiya KUMADA on 2017/01/09.
//  Copyright (c) 2017年 kumada. All rights reserved.
//

#include "processes.h"
#include <opencascade/TopoDS.hxx>
#include <opencascade/TopExp_Explorer.hxx>
#include <opencascade/TopAbs_ShapeEnum.hxx>
#include <opencascade/TopAbs.hxx>
#include <opencascade/TopoDS_Compound.hxx>
#include <opencascade/TopoDS_Solid.hxx>
#include <opencascade/TopoDS_Face.hxx>
#include <opencascade/TopoDS_Shell.hxx>
#include <opencascade/TopoDS_Edge.hxx>
#include <opencascade/TopoDS_Wire.hxx>
#include <opencascade/BRep_Tool.hxx>

std::map<TopAbs_ShapeEnum, Process::ProcessFunc> Process::processors = {
    {TopAbs_COMPOUND, Process::process_TopAbs_COMPOUND},
    {TopAbs_COMPSOLID, Process::process_TopAbs_COMPSOLID},
    {TopAbs_SOLID, Process::process_TopAbs_SOLID},
    {TopAbs_SHELL, Process::process_TopAbs_SHELL},
    {TopAbs_FACE, Process::process_TopAbs_FACE},
    {TopAbs_WIRE, Process::process_TopAbs_WIRE},
    {TopAbs_EDGE, Process::process_TopAbs_EDGE},
    {TopAbs_VERTEX, Process::process_TopAbs_VERTEX}
};

namespace detail
{
    class EdgeWatcher : public GeometryWatcher
    {
    public:
        virtual void operator()(const TopoDS_Shape& s, const std::string& offset, std::ostream& os) const
        {
            
            os << offset;
            os << "is closed: " << BRep_Tool::IsClosed(s) << std::endl;
            
        }
    };
    
    class VertexWatcher : public GeometryWatcher
    {
    public:
        virtual void operator()(const TopoDS_Shape& s, const std::string& offset, std::ostream& os) const
        {
            os << "TopAbs_VERTEX (";
            const auto& v = TopoDS::Vertex(s);
            const auto& p = BRep_Tool::Pnt(v);
            os << p.X() << ", " << p.Y() << ", " << p.Z() << ")" << std::endl;
        }
    
    };
}

void Process::process(
    const TopoDS_Shape& s,
    const std::string& offset,
    const std::string& src_shape,
    TopAbs_ShapeEnum senum,
    std::ostream& os,
    const detail::GeometryWatcher& watcher)
{

    os << src_shape << std::endl;
    watcher(s, offset, os);
    const auto offs = offset + " ";
    auto explorer = TopExp_Explorer{s, senum};
    for (; explorer.More(); explorer.Next())
    {
        const auto& e = explorer.Current();
        os << offs;
        processors[senum](e, offs, os);
    }
}

// compound -> solid
void Process::process_TopAbs_COMPOUND(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_COMPOUND", TopAbs_SOLID, os, detail::GeometryWatcher());
}

// compsolid -> solid
void Process::process_TopAbs_COMPSOLID(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_COMPSOLID", TopAbs_SOLID, os, detail::GeometryWatcher());
}

// solid -> shell
void Process::process_TopAbs_SOLID(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_SOLID", TopAbs_SHELL, os, detail::GeometryWatcher());
}

// shell -> face
void Process::process_TopAbs_SHELL(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_SHELL", TopAbs_FACE, os, detail::GeometryWatcher());
}

// face -> wire
void Process::process_TopAbs_FACE(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_FACE", TopAbs_WIRE, os, detail::GeometryWatcher());
}

// wire -> edge
void Process::process_TopAbs_WIRE(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_WIRE", TopAbs_EDGE, os, detail::GeometryWatcher());
}

// edge -> vertex
void Process::process_TopAbs_EDGE(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    process(s, offset, "TopAbs_EDGE", TopAbs_VERTEX, os, detail::EdgeWatcher());
}

void Process::process_TopAbs_VERTEX(const TopoDS_Shape& s, const std::string& offset, std::ostream& os)
{
    detail::VertexWatcher()(s, offset, os);
}


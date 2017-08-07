SRCDIR=./nauty_class/nauty_class

SRCS = $(SRCDIR)/NautyGraph.cpp
	 
OBJSDIR = ./obj

CXX = g++-4.9

EXE = ./lib/libnauty_graph.so

CFLAGS = -O3 -Wall -std=c++14 -Wno-unused-local-typedefs

LIBLIST = boost_python \
          stdc++ 

LIBDIRLIST = /usr/local/lib \
			 /usr/lib/ \
             /usr/lib/x86_64-linux-gnu

TESTLIST = 

DEFLIST = NDEBUG BOOST_PYTHON=1

INCLUDELIST = /usr/local/include \
			  /usr/local/nauty26r7/include \
			 $(SRCDIR) \
             /usr/include/python2.7

TESTS = $(patsubst %, -D%, $(TESTLIST))
INCLUDES = $(patsubst %, -I%, $(INCLUDELIST))
DEFS = $(patsubst %, -D%, $(DEFLIST))

OBJS = $(patsubst %.cpp, $(OBJSDIR)/%.o, $(SRCS))
LIBS = $(patsubst %, -l%, $(LIBLIST))
LIBDIR = $(patsubst %, -L%, $(LIBDIRLIST))

# make rules -----------------------------------------------------------

$(EXE): $(OBJS)
#	$(CXX) $(LIBDIR) $(LIBS) $(CFLAGS) -o $@ $^
	$(CXX) -shared $(CFLAGS) -o $@ $^  $(LIBDIR) $(LIBS) /usr/local/nauty26r7-fPIC/lib/nauty.a

$(OBJSDIR)/%.o: %.cpp
	$(CXX) -fPIC $(INCLUDES) $(DEFS) $(TESTS) $(CFLAGS) -o $@ -c $< 

# dependencies ---------------------------------------------------------

$(OBJSDIR)/$(SRCDIR)/NautyGraph.o: $(SRCDIR)/NautyGraph.hpp

.PHONY: clean
clean:
	 $(RM) $(OBJS) $(EXE) 

load:
	./$(EXE) 

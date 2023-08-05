PRODUCT := PreciSo

CXX := g++
LINKER := g++
INCDIRS := -I.
CXXFLAGS := -std=c++11 -Wall -Wextra

SRCFILES := $(wildcard *.cpp) 
OBJFILES := $(patsubst %.cpp,./build/objects/%.o,$(SRCFILES))
DEPFILES := $(patsubst %.cpp,./build/dependencies/%.d,$(SRCFILES))


all: $(PRODUCT)

$(PRODUCT): $(OBJFILES)
	@mkdir -p bin
	$(LINKER) $^ -o ./bin/$@

./build/objects/main.o: main.cpp
	$(CXX) $(CXXFLAGS) $(INCDIRS) -c $< -o $@ -lm
./build/objects/%.o: %.cpp %.h
	@mkdir -p build/objects
	$(CXX) $(CXXFLAGS) $(INCDIRS) -c $< -o $@

./build/dependencies/%.d: %.cpp
	@mkdir -p build/dependencies
	@$(CXX) $(INCDIRS) -MM $< > $@

-include $(DEPFILES)

.PHONY: clean
clean:
	rm -r -f bin build
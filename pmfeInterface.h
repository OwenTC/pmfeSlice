#include <string>
#include "parameterVector.h"

std::string interfacePath = "/home/owen/Documents/research/pmfe/pmfe-scorer";
std::string interfacePath = "/home/owen/Documents/research/pmfe/pmfe-scorer";


class pmfeInterface {
    public:
        pmfeInterface();
        parameterVector vertexOracle();
    private:
        std::string fastaPath;
};
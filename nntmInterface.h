#include <string>
#include "parameterVector.h"

class nntmInterface {
    public:
        nntmInterface();
        parameterVector vertexOracle();
    private:
        std::string fastaPath;
};
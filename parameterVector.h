


class ParameterVector {
    float multiloop_default = 3.4;
    float unpaired_default = 0;
    float branch_default = 0.4;
    float dummy_default = 1;

    public:
    ParameterVector(float multiloop_penalty = multiloop_default, float unpaired_penalty = unpaired_default, float branch_penalty = branch_default, float dummy_scaling = dummy_default) :
        multiloop_penalty(multiloop_penalty),
            unpaired_penalty(unpaired_penalty),
            branch_penalty(branch_penalty),
            dummy_scaling(dummy_scaling)
            {
            this->canonicalize();
        };
        Rational multiloop_penalty, unpaired_penalty, branch_penalty, dummy_scaling;


        void canonicalize() {
            multiloop_penalty.canonicalize();
            unpaired_penalty.canonicalize();
            branch_penalty.canonicalize();
            dummy_scaling.canonicalize();
        }

        std::string print_as_list();

        friend std::ostream& operator<<(std::ostream& os, const ParameterVector& params);
        friend bool operator==(const ParameterVector& a, const ParameterVector& b);
        friend bool operator!=(const ParameterVector& a, const ParameterVector& b);
};
from pmfeInterface import pmfeInterface

interface = pmfeInterface("/home/owen/Documents/research/pmfe/", "/home/owen/Documents/research/RNA_Data/tRNA/tRNA_50/fasta/Aquifex.aeolicus.VF5_AE000657.fasta", True)

print(interface.vertex_oracle(-22, 0, -16, 1))
print(interface.subopt_oracle(5, 0, 5, 1))
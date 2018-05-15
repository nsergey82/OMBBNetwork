import re
import glob
import sys

protos = []
barrels = []
with open("CompCodesE-2.txt", "r") as barrel_codes:
    for line in barrel_codes:
        line = line.strip().split("\t")
        barrels.append(line[0])
        if line[1] == "1":
            protos.append(line[0])

barrel_sizes = [[] for x in range(27)]
with open("BarrelChars85.txt", "r") as barrel_data:
    for line in barrel_data:
        if "PDB" not in line:
            line = line.split("\t")
            if line[0] in protos:
                barrel_sizes[ int(line[1]) ].append(line[0])

cutoff = 1e-2
for x in range(27):
    for y in range(x+1, 27):
        keep_lines = []
        with open("data/AllDataE20_v6_Numbered.txt", "r") as inData:
            for line in inData:
                if "Dom1" in line:
                    keep_lines.append(line.strip().split(" "))
                else:
                    line = line.strip().split(" ")
                    pdb1 = line[1]
                    pdb2 = line[2]
                    
                    if float(line[3]) <= cutoff:
                        if pdb1 in barrel_sizes[x] and pdb2 in barrel_sizes[y]:
                            keep_lines.append(line)
                        elif pdb1 in barrel_sizes[y] and pdb2 in barrel_sizes[x]:
                            keep_lines.append(line)
                        else:
                            continue
        if len(keep_lines) > 1:
            with open("data/BtwnBarrels/%s_%s_E-2.txt"%(x, y), "w+") as subnetwork:
                for value in keep_lines:
                    subnetwork.write("\t".join(value) + "\n")


from asf_tools.hand.HAND_gridsearch import *


flistfile = "flist.txt"

with open(flistfile, "r") as f:
    filelist = f.readlines()

out_dir = "."

for file in filelist:
    plot_hand(file.rstrip(), out_dir)



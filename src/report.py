from os.path import isfile
import pandas as pd

direc = 'data/'
# Add algos here
algos = ['DE','PSODE','JADE','DL']
fns = [i for i in range(1,31)]

# we used following dimensions
dims = [10,30,50,100]
#done = {i:{} for i in algos}
remaining = {str(i):[] for i in dims}

for dim in dims:
	for algo in algos:
		for fn in fns:
			filename1 = direc + str(algo) + "_" + str(dim) + "D_F" + str(fn) + "_graph.npy"
			filename2 = direc + str(algo) + "_" + str(dim) + "D_F" + str(fn) + "_values.npy"
			if (not isfile(filename1)) or (not isfile(filename2)):
				remaining[str(dim)].append({'Algo' : str(algo), 'Fn' : str(fn)})
				
for dim in dims:	
	print("\n#######################\n DIM : " + str(dim) + "    (missing npy files)")
	df = pd.DataFrame(remaining[str(dim)])
	print df
	

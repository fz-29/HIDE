import numpy as np
from matplotlib import pyplot as plt
import sys

if __name__ == '__main__':
	f_id = sys.argv[1]
	dim = sys.argv[2]

	base_name = '_' + str(dim) + 'D_F' + str(f_id) + '_'
	values = 'values.npy'
	graph = 'graph.npy'

	algos = ['DE', 'JADE', 'PSODE','DL']

	vals = []
	plots = []

	for alg in algos:
		file_values = np.load('./data/' + alg + base_name + values)
		file_graph = np.load('./data/' + alg + base_name + graph)

		vals.append(file_values.min())
		plots.append(file_graph[file_values.argmin()])

	for ix in range(len(plots)):
		plt.plot(plots[ix][:100])
		print vals[ix]
	plt.legend(algos)
	plt.show()

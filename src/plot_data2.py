import numpy as np
from matplotlib import pyplot as plt
from random import uniform
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
	
	# normalization
	for ix in range(len(plots)):
		z = plots[ix][0]
		for j in xrange(1,101,1):
			if(plots[ix][j] > z):
				plots[ix][j] = z
			z = plots[ix][j]	

	f = plt.figure(0)
	
	
	
	legend_algos = ['DE', 'JADE', 'PSODE', 'HIDE']
	markers = ['-','-', '-', '--'] 
	color	 = ['c', 'g','y' ,'k']
	line_width = [1.2,1.2,1.4, 2.5]
	for ix in range(len(plots)):
		plt.plot(plots[ix][:100], color = color[ix], ls = markers[ix], linewidth = line_width[ix])
		print vals[ix]
		
	plt.legend(legend_algos)
	plt.xlabel("No. of iterations")
	plt.ylabel("Objective function value")
	plt.title("function:" + str(f_id) + ", dimension:" + str(dim))
	# plt.show()

	f.savefig('./plot' + base_name + 'save.jpeg')
	#f.savefig('./plot' + base_name + 'save.jpeg')

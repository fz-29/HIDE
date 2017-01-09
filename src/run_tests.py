import numpy as np
import sys

from differential_evolution import DE
from distributed_leaders import DL
from PSO_DE import PSO_DE


if __name__ == '__main__':

	DIM = int(sys.argv[2])
	ITER = 2000
	n_runs = 40
	F_ID = int(sys.argv[1])

	values = []
	data = []

	try:
		for ix in range(n_runs):
			# algo = DL(num_iterations=ITER, dim=DIM, algo_type=0, n_leaders=5, population_size=25, print_status=True, stats_freq=10, visualize=False, f_id=F_ID)#, vec=[0.85, 1.0, 1.0, 1.0])
			algo = DE(num_iterations=ITER*DIM, dim=DIM, CR=0.4, F=0.48, population_size=30, print_status=False, visualize=False, f_id=F_ID)
			val, d = algo.simulate()
			values.append(val)
			data.append(d)

		values = np.asarray(values)
		data = np.asarray(data)

		np.save('./data/DE_' + str(DIM) + 'D_F'+str(F_ID)+'_values', values)
		np.save('./data/DE_' + str(DIM) + 'D_F'+str(F_ID)+'_graph', data)

		f = open('./success.txt','w+')
		msg = "DE Dim : " + str(DIM) +" F_ID : " + str(F_ID) + "\n"
		f.write("Success\n")
		f.close()
	except:
		f = open('./log.txt','w+')
		error = "DE Dim :" + str(DIM) +" F_ID : " + str(F_ID) + "\n"
		f.write(error)
		f.write("\n")
		f.close()


	values = []
	data = []

	try:
		for ix in range(n_runs):
			algo = DL(num_iterations=ITER, dim=DIM, algo_type=0, n_leaders=5, population_size=25, print_status=False, stats_freq=10, visualize=False, f_id=F_ID)#, vec=[0.85, 1.0, 1.0, 1.0])
			val, d = algo.simulate()
			values.append(val)
			data.append(d)

		values = np.asarray(values)
		data = np.asarray(data)

		np.save('./data/DL_' + str(DIM) + 'D_F'+str(F_ID)+'_values', values)
		np.save('./data/DL_' + str(DIM) + 'D_F'+str(F_ID)+'_graph', data)

		f = open('./success.txt','w+')
		msg = "DL Dim : " + str(DIM) +" F_ID : " + str(F_ID) + "\n"
		f.write("Success\n")
		f.close()
	except:
		f = open('./log.txt','w+')
		error = "DL Dim :" + str(DIM) +" F_ID : " + str(F_ID) + "\n"
		f.write(error)
		f.write("\n")
		f.close()
	
	"""
	values = []
	data = []

	try:
		for ix in range(n_runs):
			algo = PSO_DE(num_iterations=ITER, dim=DIM, algo_type=0, n_leaders=7, population_size=25, print_status=False, stats_freq=10, visualize=False, f_id=F_ID)#, vec=[0.85, 1.0, 1.0, 1.0])
			val, d = algo.simulate()
			values.append(val)
			data.append(d)

		values = np.asarray(values)
		data = np.asarray(data)

		np.save('./data/PSODE_' + str(DIM) + 'D_F'+str(F_ID)+'_values', values)
		np.save('./data/PSODE_' + str(DIM) + 'D_F'+str(F_ID)+'_graph', data)
	except:
		f = open('./log.txt','w+')
		error = "PSODE Dim :" + str(DIM) +" F_ID : " + str(F_ID) + "\n"
		f.write(error)
		f.write("\n")
	"""




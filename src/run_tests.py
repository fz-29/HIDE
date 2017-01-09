import numpy as np
import sys

from differential_evolution import DE
from distributed_leaders import DL
from PSO_DE import PSO_DE
from jade import JADE

def log_success(algo, dim, f_id):
	f = open('./success.txt','a+')
	msg = algo + " Dim : " + str(dim) +" F_ID : " + str(f_id) + "\n"
	f.write(msg)
	f.close()

def log_error(algo, dim, f_id):
	f = open('./log.txt','a+')
	msg = algo + " Dim : " + str(dim) +" F_ID : " + str(f_id) + "\n"
	f.write(msg)
	f.close()

if __name__ == '__main__':

	DIM = int(sys.argv[2])
	ITER = 10
	n_runs = 1
	F_ID = int(sys.argv[1])

	values = []
	data = []

	#DE
	
	try:
		for ix in range(n_runs):
			algo = DE(num_iterations=min(40*DIM,ITER), dim=DIM, CR=0.4, F=0.48, population_size=30, print_status=False, visualize=False, f_id=F_ID)
			val, d = algo.simulate()
			values.append(val)
			data.append(d)

		values = np.asarray(values)
		data = np.asarray(data)

		np.save('./data/DE_' + str(DIM) + 'D_F'+str(F_ID)+'_values', values)
		np.save('./data/DE_' + str(DIM) + 'D_F'+str(F_ID)+'_graph', data)
		log_success("DE", DIM, F_ID)
		
	except:
		log_error("DE", DIM, F_ID)
	"""
	#DL
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
		f.write(msg)
		f.close()
	except:
		f = open('./log.txt','w+')
		error = "DL Dim :" + str(DIM) +" F_ID : " + str(F_ID) + "\n"
		f.write(error)
		f.write("\n")
		f.close()
	"""

	#PSODE
	values = []
	data = []

	try:
		for ix in range(n_runs):
			algo = PSO_DE(num_iterations=ITER, dim=DIM, population_size=50, phi_p=2.00, phi_g=2.00, w=0.7, CR=0.48, F=0.5, print_status=True, visualize=False)
			val, d = algo.simulate()
			values.append(val)
			data.append(d)

		values = np.asarray(values)
		data = np.asarray(data)

		np.save('./data/PSODE_' + str(DIM) + 'D_F'+str(F_ID)+'_values', values)
		np.save('./data/PSODE_' + str(DIM) + 'D_F'+str(F_ID)+'_graph', data)

		log_success("PSODE", DIM, F_ID)
	except:
		log_error("PSODE", DIM, F_ID)

	#JADE
	values = []
	data = []

	try:
		for ix in range(n_runs):
			algo = JADE(num_iterations=ITER, dim=DIM, population_size=50, print_status=True, visualize=False)
			val, d = algo.simulate()
			values.append(val)
			data.append(d)

		values = np.asarray(values)
		data = np.asarray(data)

		np.save('./data/JADE_' + str(DIM) + 'D_F'+str(F_ID)+'_values', values)
		np.save('./data/JADE_' + str(DIM) + 'D_F'+str(F_ID)+'_graph', data)

		log_success("JADE", DIM, F_ID)
	except:
		log_error("JADE", DIM, F_ID)

	print "********************************\n********************************"
	print "Complete : D = " + str(DIM) + " F_ID = " + str(F_ID)
	print "********************************\n********************************"
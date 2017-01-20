import numpy as np
import os
import json
import copy

if __name__ == '__main__':
	f = os.listdir('./data')

	data_DE = {10: {}, 30: {}, 50: {}, 100: {}}
	data_JADE = {10: {}, 30: {}, 50: {}, 100: {}}
	data_PSODE = {10: {}, 30: {}, 50: {}, 100: {}}

	data = {'DE': data_DE, 'JADE': data_JADE, 'PSODE': data_PSODE}

	for fx in f:
		if 'values' in fx:
			dv = np.load('./data/' + fx)
			name = fx.split('_')
			algo = name[0]
			dim = int(name[1][:-1])
			f_id = int(name[2][1:])
			
			fill = dict({'best': 0, 'mean': 0, 'index': 0})

			fill['best'] = dv.min()
			fill['mean'] = dv.mean()
			fill['index'] = dv.argmin()

			data[algo][dim][f_id] = fill
		else:
			pass

	'''for fx in f:
		if 'graph' in fx:
			dv = np.load('./data/' + fx)
			name = fx.split('_')
			algo = name[0]
			dim = int(name[1][:-1])
			f_id = int(name[2][1:])
			indx = data[algo][dim][f_id]['index']

			data[algo][dim][f_id]['data'] = list(dv[indx, :])
		else:
			pass'''

	final_data = json.dumps(data)
	info = open('./analysis_data/vals_info.json', 'w')
	info.write(final_data)
	info.close()

	print 'Complete...'

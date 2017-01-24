import json
import numpy as np

def get_data(dim):
	all_data = ""
	# print sorted(data['DE'][dim].keys())
	keys_DE = set(data['DE'][dim].keys())
	keys_JADE = set(data['JADE'][dim].keys())
	keys_PSODE = set(data['PSODE'][dim].keys())
	keys_DL = set(data['DL'][dim].keys())

	keys = keys_PSODE.intersection(keys_DL.intersection(keys_DE.intersection(keys_JADE)))
	
	for fx in sorted([int(k) for k in keys]):
		d1 = data['DE'][dim][str(fx)]
		d2 = data['JADE'][dim][str(fx)]
		d3 = data['PSODE'][dim][str(fx)]
		d4 = data['DL'][dim][str(fx)]
		# print d['best'], d['mean']
		k = """{0}  & {1} & {2} & {3} & {4} & {5} & {6} & {7} & {8} \\\\ \n \\hline""".format(str(fx), round(d1['best'],6), round(d1['mean'],6), round(d2['best'],6), round(d2['mean'],6), round(d3['best'],6), round(d3['mean'],6), round(d4['best'],6), round(d4['mean'],6) )
		all_data += k
		all_data += '\n'
	return all_data

if __name__ == '__main__':
	f = open('./vals_info.json', 'rb')
	data = f.read()
	f.close()

	dims = ['10', '30', '50', '100']
	data = json.loads(data)

	for dx in range(len(dims)):
		filename = './dim' + str(dims[dx]) + '.tex'
		f = open(filename, 'w')
		texdata = ""
		texdata = get_data(dims[dx])
		f.write(texdata)
		f.close()

	print 'Done....'

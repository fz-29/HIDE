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
		k = """<tr>
		<td>{0}</td>
		<td>{1}</td>
		<td>{2}</td>
		<td>{3}</td>
		<td>{4}</td>
		<td>{5}</td>
		<td>{6}</td>
		<td>{7}</td>
		<td>{8}</td>
		</tr>""".format(str(fx), d1['best'], d1['mean'], d2['best'], d2['mean'], d3['best'], d3['mean'], d4['best'], d4['mean'])
		all_data += k
		all_data += '\n'
	return all_data

if __name__ == '__main__':
	f = open('./vals_info.json', 'rb')
	data = f.read()
	f.close()

	f = open('./data_table.html', 'r')
	html = f.read()
	f.close()

	html = html.split('##########')
	new_html = ""

	dims = ['10', '30', '50', '100']
	data = json.loads(data)

	for dx in range(len(dims)):
		new_html += html[dx]
		new_html += get_data(dims[dx])
	new_html += html[-1]

	# print new_html

	
	f = open('./index.html', 'w')
	f.write(new_html)
	f.close()

	print 'Done....'

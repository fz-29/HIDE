a=1

while [ $a -lt 31 ]
do
	python plot_data.py $a 10
	python plot_data.py $a 30
	python plot_data.py $a 50
	python plot_data.py $a 100
	a=`expr $a + 1`
done

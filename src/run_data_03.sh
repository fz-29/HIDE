a=1

while [ $a -lt 11 ]
do
	# python run_tests.py $a 10
	# python run_tests.py $a 30
	python run_tests.py $a 50
	# python run_tests.py $a 100
	a=`expr $a + 1`
done
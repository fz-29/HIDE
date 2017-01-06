a=1

while [ $a -lt 31 ]
do
	python run_tests.py $a
	a=`expr $a + 1`
done
import ctypes
import numpy

indata = numpy.array([[10.0, 2.24]])
outdata = numpy.zeros((1,2), dtype=numpy.double)


lib = ctypes.cdll.LoadLibrary('./objective.so')
func = lib.cec17_test_func
m = 1
n = 20
f_id = 2
func(ctypes.c_void_p(indata.ctypes.data), ctypes.c_void_p(outdata.ctypes.data),n,m,f_id)

print 'indata: %s' % indata

print 'outdata: %s' % outdata[0][0]


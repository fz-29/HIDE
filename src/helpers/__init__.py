__author__ = 'Shubham Dokania'

import collection
import point
import test_functions


def get_best_point(points):
    best = sorted(points, key=lambda x:x.z)[0]
    return best

def get_best_point_PSODE(points1, points2):
    best1 = sorted(points1, key=lambda x:x.z)[0]
    best2 = sorted(points2, key=lambda x:x.z)[0]
    if best1.z < best2.z :
        return best1
    else:
    	return best2
    	
if __name__ == '__main__':
    pass


#!/usr/bin/env python3
#encoding=utf-8

import bezier
import numpy as np
import spline_util

nodes = np.asfortranarray([
    [882.0, 863.0, 907.0],
    [803.0, -2.0, -2.0],
])
curve = bezier.Curve(nodes, degree=2)
#print(curve.evaluate(0.5))

point1 = np.asfortranarray([
     [882.0],
     [803.0],
])
point2 = np.asfortranarray([
     [907.0],
     [-2.0],
])
#print(point2[0])
print(curve.locate(point1))
print(curve.locate(point2))
#print(curve)

distance = spline_util.get_distance(point1[0],point1[1],point2[0],point2[1])
round_offset = 33
round_offset_rate = round_offset / distance

print('distance:',distance)
print('round_offset:',round_offset)
print('round_offset_rate:',round_offset_rate)

print(curve.evaluate(round_offset_rate))

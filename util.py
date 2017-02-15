import math


def distance(point_one,ponit_two):
	x,y=point_one
	xx,yy=ponit_two
	return math.sqrt(math.pow((x-xx),2)+math.pow((y-yy),2))

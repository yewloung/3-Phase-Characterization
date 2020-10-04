'''
This class consists of 14 functions to calculate complete 9 sets of line-to-neutral [L1N, L2N, L3N] and
line-to-line [L12, L23, L31, L21, L32, L13] voltages & phases by setting up any combination of 3 sets of
voltages & phases comprising 1 line-to-neutral & 2 line-to-line as inputs, to derive the other 6 sets of voltages &
phases

Developed by: Liew Yew Loung
Revision: V1.0                                                                                          Date: May 2020
------------------------------------------------------------------------------------------------------------------------
List of 4 degree to radian, radian to degree conversion functions:
------------------------------------------------------------------------------------------------------------------------
any_degree_to_half_angle_radians(degree), return radian --> get any range of degree input return radian value from -Pi to +Pi
any_radians_to_half_angle_degree(radian), return degree --> get any range of radian input return degree value from -180 to +180
any_degree_to_half_degree(degree), return degree --> get any range of degree input return degree value from -180 to +180
any_radians_to_half_radians(radian), return radian --> get any range of  radian input return radian value from -Pi to +Pi

e.g:
Degree = 950 --> 950 - 360 - 360 = 230 = -130 --> Radian = -130 * Pi / 180 = -2.268928028 (manual calculation)
By using, any_degree_to_half_angle_radians(950), return -2.268928028
Degree value can be integer, float, positive or negative value
'''

import numpy as np
import cmath

def any_degree_to_half_angle_radians(degree):
    ''' Convert degree within -360 to 360 '''
    if degree > 360:
        Quotient = degree // 360
        degree = degree - (Quotient * 360)
    elif degree < -360:
        Quotient = abs(degree // 360)
        degree = degree + (Quotient * 360)
    elif degree == 360 or degree == -360:
        degree = 0

    ''' Convert degree within -180 to 180 '''
    if degree > 180 and degree < 360:
        degree = degree - 360
    elif degree < -180 and degree > -360:
        degree = 360 + degree

    radian = np.radians(degree)
    return radian


def any_radians_to_half_angle_degree(radian):
    ''' Convert degree within -360 to 360 '''
    if radian > (2 * cmath.pi):
        Quotient = radian // (2 * cmath.pi)
        radian = radian - (Quotient * (2 * cmath.pi))
    elif radian < (-2 * cmath.pi):
        Quotient = abs(radian // (2 * cmath.pi))
        radian = radian + (Quotient * (2 * cmath.pi))
    elif radian == (2 * cmath.pi) or radian == (-2 * cmath.pi):
        radian = 0

    ''' Convert degree within -180 to 180 '''
    if radian > (cmath.pi) and radian < (2 * cmath.pi):
        radian = radian - (2 * cmath.pi)
    elif radian < (- cmath.pi) and radian > (-2 * cmath.pi):
        radian = (2 * cmath.pi) + radian

    degree = np.degrees(radian)
    return degree


def any_degree_to_half_degree(degree):
    ''' Convert degree within -360 to 360 '''
    if degree > 360:
        Quotient = degree // 360
        degree = degree - (Quotient * 360)
    elif degree < -360:
        Quotient = abs(degree // 360)
        degree = degree + (Quotient * 360)
    elif degree == 360 or degree == -360:
        degree = 0

    ''' Convert degree within -180 to 180 '''
    if degree > 180 and degree < 360:
        degree = degree - 360
    elif degree < -180 and degree > -360:
        degree = 360 + degree

    return degree


def any_radians_to_half_radians(radian):
    ''' Convert degree within -360 to 360 '''
    if radian > (2 * cmath.pi):
        Quotient = radian // (2 * cmath.pi)
        radian = radian - (Quotient * (2 * cmath.pi))
    elif radian < (-2 * cmath.pi):
        Quotient = abs(radian // (2 * cmath.pi))
        radian = radian + (Quotient * (2 * cmath.pi))
    elif radian == (2 * cmath.pi) or radian == (-2 * cmath.pi):
        radian = 0

    ''' Convert degree within -180 to 180 '''
    if radian > (cmath.pi) and radian < (2 * cmath.pi):
        radian = radian - (2 * cmath.pi)
    elif radian < (- cmath.pi) and radian > (-2 * cmath.pi):
        radian = (2 * cmath.pi) + radian

    return radian
'''
This class consists of 14 functions to calculate complete 9 sets of line-to-neutral [L1N, L2N, L3N] and
line-to-line [L12, L23, L31, L21, L32, L13] voltages & phases by setting up any combination of 3 sets of
voltages & phases comprising 1 line-to-neutral & 2 line-to-line as inputs, to derive the other 6 sets of voltages &
phases

Developed by: Liew Yew Loung
Revision: V1.0                                                                                          Date: May 2020
------------------------------------------------------------------------------------------------------------------------
List of 3 phases calculation methods:
------------------------------------------------------------------------------------------------------------------------

calc_result_givenby_L1N_L2N_L3N()     --> get L1N, L2N, L3N as inputs, calculate L12, L23, L31, L21, L32, L13
calc_result_givenby_L21_L31_L1N()     --> get L21, L31, L1N as inputs, calculate L12, L23, L3N, L2N, L32, L13
calc_result_givenby_L21_L13_L1N()     --> get L21, L13, L1N as inputs, calculate L12, L23, L3N, L2N, L32, L31
calc_result_givenby_L12_L31_L1N()     --> get L12, L31, L1N as inputs, calculate L21, L23, L3N, L2N, L32, L13
calc_result_givenby_L12_L13_L1N()     --> get L12, L13, L1N as inputs, calculate L21, L23, L3N, L2N, L32, L31
calc_result_givenby_L12_L32_L2N()     --> get L12, L2N, L32 as inputs, calculate L1N, L23, L31, L21, L3N, L13
calc_result_givenby_L12_L23_L2N()     --> get L12, L2N, L23 as inputs, calculate L1N, L32, L31, L21, L3N, L13
calc_result_givenby_L21_L32_L2N()     --> get L21, L2N, L32 as inputs, calculate L1N, L23, L31, L12, L3N, L13
calc_result_givenby_L21_L23_L2N()     --> get L21, L2N, L23 as inputs, calculate L1N, L32, L31, L12, L3N, L13
calc_result_givenby_L13_L23_L3N()     --> get L13, L23, L3N as inputs, calculate L12, L2N, L31, L21, L32, L1N
calc_result_givenby_L13_L32_L3N()     --> get L13, L32, L3N as inputs, calculate L12, L2N, L31, L21, L23, L1N
calc_result_givenby_L31_L23_L3N()     --> get L31, L23, L3N as inputs, calculate L12, L2N, L13, L21, L32, L1N
calc_result_givenby_L31_L32_L3N()     --> get L31, L32, L3N as inputs, calculate L12, L2N, L13, L21, L23, L1N
get_polar_plot()                      --> get phasor diagram
get_waveform_plot()                   --> get waveform

************************************************************************************************************************
User Guide:
************************************************************************************************************************
<Step 1>:
Create instant of class with parameters initialization as per example below, angle MUST BE in Degree
e.g: If the intended calculation is by taking L1N, L2N, L3N as inputs, Calc_Mode=L1N_L2N_L3N and
<L1N_Voltage>, <L1N_Angle_In_Degree>, <L2N_Voltage>, <L2N_Angle_In_Degree>, <L3N_Voltage>, <L3N_Angle_In_Degree>
MUST BE provided, the rest is optional / left as None. Final calculation result of all other voltages and phases will
be put to the respective class properties

<class_instance> = ThreePhaseCalcEngine(Calc_Mode=<Calculation_Type>,
                                        Magnitude_L1N=<L1N_Voltage>, Phase_L1N=<L1N_Angle_In_Degree>,
                                        Magnitude_L2N=<L2N_Voltage>, Phase_L2N=<L1N_Angle_In_Degree>,
                                        Magnitude_L3N=<L3N_Voltage>, Phase_L3N=<L1N_Angle_In_Degree>,
                                        Magnitude_L12=<L12_Voltage>, Phase_L12=<L1N_Angle_In_Degree>,
                                        Magnitude_L23=<L23_Voltage>, Phase_L23=<L1N_Angle_In_Degree>,
                                        Magnitude_L31=<L31_Voltage>, Phase_L31=<L1N_Angle_In_Degree>,
                                        Magnitude_L21=<L21_Voltage>, Phase_L21=<L1N_Angle_In_Degree>,
                                        Magnitude_L32=<L32_Voltage>, Phase_L32=<L1N_Angle_In_Degree>,
                                        Magnitude_L13=<L13_Voltage>, Phase_L13=<L1N_Angle_In_Degree>)

<Calculation_Type> is ENUM values range from:
L1N_L2N_L3N
L21_L31_L1N
L21_L13_L1N
L12_L31_L1N
L12_L13_L1N
L12_L32_L2N
L12_L23_L2N
L21_L32_L2N
L21_L23_L2N
L13_L23_L3N
L13_L32_L3N
L31_L23_L3N
L31_L32_L3N

<Step 2>:
Execute methods to perform calculation depends on the Calc_Mode=<Calculation_Type> initialized,
For <Calculation_Type> = L1N_L2N_L3N    --> <class_instance>.calc_result_givenby_L1N_L2N_L3N()
For <Calculation_Type> = L21_L31_L1N    --> <class_instance>.calc_result_givenby_L21_L31_L1N()
...

<Step 3>:
Get the result of calculation from the property of the class as follow,
To get the calculated value of L1N Voltage          --> <class_instance>.Magnitude_L1N
To get the calculated value of L1N Angle in Radian  --> <class_instance>.Phase_L1N
...

'''

from AngleConversion import *
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


class ThreePhaseCalcEngine:

    def __init__(self, Calc_Mode,
                 Magnitude_L1N=None, Phase_L1N=None,
                 Magnitude_L2N=None, Phase_L2N=None,
                 Magnitude_L3N=None, Phase_L3N=None,
                 Magnitude_L12=None, Phase_L12=None,
                 Magnitude_L23=None, Phase_L23=None,
                 Magnitude_L31=None, Phase_L31=None,
                 Magnitude_L21=None, Phase_L21=None,
                 Magnitude_L32=None, Phase_L32=None,
                 Magnitude_L13=None, Phase_L13=None):

        # Instance Variable / properties
        try:
            self.Calc_Mode = Calc_Mode
            self.Magnitude_L1N = Magnitude_L1N
            self.Phase_L1N = Phase_L1N
            self.Magnitude_L2N = Magnitude_L2N
            self.Phase_L2N = Phase_L2N
            self.Magnitude_L3N = Magnitude_L3N
            self.Phase_L3N = Phase_L3N

            self.Magnitude_L12 = Magnitude_L12
            self.Phase_L12 = Phase_L12
            self.Magnitude_L23 = Magnitude_L23
            self.Phase_L23 = Phase_L23
            self.Magnitude_L31 = Magnitude_L31
            self.Phase_L31 = Phase_L31

            self.Magnitude_L21 = Magnitude_L21
            self.Phase_L21 = Phase_L21
            self.Magnitude_L32 = Magnitude_L32
            self.Phase_L32 = Phase_L32
            self.Magnitude_L13 = Magnitude_L13
            self.Phase_L13 = Phase_L13
        except:
            pass
            #print('>>> Calculation is done unsuccessfully due to missing or invalid input parameters value...')


    def calc_result_givenby_L1N_L2N_L3N(self) -> None:
        '''
        L12 = L1N - L2N
        L23 = L2N - L3N
        L31 = L3N - L1N
        L21 = L2N - L1N
        L32 = L3N - L2N
        L13 = L1N - L3N
        L1N = L1N
        L2N = L2N
        L3N = L3N
        '''

        if self.Calc_Mode != 'L1N_L2N_L3N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L1N, L2N, get L12 --> L12 = L1N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L2N,
                                                                                     self.Phase_L2N)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L23 --> L23 = L2N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L3N,
                                                                                     self.Phase_L3N)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        ''' With known L3N, L1N, get L31 --> L31 = L3N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L2N, L1N, get L21 --> L21 = L2N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L3N, L2N, get L32 --> L32 = L3N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        ''' With known L1N, L3N, get L13 --> L13 = L1N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        self.Magnitude_L1N = self.Magnitude_L1N
        self.Phase_L1N = self.Phase_L1N
        self.Magnitude_L2N = self.Magnitude_L2N
        self.Phase_L2N = self.Phase_L2N
        self.Magnitude_L3N = self.Magnitude_L3N
        self.Phase_L3N = self.Phase_L3N

    def calc_result_givenby_L21_L31_L1N(self) -> None:
        '''
        L23 = L21 - L31
        L32 = L31 - L21
        L3N = L31 + L1N
        L2N = L21 + L1N
        L12 = L1N - L2N = -L21
        L13 = L1N - L3N = -L31
        L21 = L21
        L31 = L31
        L1N = L1N
        '''

        if self.Calc_Mode != 'L21_L31_L1N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L21, L31, get L23 --> L23 = L21 - L31 '''
        rect_operation = cmath.rect(self.Magnitude_L21, self.Phase_L21) - cmath.rect(self.Magnitude_L31,
                                                                                     self.Phase_L31)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        ''' With known L21, L31, get L32 --> L32 = L31 - L21 '''
        rect_operation = cmath.rect(self.Magnitude_L31, self.Phase_L31) - cmath.rect(self.Magnitude_L21,
                                                                                     self.Phase_L21)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        ''' With known L31, L1N, get L3N --> L3N = L31 + L1N '''
        rect_operation = cmath.rect(self.Magnitude_L31, self.Phase_L31) + cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L21, L1N, get L2N --> L2N = L21 + L1N '''
        rect_operation = cmath.rect(self.Magnitude_L21, self.Phase_L21) + cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L1N, L2N, get L12 --> L12 = L1N - L2N = -L21'''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        #rect_operation = - cmath.rect(self.Magnitude_L21, self.Phase_L21)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L1N, L3N, get L13 --> L13 = L1N - L3N = -L31'''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        #rect_operation = - cmath.rect(self.Magnitude_L31, self.Phase_L31)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        self.Magnitude_L21 = self.Magnitude_L21
        self.Phase_L21 = self.Phase_L21
        self.Magnitude_L31 = self.Magnitude_L31
        self.Phase_L31 = self.Phase_L31
        self.Magnitude_L1N = self.Magnitude_L1N
        self.Phase_L1N = self.Phase_L1N

        print("calculated")


    def calc_result_givenby_L21_L13_L1N(self) -> None:
        '''
        L23 = L21 + L13
        L32 = - L13 - L21
        L3N = L1N - L13
        L2N = L21 + L1N
        L12 = L1N - L2N
        L31 = L3N - L1N
        L21 = L21
        L13 = L13
        L1N = L1N
        '''

        if self.Calc_Mode != 'L21_L13_L1N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L21, L13, get L23 --> L23 = L21 + L13 '''
        rect_operation = cmath.rect(self.Magnitude_L21, self.Phase_L21) + cmath.rect(self.Magnitude_L13,
                                                                                     self.Phase_L13)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        ''' With known L13, L21, get L32 --> L32 = - L13 - L21 '''
        rect_operation = - cmath.rect(self.Magnitude_L13, self.Phase_L13) - cmath.rect(self.Magnitude_L21,
                                                                                       self.Phase_L21)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        ''' With known L1N, L13, get L3N --> L3N = L1N - L13 '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L13, self.Phase_L13)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L21, L1N, get L2N --> L2N = L21 + L1N '''
        rect_operation = cmath.rect(self.Magnitude_L21, self.Phase_L21) + cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L1N, L2N, get L12 --> L12 = L1N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L3N, L1N, get L31 --> L31 = L3N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        self.Magnitude_L21 = self.Magnitude_L21
        self.Phase_L21 = self.Phase_L21
        self.Magnitude_L13 = self.Magnitude_L13
        self.Phase_L13 = self.Phase_L13
        self.Magnitude_L1N = self.Magnitude_L1N
        self.Phase_L1N = self.Phase_L1N


    def calc_result_givenby_L12_L31_L1N(self) -> None:
        '''
        L23 = - L12 - L31
        L32 = L31 + L12
        L3N = L31 + L1N
        L2N = L1N - L12
        L21 = L2N - L1N
        L13 = L1N - L3N
        L12 = L12
        L31 = L31
        L1N = L1N
        '''

        if self.Calc_Mode != 'L12_L31_L1N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L12, L31, get L23 --> L23 = - L12 - L31 '''
        rect_operation = - cmath.rect(self.Magnitude_L12, self.Phase_L12) - cmath.rect(self.Magnitude_L31,
                                                                                       self.Phase_L31)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        ''' With known L31, L12, get L32 --> L32 = L31 + L12 '''
        rect_operation = cmath.rect(self.Magnitude_L31, self.Phase_L31) + cmath.rect(self.Magnitude_L12,
                                                                                     self.Phase_L12)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        ''' With known L31, L1N, get L3N --> L3N = L31 + L1N '''
        rect_operation = cmath.rect(self.Magnitude_L31, self.Phase_L31) + cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L1N, L12, get L2N --> L2N = L1N - L12 '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L12, self.Phase_L12)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L2N, L1N, get L21 --> L21 = L2N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L1N, L3N, get L13 --> L13 = L1N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        self.Magnitude_L12 = self.Magnitude_L12
        self.Phase_L12 = self.Phase_L12
        self.Magnitude_L31 = self.Magnitude_L31
        self.Phase_L31 = self.Phase_L31
        self.Magnitude_L1N = self.Magnitude_L1N
        self.Phase_L1N = self.Phase_L1N


    def calc_result_givenby_L12_L13_L1N(self) -> None:
        '''
        L23 = - L12 + L13
        L32 = - L13 + L12
        L3N = L1N - L13
        L2N = L1N - L12
        L21 = L2N - L1N
        L31 = L3N - L1N
        L12 = L12
        L13 = L13
        L1N = L1N
        '''

        if self.Calc_Mode != 'L12_L13_L1N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L12, L13, get L23 --> L23 = - L12 + L13 '''
        rect_operation = - cmath.rect(self.Magnitude_L12, self.Phase_L12) + cmath.rect(self.Magnitude_L13,
                                                                                       self.Phase_L13)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        ''' With known L13, L12, get L32 --> L32 = - L13 + L12 '''
        rect_operation = - cmath.rect(self.Magnitude_L13, self.Phase_L13) + cmath.rect(self.Magnitude_L12,
                                                                                       self.Phase_L12)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        ''' With known L1N, L13, get L3N --> L3N = L1N - L13 '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L13, self.Phase_L13)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L1N, L12, get L2N --> L2N = L1N - L12 '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L12, self.Phase_L12)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L2N, L1N, get L21 --> L21 = L2N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L3N, L1N, get L31 --> L31 = L3N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        self.Magnitude_L12 = self.Magnitude_L12
        self.Phase_L12 = self.Phase_L12
        self.Magnitude_L13 = self.Magnitude_L13
        self.Phase_L13 = self.Phase_L13
        self.Magnitude_L1N = self.Magnitude_L1N
        self.Phase_L1N = self.Phase_L1N


    def calc_result_givenby_L12_L32_L2N(self) -> None:
        '''
        L13 = L12 - L32
        L31 = L32 - L12
        L3N = L32 + L2N
        L1N = L12 + L2N
        L23 = L2N - L3N
        L21 = L2N - L1N
        L12 = L12
        L32 = L32
        L2N = L2N
        '''

        if self.Calc_Mode != 'L12_L32_L2N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L12, L32, get L13 --> L13 = L12 - L32 '''
        rect_operation = cmath.rect(self.Magnitude_L12, self.Phase_L12) - cmath.rect(self.Magnitude_L32,
                                                                                     self.Phase_L32)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        ''' With known L32, L12, get L31 --> L31 = L32 - L12 '''
        rect_operation = cmath.rect(self.Magnitude_L32, self.Phase_L32) - cmath.rect(self.Magnitude_L12,
                                                                                     self.Phase_L12)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L32, L2N, get L3N --> L3N = L32 + L2N '''
        rect_operation = cmath.rect(self.Magnitude_L32, self.Phase_L32) + cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L12, L2N, get L1N --> L1N = L12 + L2N '''
        rect_operation = cmath.rect(self.Magnitude_L12, self.Phase_L12) + cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L21 --> L21 = L2N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L23 --> L23 = L2N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        self.Magnitude_L12 = self.Magnitude_L12
        self.Phase_L12 = self.Phase_L12
        self.Magnitude_L32 = self.Magnitude_L32
        self.Phase_L32 = self.Phase_L32
        self.Magnitude_L2N = self.Magnitude_L2N
        self.Phase_L2N = self.Phase_L2N


    def calc_result_givenby_L12_L23_L2N(self) -> None:
        '''
        L13 = L12 + L23
        L31 = - L23 - L12
        L3N = L2N - L23
        L1N = L12 + L2N
        L21 = L2N - L1N
        L32 = L3N - L2N
        L12 = L12
        L23 = L23
        L2N = L2N
        '''

        if self.Calc_Mode != 'L12_L23_L2N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L12, L23, get L13 --> L13 = L12 + L23 '''
        rect_operation = cmath.rect(self.Magnitude_L12, self.Phase_L12) + cmath.rect(self.Magnitude_L23,
                                                                                     self.Phase_L23)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        ''' With known L23, L12, get L31 --> L31 = - L23 - L12 '''
        rect_operation = - cmath.rect(self.Magnitude_L23, self.Phase_L23) - cmath.rect(self.Magnitude_L12,
                                                                                       self.Phase_L12)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L2N, L23, get L3N --> L3N = L2N - L23 '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L23, self.Phase_L23)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L12, L2N, get L1N --> L1N = L12 + L2N '''
        rect_operation = cmath.rect(self.Magnitude_L12, self.Phase_L12) + cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L21 --> L21 = L2N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L3N, L2N, get L32 --> L32 = L3N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        self.Magnitude_L12 = self.Magnitude_L12
        self.Phase_L12 = self.Phase_L12
        self.Magnitude_L23 = self.Magnitude_L23
        self.Phase_L23 = self.Phase_L23
        self.Magnitude_L2N = self.Magnitude_L2N
        self.Phase_L2N = self.Phase_L2N


    def calc_result_givenby_L21_L32_L2N(self) -> None:
        '''
        L13 = - L21 - L32
        L31 = L32 + L21
        L3N = L32 + L2N
        L1N = L2N - L21
        L23 = L2N - L3N
        L12 = L1N - L2N
        L21 = L21
        L32 = L32
        L2N = L2N
        '''

        if self.Calc_Mode != 'L21_L32_L2N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L21, L32, get L13 --> L13 = - L21 - L32 '''
        rect_operation = - cmath.rect(self.Magnitude_L21, self.Phase_L21) - cmath.rect(self.Magnitude_L32,
                                                                                       self.Phase_L32)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        ''' With known L32, L21, get L31 --> L31 = L32 + L21 '''
        rect_operation = cmath.rect(self.Magnitude_L32, self.Phase_L32) + cmath.rect(self.Magnitude_L21,
                                                                                     self.Phase_L21)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L32, L2N, get L3N --> L3N = L32 + L2N '''
        rect_operation = cmath.rect(self.Magnitude_L32, self.Phase_L32) + cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L2N, L21, get L1N --> L1N = L2N - L21 '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L21, self.Phase_L21)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L12 --> L23 = L2N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        ''' With known L1N, L2N, get L32 --> L12 = L1N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        self.Magnitude_L21 = self.Magnitude_L21
        self.Phase_L21 = self.Phase_L21
        self.Magnitude_L32 = self.Magnitude_L32
        self.Phase_L32 = self.Phase_L32
        self.Magnitude_L2N = self.Magnitude_L2N
        self.Phase_L2N = self.Phase_L2N


    def calc_result_givenby_L21_L23_L2N(self) -> None:
        '''
        L13 = - L21 + L23
        L31 = - L23 + L21
        L3N = L2N - L23
        L1N = L2N - L21
        L12 = L1N - L2N
        L32 = L3N - L2N
        L21 = L21
        L23 = L23
        L2N = L2N
        '''

        if self.Calc_Mode != 'L21_L23_L2N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L21, L23, get L13 --> L13 = - L21 + L23 '''
        rect_operation = - cmath.rect(self.Magnitude_L21, self.Phase_L21) + cmath.rect(self.Magnitude_L23,
                                                                                       self.Phase_L23)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        ''' With known L23, L21, get L31 --> L31 = - L23 + L21 '''
        rect_operation = - cmath.rect(self.Magnitude_L23, self.Phase_L23) + cmath.rect(self.Magnitude_L21,
                                                                                       self.Phase_L21)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L2N, L23, get L3N --> L3N = L2N - L23 '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L23, self.Phase_L23)
        self.Magnitude_L3N = abs(rect_operation)
        self.Phase_L3N = cmath.phase(rect_operation)

        ''' With known L2N, L21, get L1N --> L1N = L2N - L21 '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L21, self.Phase_L21)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L1N, L2N, get L12 --> L12 = L1N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L3N, L2N, get L32 --> L32 = L3N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        self.Magnitude_L21 = self.Magnitude_L21
        self.Phase_L21 = self.Phase_L21
        self.Magnitude_L23 = self.Magnitude_L23
        self.Phase_L23 = self.Phase_L23
        self.Magnitude_L2N = self.Magnitude_L2N
        self.Phase_L2N = self.Phase_L2N


    def calc_result_givenby_L13_L23_L3N(self) -> None:
        '''
        L12 = L13 - L23
        L21 = L23 - L13
        L2N = L23 + L3N
        L1N = L13 + L3N
        L31 = L3N - L1N
        L32 = L3N - L2N
        L13 = L13
        L23 = L23
        L3N = L3N
        '''

        if self.Calc_Mode != 'L13_L23_L3N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L13, L23, get L12 --> L12 = L13 - L23 '''
        rect_operation = cmath.rect(self.Magnitude_L13, self.Phase_L13) - cmath.rect(self.Magnitude_L23,
                                                                                     self.Phase_L23)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L23, L13, get L21 --> L21 = L23 - L13 '''
        rect_operation = cmath.rect(self.Magnitude_L23, self.Phase_L23) - cmath.rect(self.Magnitude_L13,
                                                                                     self.Phase_L13)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L23, L3N, get L2N --> L2N = L23 + L3N '''
        rect_operation = cmath.rect(self.Magnitude_L23, self.Phase_L23) + cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L13, L3N, get L1N --> L1N = L13 + L3N '''
        rect_operation = cmath.rect(self.Magnitude_L13, self.Phase_L13) + cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L3N, L1N, get L13 --> L31 = L3N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L3N, L2N, get L23 --> L32 = L3N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        self.Magnitude_L13 = self.Magnitude_L13
        self.Phase_L13 = self.Phase_L13
        self.Magnitude_L23 = self.Magnitude_L23
        self.Phase_L23 = self.Phase_L23
        self.Magnitude_L3N = self.Magnitude_L3N
        self.Phase_L3N = self.Phase_L3N


    def calc_result_givenby_L13_L32_L3N(self) -> None:
        '''
        L12 = L13 + L32
        L21 = - L32 - L13
        L2N = L3N - L32
        L1N = L13 + L3N
        L31 = L3N - L1N
        L23 = L2N - L3N
        L13 = L13
        L32 = L32
        L3N = L3N
        '''

        if self.Calc_Mode != 'L13_L32_L3N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L13, L32, get L12 --> L12 = L13 + L32 '''
        rect_operation = cmath.rect(self.Magnitude_L13, self.Phase_L13) + cmath.rect(self.Magnitude_L32,
                                                                                     self.Phase_L32)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L32, L13, get L21 --> L21 = - L32 - L13 '''
        rect_operation = - cmath.rect(self.Magnitude_L32, self.Phase_L32) - cmath.rect(self.Magnitude_L13,
                                                                                       self.Phase_L13)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L3N, L32, get L2N --> L2N = L3N - L32 '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L32, self.Phase_L32)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L13, L3N, get L1N --> L1N = L13 + L3N '''
        rect_operation = cmath.rect(self.Magnitude_L13, self.Phase_L13) + cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L3N, L1N, get L13 --> L31 = L3N - L1N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L1N, self.Phase_L1N)
        self.Magnitude_L31 = abs(rect_operation)
        self.Phase_L31 = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L23 --> L23 = L2N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        self.Magnitude_L13 = self.Magnitude_L13
        self.Phase_L13 = self.Phase_L13
        self.Magnitude_L32 = self.Magnitude_L32
        self.Phase_L32 = self.Phase_L32
        self.Magnitude_L3N = self.Magnitude_L3N
        self.Phase_L3N = self.Phase_L3N


    def calc_result_givenby_L31_L23_L3N(self) -> None:
        '''
        L12 = - L31 - L23
        L21 = L23 + L31
        L2N = L23 + L3N
        L1N = L3N - L31
        L13 = L1N - L3N
        L32 = L3N - L2N
        L31 = L31
        L23 = L23
        L3N = L3N
        '''

        if self.Calc_Mode != 'L31_L23_L3N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L31, L23, get L12 --> L12 = - L31 - L23 '''
        rect_operation = - cmath.rect(self.Magnitude_L31, self.Phase_L31) - cmath.rect(self.Magnitude_L23,
                                                                                       self.Phase_L23)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L23, L31, get L21 --> L21 = L23 + L31 '''
        rect_operation = cmath.rect(self.Magnitude_L23, self.Phase_L23) + cmath.rect(self.Magnitude_L31,
                                                                                     self.Phase_L31)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L23, L3N, get L2N --> L2N = L23 + L3N '''
        rect_operation = cmath.rect(self.Magnitude_L23, self.Phase_L23) + cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L3N, L31, get L1N --> L1N = L3N - L31 '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L31, self.Phase_L31)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L1N, L3N, get L13 --> L13 = L1N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        ''' With known L3N, L2N, get L32 = L3N - L2N '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L2N, self.Phase_L2N)
        self.Magnitude_L32 = abs(rect_operation)
        self.Phase_L32 = cmath.phase(rect_operation)

        self.Magnitude_L31 = self.Magnitude_L31
        self.Phase_L31 = self.Phase_L31
        self.Magnitude_L32 = self.Magnitude_L32
        self.Phase_L23 = self.Phase_L23
        self.Magnitude_L3N = self.Magnitude_L3N
        self.Phase_L3N = self.Phase_L3N


    def calc_result_givenby_L31_L32_L3N(self) -> None:
        '''
        L12 = L32 - L31
        L21 = - L32 + L31
        L2N = L3N - L32
        L1N = L3N - L31
        L13 = L1N - L3N
        L23 = L2N - L3N
        L31 = L31
        L32 = L32
        L3N = L3N
        '''

        if self.Calc_Mode != 'L31_L32_L3N':
            print('>>> No calculation performed due to error!')
            return None

        ''' With known L32, L31, get L12 --> L12 = L32 - L31 '''
        rect_operation = cmath.rect(self.Magnitude_L32, self.Phase_L32) - cmath.rect(self.Magnitude_L31,
                                                                                     self.Phase_L31)
        self.Magnitude_L12 = abs(rect_operation)
        self.Phase_L12 = cmath.phase(rect_operation)

        ''' With known L32, L31, get L21 --> L21 = - L32 + L31 '''
        rect_operation = - cmath.rect(self.Magnitude_L32, self.Phase_L32) + cmath.rect(self.Magnitude_L31,
                                                                                       self.Phase_L31)
        self.Magnitude_L21 = abs(rect_operation)
        self.Phase_L21 = cmath.phase(rect_operation)

        ''' With known L3N, L32, get L2N --> L2N = L3N - L32 '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L32, self.Phase_L32)
        self.Magnitude_L2N = abs(rect_operation)
        self.Phase_L2N = cmath.phase(rect_operation)

        ''' With known L3N, L31, get L1N --> L1N = L3N - L31 '''
        rect_operation = cmath.rect(self.Magnitude_L3N, self.Phase_L3N) - cmath.rect(self.Magnitude_L31, self.Phase_L31)
        self.Magnitude_L1N = abs(rect_operation)
        self.Phase_L1N = cmath.phase(rect_operation)

        ''' With known L1N, L3N, get L13 --> L13 = L1N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L1N, self.Phase_L1N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L13 = abs(rect_operation)
        self.Phase_L13 = cmath.phase(rect_operation)

        ''' With known L2N, L3N, get L23 --> L23 = L2N - L3N '''
        rect_operation = cmath.rect(self.Magnitude_L2N, self.Phase_L2N) - cmath.rect(self.Magnitude_L3N, self.Phase_L3N)
        self.Magnitude_L23 = abs(rect_operation)
        self.Phase_L23 = cmath.phase(rect_operation)

        self.Magnitude_L31 = self.Magnitude_L31
        self.Phase_L31 = self.Phase_L31
        self.Magnitude_L32 = self.Magnitude_L32
        self.Phase_L32 = self.Phase_L32
        self.Magnitude_L3N = self.Magnitude_L3N
        self.Phase_L3N = self.Phase_L3N


    def get_polar_plot(self) -> None:
        plt.close()

        ''' Check if the plot windows is closed or not '''
        def handle_close(evt):
            plt.close()
            print('>>> Phasor diagram is closed')

        ''' Dictionary to be used by Quiver vector plot'''
        pl_L1N = {'dx': np.cos(self.Phase_L1N),
                  'dy': np.sin(self.Phase_L1N),
                  'r': self.Magnitude_L1N}
        pl_L2N = {'dx': np.cos(self.Phase_L2N),
                  'dy': np.sin(self.Phase_L2N),
                  'r': self.Magnitude_L2N}
        pl_L3N = {'dx': np.cos(self.Phase_L3N),
                  'dy': np.sin(self.Phase_L3N),
                  'r': self.Magnitude_L3N}
        pl_L12 = {'dx': np.cos(self.Phase_L12),
                  'dy': np.sin(self.Phase_L12),
                  'r': self.Magnitude_L12}
        pl_L23 = {'dx': np.cos(self.Phase_L23),
                  'dy': np.sin(self.Phase_L23),
                  'r': self.Magnitude_L23}
        pl_L31 = {'dx': np.cos(self.Phase_L31),
                  'dy': np.sin(self.Phase_L31),
                  'r': self.Magnitude_L31}
        pl_L21 = {'dx': np.cos(self.Phase_L21),
                  'dy': np.sin(self.Phase_L21),
                  'r': self.Magnitude_L21}
        pl_L32 = {'dx': np.cos(self.Phase_L32),
                  'dy': np.sin(self.Phase_L32),
                  'r': self.Magnitude_L32}
        pl_L13 = {'dx': np.cos(self.Phase_L13),
                  'dy': np.sin(self.Phase_L13),
                  'r': self.Magnitude_L13}

        max_magnitude = max(pl_L1N['r'], pl_L2N['r'], pl_L3N['r'],
                            pl_L12['r'], pl_L23['r'], pl_L31['r'],
                            pl_L21['r'], pl_L32['r'], pl_L13['r'])

        ''' Prepare dynamic plot variable to ease plot changes '''
        Normalized_Value = max_magnitude
        No_Of_Magnitude_Mark_Scale = 5

        Min_Magnitude_Scale = 0
        Max_Magnitude_Scale = 1

        Norm_Min_Mag_Scale = Min_Magnitude_Scale * Normalized_Value
        Norm_Max_Mag_Scale = Max_Magnitude_Scale * Normalized_Value

        Scalelist = []
        Scalestep = (Norm_Max_Mag_Scale - Norm_Min_Mag_Scale) / No_Of_Magnitude_Mark_Scale
        for i in range(0, No_Of_Magnitude_Mark_Scale):
            n = round((i + 1) * Scalestep, 1)
            Scalelist.append(n)

        ''' Prepare window plot properties '''
        #plt.ioff()
        fig = plt.figure('3 Phases System - Phasor Diagram', figsize=(8, 5))
        fig.canvas.mpl_connect('close_event', handle_close)
        gs = gridspec.GridSpec(ncols=10, nrows=10, left=0, bottom=0, right=0.95, top=0.94, wspace=0.0, hspace=0.0)

        polar1 = fig.add_subplot(gs[0:8, 0:8], projection='polar')
        polar1.set_rmax(Max_Magnitude_Scale)  # configure maximum radial scale
        polar1.set_rlim(Min_Magnitude_Scale, Max_Magnitude_Scale)
        polar1.set_rticks(Scalelist)  # configure radial scale
        polar1.grid(color='lightgrey', linestyle='dotted', linewidth=0.5)
        polar1.set_thetagrids([0, 15, 30, 45, 60, 75, 90,
                               105, 120, 135, 150, 165, 180,
                               195, 210, 225, 240, 255, 270,
                               285, 300, 315, 330, 345])
        polar1.plot(0, 0, color='#228B22', marker='o', markersize=10)

        ''' Define arrow vector coordinate for the tail '''
        x_pos = [0] * 9
        y_pos = [0] * 9

        ''' Prepare list of arrow vector length start extended from the tail '''
        x_direct = [pl_L1N['dx'], pl_L2N['dx'], pl_L3N['dx'],
                    pl_L12['dx'], pl_L23['dx'], pl_L31['dx'],
                    pl_L21['dx'], pl_L32['dx'], pl_L13['dx']]
        for i in range(len(x_direct)):
            x_direct[i] = round(x_direct[i], 3)

        y_direct = [pl_L1N['dy'], pl_L2N['dy'], pl_L3N['dy'],
                    pl_L12['dy'], pl_L23['dy'], pl_L31['dy'],
                    pl_L21['dy'], pl_L32['dy'], pl_L13['dy']]
        for i in range(len(y_direct)):
            y_direct[i] = round(y_direct[i], 3)

        r_direct = [pl_L1N['r'], pl_L2N['r'], pl_L3N['r'],
                    pl_L12['r'], pl_L23['r'], pl_L31['r'],
                    pl_L21['r'], pl_L32['r'], pl_L13['r']]
        for i in range(len(r_direct)):
            if r_direct[i] == 0:
                r_direct[i] = round((Normalized_Value) / 0.00001, 2)
            else:
                r_direct[i] = round((Normalized_Value) / r_direct[i], 2)


        quiver_scale = ((Norm_Max_Mag_Scale - Norm_Min_Mag_Scale) / (Normalized_Value)) * 2

        vL1N = polar1.quiver(x_pos[0], y_pos[0], x_direct[0], y_direct[0], scale=quiver_scale * r_direct[0],
                             scale_units='width', color='#FF0000', headwidth=2, headlength=3, headaxislength=3)
        vL2N = polar1.quiver(x_pos[1], y_pos[1], x_direct[1], y_direct[1], scale=quiver_scale * r_direct[1],
                             scale_units='width', color='#FFFF00', headwidth=2, headlength=3, headaxislength=3)
        vL3N = polar1.quiver(x_pos[2], y_pos[2], x_direct[2], y_direct[2], scale=quiver_scale * r_direct[2],
                             scale_units='width', color='#0000FF', headwidth=2, headlength=3, headaxislength=3)
        vL12 = polar1.quiver(x_pos[3], y_pos[3], x_direct[3], y_direct[3], scale=quiver_scale * r_direct[3],
                             scale_units='width', color='#9C661F', headwidth=2, headlength=3, headaxislength=3)
        vL23 = polar1.quiver(x_pos[4], y_pos[4], x_direct[4], y_direct[4], scale=quiver_scale * r_direct[4],
                             scale_units='width', color='#000000', headwidth=2, headlength=3, headaxislength=3)
        vL31 = polar1.quiver(x_pos[5], y_pos[5], x_direct[5], y_direct[5], scale=quiver_scale * r_direct[5],
                             scale_units='width', color='#808080', headwidth=2, headlength=3, headaxislength=3)
        vL21 = polar1.quiver(x_pos[6], y_pos[6], x_direct[6], y_direct[6], scale=quiver_scale * r_direct[6],
                             scale_units='width', color='#00FF00', headwidth=2, headlength=3, headaxislength=3)
        vL32 = polar1.quiver(x_pos[7], y_pos[7], x_direct[7], y_direct[7], scale=quiver_scale * r_direct[7],
                             scale_units='width', color='#FF69B4', headwidth=2, headlength=3, headaxislength=3)
        vL13 = polar1.quiver(x_pos[8], y_pos[8], x_direct[8], y_direct[8], scale=quiver_scale * r_direct[8],
                             scale_units='width', color='#ADD8E6', headwidth=2, headlength=3, headaxislength=3)

        vL1N_label = 'L1N=' + str(round(self.Magnitude_L1N, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L1N), 1)) + '\u00b0'
        polar1.quiverkey(vL1N, X=1.3, Y=1, U=0.3, label=vL1N_label, labelpos='E', fontproperties={'size': 'small'})

        vL2N_label = 'L2N=' + str(round(self.Magnitude_L2N, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L2N), 1)) + '\u00b0'
        polar1.quiverkey(vL2N, X=1.3, Y=0.95, U=0.3, label=vL2N_label, labelpos='E', fontproperties={'size': 'small'})

        vL3N_label = 'L3N=' + str(round(self.Magnitude_L3N, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L3N), 1)) + '\u00b0'
        polar1.quiverkey(vL3N, X=1.3, Y=0.90, U=0.3, label=vL3N_label, labelpos='E', fontproperties={'size': 'small'})


        vL21_label = 'L21=' + str(round(self.Magnitude_L21, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L21), 1)) + '\u00b0'
        polar1.quiverkey(vL21, X=1.3, Y=0.80, U=0.3, label=vL21_label, labelpos='E', fontproperties={'size': 'small'})

        vL31_label = 'L31=' + str(round(self.Magnitude_L31, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L31), 1)) + '\u00b0'
        polar1.quiverkey(vL31, X=1.3, Y=0.75, U=0.3, label=vL31_label, labelpos='E', fontproperties={'size': 'small'})

        vL32_label = 'L32=' + str(round(self.Magnitude_L32, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L32), 1)) + '\u00b0'
        polar1.quiverkey(vL32, X=1.3, Y=0.70, U=0.3, label=vL32_label, labelpos='E', fontproperties={'size': 'small'})


        vL13_label = 'L13=' + str(round(self.Magnitude_L31, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L13), 1)) + '\u00b0'
        polar1.quiverkey(vL13, X=1.3, Y=0.60, U=0.3, label=vL13_label, labelpos='E', fontproperties={'size': 'small'})

        vL23_label = 'L23=' + str(round(self.Magnitude_L23, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L23), 1)) + '\u00b0'
        polar1.quiverkey(vL23, X=1.3, Y=0.55, U=0.3, label=vL23_label, labelpos='E', fontproperties={'size': 'small'})

        vL12_label = 'L12=' + str(round(self.Magnitude_L12, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L12), 1)) + '\u00b0'
        polar1.quiverkey(vL12, X=1.3, Y=0.50, U=0.3, label=vL12_label, labelpos='E', fontproperties={'size': 'small'})

        print('>>> Norm_Min_Mag_Scale=', Norm_Min_Mag_Scale)
        print('>>> Norm_Max_Mag_Scale=', Norm_Max_Mag_Scale)
        print('>>> quiver_scale=', quiver_scale)
        print('>>> x_direct: ', x_direct)
        print('>>> y_direct: ', y_direct)
        print('>>> r_direct: ', r_direct)

        plt.show(block=False)


    def get_waveform_plot(self) -> None:
        plt.close()

        ''' Check if the plot windows is closed or not '''
        def handle_close(evt):
            plt.close()
            print('>>> Waveform is closed')

        ''' Prepare waveform variables used by formula '''
        StartPlot = 0
        NoOfCycle = 1.5
        NoOfData = 100
        EndPlot = NoOfCycle * 360
        PlotInterval = (EndPlot - StartPlot) / NoOfData

        ''' Waveform formula '''
        # t = np.arange(StartPlot, EndPlot, PlotInterval)
        t = np.linspace(StartPlot, EndPlot, NoOfData)

        wf_L1N = self.Magnitude_L1N * np.sin(np.radians(t) + self.Phase_L1N)
        wf_L2N = self.Magnitude_L2N * np.sin(np.radians(t) + self.Phase_L2N)
        wf_L3N = self.Magnitude_L3N * np.sin(np.radians(t) + self.Phase_L3N)
        wf_L12 = self.Magnitude_L12 * np.sin(np.radians(t) + self.Phase_L12)
        wf_L23 = self.Magnitude_L23 * np.sin(np.radians(t) + self.Phase_L23)
        wf_L31 = self.Magnitude_L31 * np.sin(np.radians(t) + self.Phase_L31)
        wf_L21 = self.Magnitude_L21 * np.sin(np.radians(t) + self.Phase_L21)
        wf_L32 = self.Magnitude_L32 * np.sin(np.radians(t) + self.Phase_L32)
        wf_L13 = self.Magnitude_L13 * np.sin(np.radians(t) + self.Phase_L13)

        ''' Prepare plot properties '''
        fig = plt.figure('3 Phase Waveform', figsize=(12, 6))
        fig.canvas.mpl_connect('close_event', handle_close)
        gs = gridspec.GridSpec(ncols=12, nrows=12, left=0.07, bottom=0.05, right=0.9, top=0.95, wspace=0.0, hspace=10)

        LN = fig.add_subplot(gs[0:6, 0:6])
        LL1 = fig.add_subplot(gs[0:6, 6:12])
        LL2 = fig.add_subplot(gs[6:12, 0:6])
        LL3 = fig.add_subplot(gs[6:12, 6:12])

        #LN = fig.add_subplot(gs[0:6, 0:5])
        #LL1 = fig.add_subplot(gs[0:6, 7:12])
        #LL2 = fig.add_subplot(gs[6:12, 0:5])
        #LL3 = fig.add_subplot(gs[6:12, 7:12])

        ''' Line to Neutral plot '''
        vL1N_label = 'L1N=' + str(round(self.Magnitude_L1N, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L1N), 1)) + '\u00b0'

        vL2N_label = 'L2N=' + str(round(self.Magnitude_L2N, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L2N), 1)) + '\u00b0'

        vL3N_label = 'L3N=' + str(round(self.Magnitude_L3N, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L3N), 1)) + '\u00b0'

        LN.grid(color='lightgrey', linestyle='dotted', linewidth=0.5)
        LN.plot(t, wf_L1N, color='red', label=vL1N_label)
        LN.plot(t, wf_L2N, color='yellow', label=vL2N_label)
        LN.plot(t, wf_L3N, color='blue', label=vL3N_label)
        LN.legend(ncol=3, bbox_to_anchor=(0, 1), loc='lower left', borderaxespad=0, fontsize='x-small')

        ''' Line to Line plot '''
        vL31_label = 'L31=' + str(round(self.Magnitude_L31, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L31), 1)) + '\u00b0'

        vL21_label = 'L21=' + str(round(self.Magnitude_L21, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L21), 1)) + '\u00b0'

        vL32_label = 'L32=' + str(round(self.Magnitude_L32, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L32), 1)) + '\u00b0'

        LL1.grid(color='lightgrey', linestyle='dotted', linewidth=0.5)
        LL1.plot(t, wf_L31, color='red', label=vL31_label)
        LL1.plot(t, wf_L21, color='yellow', label=vL21_label)
        LL1.plot(t, wf_L32, color='blue', label=vL32_label)
        LL1.set_yticklabels([])
        LL1.legend(ncol=3, bbox_to_anchor=(0, 1), loc='lower left', borderaxespad=0, fontsize='x-small')

        ''' Line to Line plot '''
        vL13_label = 'L13=' + str(round(self.Magnitude_L13, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L13), 1)) + '\u00b0'

        vL23_label = 'L23=' + str(round(self.Magnitude_L23, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L23), 1)) + '\u00b0'

        vL12_label = 'L12=' + str(round(self.Magnitude_L12, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L12), 1)) + '\u00b0'

        LL2.grid(color='lightgrey', linestyle='dotted', linewidth=0.5)
        LL2.plot(t, wf_L13, color='red', label=vL13_label)
        LL2.plot(t, wf_L23, color='yellow', label=vL23_label)
        LL2.plot(t, wf_L12, color='blue', label=vL12_label)
        LL2.legend(ncol=3, bbox_to_anchor=(0, 1), loc='lower left', borderaxespad=0, fontsize='x-small')

        ''' Line to Line plot '''
        vL12_label = 'L12=' + str(round(self.Magnitude_L12, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L12), 1)) + '\u00b0'

        vL32_label = 'L32=' + str(round(self.Magnitude_L32, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L32), 1)) + '\u00b0'

        vL13_label = 'L13=' + str(round(self.Magnitude_L13, 2)) + 'V' + ', ' \
                     + '\u03B8 =' + str(round(any_radians_to_half_angle_degree(self.Phase_L13), 1)) + '\u00b0'

        LL3.grid(color='lightgrey', linestyle='dotted', linewidth=0.5)
        LL3.plot(t, wf_L12, color='red', label=vL12_label)
        LL3.plot(t, wf_L32, color='yellow', label=vL32_label)
        LL3.plot(t, wf_L13, color='blue', label=vL13_label)
        LL3.set_yticklabels([])
        LL3.legend(ncol=3, bbox_to_anchor=(0, 1), loc='lower left', borderaxespad=0, fontsize='x-small')

        plt.show(block=False)





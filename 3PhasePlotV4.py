from AngleConversion import *
from ThreePhaseCalculation import ThreePhaseCalcEngine
from PySimpleGUI_Property_Template import *
import os
import sys
from datetime import datetime
import numpy as np
import pandas as pd
import time
import PySimpleGUI as sg


sg.ChangeLookAndFeel('Black')

''' Create windows base GUI object '''
''' a_button.grid(row=0, column=1, padx=10, pady=10) '''
class Gui:
    def __init__(self):
        col1 = sg.Column(
            [
            # Input parameters frame
            [sg.Frame('Select 3 Known Parameters For Complete 3 Phase Parameters Set Calculation ',
                      [
                        [sg.Checkbox('L1N', key='-SL1N-', size=(3, 1),
                                    default=True, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L2N', key='-SL2N-', size=(3, 1),
                                    default=True, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L3N', key='-SL3N-', size=(3, 1),
                                    default=True, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L12', key='-SL12-', size=(3, 1),
                                    default=False, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L23', key='-SL23-', size=(3, 1),
                                    default=False, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L31', key='-SL31-', size=(3, 1),
                                    default=False, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L21', key='-SL21-', size=(3, 1),
                                    default=False, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L32', key='-SL32-', size=(3, 1),
                                    default=False, enable_events=True, font=('Helvetica', 8)),
                        sg.Checkbox('L13', key='-SL13-', size=(4, 1),
                                    default=False, enable_events=True, font=('Helvetica', 8))],
                       ],
                      relief="groove", key='-FInputChoice-', size=(200, 1), font=('Helvetica', 8))],
            ],
            pad=(0, 0))

        col1_2 = sg.Column(
            [
                # Output
                [sg.Text('', size=(2, 1)),
                 sg.Text('Un(LN)', size=(5, 1)),
                 sg.InputText('220', size=(13, 1), key='Un_SRefLN', text_color='Black',
                              background_color='White',
                              disabled=False, tooltip='Un value used for calculating %UV, %OV, %ASY',
                              enable_events=True)],
                [sg.Text('', size=(2, 1)),
                 sg.Text('Un(LL)', size=(5, 1)),
                 sg.InputText('380', size=(13, 1), key='Un_SRefLL', text_color='Black',
                              background_color='White',
                              disabled=False, tooltip='Un value used for calculating %UV, %OV, %ASY',
                              enable_events=True)]

            ],
            pad=(0, 0))

        col2 = sg.Column(
            [
                # Reference phase frame
                [sg.Frame('Select Reference Phase',
                          [
                            [sg.Radio('L1N', group_id='RefPhase', key='-RL1N-', size=(3, 1),
                                     default=True, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L2N', group_id='RefPhase', key='-RL2N-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L3N', group_id='RefPhase', key='-RL3N-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L12', group_id='RefPhase', key='-RL12-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L23', group_id='RefPhase', key='-RL23-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L31', group_id='RefPhase', key='-RL31-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L21', group_id='RefPhase', key='-RL21-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L32', group_id='RefPhase', key='-RL32-', size=(3, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8)),
                            sg.Radio('L13', group_id='RefPhase', key='-RL13-', size=(4, 1),
                                     default=False, enable_events=True, font=('Helvetica', 8))]
                           ],
                          relief="groove", key='-FPhaseChoice-', font=('Helvetica', 8))],
            ],
            pad=(0, 0))

        col3 = sg.Column(
            [
                # Result frame
                [sg.Frame('Known Input Parameters & 3 Phase Parameters Calculation Result',
                          [
                            [col1, col1_2],
                            [col2],
                            [sg.Text('L1N, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                     tooltip='L1 to neutral voltage & phase angle...'),
                            sg.InputText('277.0', size=(13, 1), key='L1N', text_color='Black', background_color='White',
                                         disabled=False, tooltip='L1 to neutral voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('0.0', size=(8, 1), key='AL1N', text_color='Black', background_color='White',
                                         disabled=False, tooltip='L1 to neutral voltage phase angle (Normal = 0)...',
                                         enable_events=True),
                            sg.Text('', size=(2, 1)),
                            sg.Text('L2N, \u03B8'+ '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L2 to neutral voltage & phase angle...'),
                            sg.InputText('277.0', size=(13, 1), key='L2N', text_color='Black', background_color='White',
                                         disabled=False, tooltip='L2 to neutral voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('-120.0', size=(8, 1), key='AL2N', text_color='Black', background_color='White',
                                         disabled=False, tooltip='L2 to neutral voltage phase angle (Normal = -120 '
                                                                 '--> Chroma P1_2 Setting = 120)...',
                                         enable_events=True),
                            sg.Text('', size=(2, 1)),
                            sg.Text('L3N, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L3 to neutral voltage & phase angle...'),
                            sg.InputText('277.0', size=(13, 1), key='L3N', text_color='Black', background_color='White',
                                         disabled=False, tooltip='L3 to neutral voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('120.0', size=(8, 1), key='AL3N', text_color='Black', background_color='White',
                                         disabled=False, tooltip='L3 to neutral voltage phase angle (Normal = 120 '
                                                                 '--> Chroma P1_3 Setting = 240)...',
                                         enable_events=True)],
                           [sg.Text('L12, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L1 to L2 voltage & phase angle...'),
                            sg.InputText('479.78', size=(13, 1), key='L12', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L1 to L2 voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('30.0', size=(8, 1), key='AL12', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L1 to L2 voltage phase angle...',
                                         enable_events=True),
                            sg.Text('', size=(2, 1)),
                            sg.Text('L23, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L2 to L3 voltage & phase angle...'),
                            sg.InputText('479.78', size=(13, 1), key='L23', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L2 to L3 voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('-90.0', size=(8, 1), key='AL23', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L2 to L3 voltage phase angle...',
                                         enable_events=True),
                            sg.Text('', size=(2, 1)),
                            sg.Text('L31, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L3 to L1 voltage & phase angle...'),
                            sg.InputText('479.78', size=(13, 1), key='L31', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L3 to L1 voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('150.0', size=(8, 1), key='AL31', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L3 to L1 voltage phase angle...',
                                         enable_events=True)],
                           [sg.Text('L21, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L2 to L1 voltage & phase angle...'),
                            sg.InputText('479.78', size=(13, 1), key='L21', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L2 to L1 voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('-150.0', size=(8, 1), key='AL21', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L2 to L1 voltage phase angle...',
                                         enable_events=True),
                            sg.Text('', size=(2, 1)),
                            sg.Text('L32, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L3 to L2 voltage & phase angle...'),
                            sg.InputText('479.78', size=(13, 1), key='L32', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L3 to L2 voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('90.0', size=(8, 1), key='AL32', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L3 to L2 voltage phase angle...',
                                         enable_events=True),
                            sg.Text('', size=(2, 1)),
                            sg.Text('L13, \u03B8' + '\u00b0', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='L1 to L3 voltage & phase angle...'),
                            sg.InputText('479.78', size=(13, 1), key='L13', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L1 to L3 voltage magnitude...',
                                         enable_events=True),
                            sg.InputText('-30.0', size=(8, 1), key='AL13', text_color='Black', background_color='White',
                                         disabled=True, tooltip='L1 to L3 voltage phase angle...',
                                         enable_events=True)],
                           #[sg.Text('', size=(1, 1))],
                           [sg.Button('Calculate & Add Record', size=(18, 1), key='_CALCULATE_',
                                      button_color=('white', 'green'),
                                      font=('Helvetica', 10)),
                            sg.Button('Delete Last Record', size=(14, 1), key='_DELETE RECORD_',
                                      button_color=('white', 'blue'),
                                      font=('Helvetica', 10)),
                            sg.Button('Show Record', size=(10, 1), key='_SHOW RECORD_',
                                      button_color=('white', 'blue'),
                                      font=('Helvetica', 10)),
                            sg.Button('Phasor Diagram [Last Record]', size=(22, 1), key='_SHOW PHASOR_',
                                      button_color=('black', 'yellow'),
                                      font=('Helvetica', 10),
                                      disabled=True),
                            sg.Button('Waveform [Last Record]', size=(20, 1), key='_SHOW WAVEFORM_',
                                      button_color=('black', 'yellow'),
                                      font=('Helvetica', 10),
                                      disabled=True)]
                           ],
                          relief="groove")],
            ],
            pad=(0, 0))

        col4 = sg.Column(
            [
                # OK / Cancel
                [sg.Ok(size=(12, 1), key='_OK BUTTON_', button_color=('white', 'blue'), font=('Helvetica', 10)),
                 sg.Cancel(size=(11, 1), key='_CANCEL BUTTON_', font=('Helvetica', 10))]
            ],
            pad=(0, 0))

        col5 = sg.Column(
            [
                # Output
                [sg.Output(size=(122, 17), key='OUTPUT', font=('Helvetica', 8))]
            ],
            pad=(0, 0))

        col6 = sg.Column(
            [
                # Generate Data of Specific Condition
                [sg.Frame('Generate Data of Specific Condition',
                          [
                            [sg.Radio('Known L31, L21, L1N', group_id='GenData', key='L31_L21_L1N',
                                     size=(19, 1), default=True),
                            sg.Radio('Known L13, L23, L3N', group_id='GenData', key='L13_L23_L3N',
                                     size=(19, 1), default=False),
                            sg.Radio('Known L12, L32, L2N', group_id='GenData', key='L12_L32_L2N',
                                     size=(19, 1), default=False)],
                           [sg.Text('', size=(8, 1)),
                            sg.Text('LL Voltage, V', size=(10, 1), auto_size_text=False, justification='left',
                                    tooltip='Line to Line Voltage value', font=('Helvetica', 10)),
                            sg.Text('LN Voltage, V', size=(11, 1), auto_size_text=False, justification='left',
                                    tooltip='Line to Neutral Voltage value', font=('Helvetica', 10)),
                            sg.Text('Phase Angle, \u00b0', size=(13, 1), auto_size_text=False, justification='left',
                                    tooltip='Phase Angle in Degree', font=('Helvetica', 10)),
                            #sg.Text('', size=(1, 1)),
                            sg.Text('Un(LN)', size=(9, 1)),
                            sg.InputText('220', size=(13, 1), key='Un_GRefLN', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Un value used for calculating %UV, %OV, %ASY',
                                         enable_events=True),
                            sg.Text('Un(LL)', size=(5, 1)),
                            sg.InputText('380', size=(14, 1), key='Un_GRefLL', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Un value used for calculating %UV, %OV, %ASY',
                                         enable_events=True)],
                           [sg.Text('Start Value', size=(8, 1)),
                            sg.InputText('110', size=(12, 1), key='LL_Start', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Start line to line voltage of data interation...',
                                         enable_events=True),
                            sg.InputText('50', size=(12, 1), key='LN_Start', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Start line to neutral voltage of data interation...',
                                         enable_events=True),
                            sg.InputText('0', size=(12, 1), key='PH_Start', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Start phase angle of data interation...',
                                         enable_events=True),
                            sg.Text('', size=(1, 1)),
                            sg.Text('Step Voltage', size=(9, 1)),
                            sg.InputText('100', size=(5, 1), key='V_Step', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Step voltage of data interation',
                                         enable_events=True),
                            sg.Text('', size=(12, 1)),
                            sg.Button('Generate Data', size=(12, 1), key='_GEN_DATA_',
                                      button_color=('white', 'green'),
                                      font=('Helvetica', 10),
                                      disabled=False)],
                           [sg.Text('Stop Value', size=(8, 1)),
                            sg.InputText('650', size=(12, 1), key='LL_Stop', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Stop line to line voltage of data interation...',
                                         enable_events=True),
                            sg.InputText('400', size=(12, 1), key='LN_Stop', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Stop line to neutral voltage of data interation...',
                                         enable_events=True),
                            sg.InputText('360', size=(12, 1), key='PH_Stop', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Stop phase angle of data interation...',
                                         enable_events=True),
                            sg.Text('', size=(1, 1)),
                            sg.Text('Step Phase', size=(9, 1)),
                            sg.InputText('60', size=(5, 1), key='PH_Step', text_color='Black',
                                         background_color='White',
                                         disabled=False, tooltip='Step phase angle of data interation',
                                         enable_events=True),
                            sg.Text('', size=(12, 1)),
                            sg.Button('Clear Data', size=(12, 1), key='_CLEAR_DATA_',
                                      button_color=('white', 'blue'),
                                      font=('Helvetica', 10),
                                      disabled=False)],
                           ],
                          relief="groove")],
            ],
            pad=(0, 0))

        col7 = sg.Column(
            [
                # Generate Data of Specific Condition
                [sg.Frame('Save Record To .xlsx File',
                          [
                            [sg.Text('Filename', size=(7, 1), auto_size_text=False, justification='left',
                                    tooltip='Intended filename...'),
                            sg.InputText(default_filename, size=(20, 1), key='FILENAME',
                                         text_color='White', disabled=False,
                                         tooltip='Intended filename...'),
                            sg.Text('Folder', size=(5, 1), auto_size_text=False, justification='left',
                                    tooltip='Target folder to store the saved file...'),
                            sg.InputText(default_save_path, size=(45, 1), key='DESTINATION_FOLDER_PATH',
                                         text_color='Black', disabled=True,
                                         tooltip='Target folder to store the saved file...'),
                            sg.FolderBrowse('Browse', size=(7, 1), key='_BROWSE_DESTINATION_FOLDER_',
                                            target='DESTINATION_FOLDER_PATH'),
                            sg.Button('Save', size=(7, 1), key='_SAVE RECORD_', font=('Helvetica', 10))]
                          ],
                          relief="groove")],
            ],
            pad=(0, 0))

        #col8 = sg.TabGroup(
        #    [
        #        [sg.Tab('Output Result', [[sg.Output(size=(105, 10))]],
        #                key='TOutput'),
        #         sg.Tab('Phasor Diagram', [[sg.Text('Sample text 2')], [sg.Canvas(key='-CVPhasor-')]],
        #                key='TPhasor'),
        #         sg.Tab('Waveform', [[sg.Text('Sample text 3')], [sg.Canvas(key='-CVWaveform-')]],
        #                key='TWaveform')],
        #    ],
        #    key='TGroup', pad=(0, 0), enable_events=True)

        #self.layout = [[col1], [col2], [col3], [col6], [col7], [col5]]
        #self.layout = [[col3], [col6], [col7], [col8]]
        self.layout = [[col3], [col6], [col7], [col5]]

        self.window: object = sg.Window(
            'Three Phase System Characteristics Modeling',
            self.layout,
            auto_size_text=True,
            element_justification='left', location=(0, 0))

# Reference_Phase_Conversion
def Convert_Ref_Phase(NewRefPhase, windows, values):
    if values['AL1N'] == '' or values['AL2N'] == '' or values['AL3N'] == '' or \
            values['AL12'] == '' or values['AL23'] == '' or values['AL31'] == '' or \
            values['AL21'] == '' or values['AL32'] == '' or values['AL12'] == '':
        print('>>> Calculation is not executed due to invalid / empty phase angle field value...')
        print('\n')
        return 0
    else:
        if NewRefPhase >= 0:
            DeltaAngle = - NewRefPhase
        elif NewRefPhase < 0:
            DeltaAngle = - NewRefPhase

        windows['AL1N'].update(round(any_degree_to_half_degree(float(values['AL1N']) + DeltaAngle), 2))
        windows['AL2N'].update(round(any_degree_to_half_degree(float(values['AL2N']) + DeltaAngle), 2))
        windows['AL3N'].update(round(any_degree_to_half_degree(float(values['AL3N']) + DeltaAngle), 2))
        windows['AL12'].update(round(any_degree_to_half_degree(float(values['AL12']) + DeltaAngle), 2))
        windows['AL23'].update(round(any_degree_to_half_degree(float(values['AL23']) + DeltaAngle), 2))
        windows['AL31'].update(round(any_degree_to_half_degree(float(values['AL31']) + DeltaAngle), 2))
        windows['AL21'].update(round(any_degree_to_half_degree(float(values['AL21']) + DeltaAngle), 2))
        windows['AL32'].update(round(any_degree_to_half_degree(float(values['AL32']) + DeltaAngle), 2))
        windows['AL13'].update(round(any_degree_to_half_degree(float(values['AL13']) + DeltaAngle), 2))


# Decode Selection
def Decode_Selection(no_of_sel, selection, windows, instant_sel_value, concat_sel_value):
    choice = {6: 'L1N_L2N_L3N',
              131: 'L21_L31_L1N',
              401: 'L21_L13_L1N',
              41: 'L12_L31_L1N',
              311: 'L12_L13_L1N',
              212: 'L12_L32_L2N',
              32: 'L12_L23_L2N',
              302: 'L21_L32_L2N',
              122: 'L21_L23_L2N',
              323: 'L13_L23_L3N',
              503: 'L13_L32_L3N',
              53: 'L31_L23_L3N',
              233: 'L31_L32_L3N'}
    try:
        # ['L1N', 'L2N', 'L3N', 'L12', 'L23', 'L31', 'L21', 'L32', 'L13']
        # ['AL1N', 'AL2N', 'AL3N', 'AL12', 'AL23', 'AL31', 'AL21', 'AL32', 'AL13']
        if no_of_sel == 0:
            Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L3N', 'L12', 'L23', 'L31', 'L21', 'L32', 'L13'])
            Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL3N', 'AL12', 'AL23', 'AL31', 'AL21', 'AL32', 'AL13'])
        elif no_of_sel == 1:
            if 'L1N' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L23', 'L32'])
                Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L3N', 'L21', 'L12', 'L13', 'L31'])
                Disable_Text_Related_Element(windows, ['AL23', 'AL32'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL3N', 'AL21', 'AL12', 'AL13', 'AL31'])
            elif 'L2N' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L13', 'L31'])
                Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L3N', 'L21', 'L12', 'L23', 'L32'])
                Disable_Text_Related_Element(windows, ['AL13', 'AL31'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL3N', 'AL21', 'AL12', 'AL23', 'AL32'])
            elif 'L3N' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L12', 'L21'])
                Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L3N', 'L31', 'L13', 'L23', 'L32'])
                Disable_Text_Related_Element(windows, ['AL12', 'AL21'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL3N', 'AL31', 'AL13', 'AL23', 'AL32'])
            elif 'L12' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L3N', 'L21'])
                Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L31', 'L13', 'L23', 'L32'])
                Disable_Text_Related_Element(windows, ['AL3N', 'AL21'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL31', 'AL13', 'AL23', 'AL32'])
            elif 'L23' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L1N', 'L32'])
                Enable_Text_Related_Element(windows, ['L13', 'L2N', 'L3N', 'L21', 'L12', 'L23', 'L31'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL32'])
                Enable_Text_Related_Element(windows, ['AL13', 'AL2N', 'AL3N', 'AL21', 'AL12', 'AL23', 'AL31'])
            elif 'L31' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L2N', 'L13'])
                Enable_Text_Related_Element(windows, ['L1N', 'L12', 'L3N', 'L31', 'L21', 'L23', 'L32'])
                Disable_Text_Related_Element(windows, ['AL2N', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL12', 'AL3N', 'AL31', 'AL21', 'AL23', 'AL32'])
            elif 'L21' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L3N', 'L12'])
                Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L21', 'L31', 'L13', 'L23', 'L32'])
                Disable_Text_Related_Element(windows, ['AL3N', 'AL12'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL21', 'AL31', 'AL13', 'AL23', 'AL32'])
            elif 'L32' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L1N', 'L23'])
                Enable_Text_Related_Element(windows, ['L13', 'L2N', 'L3N', 'L21', 'L12', 'L32', 'L31'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL23'])
                Enable_Text_Related_Element(windows, ['AL13', 'AL2N', 'AL3N', 'AL21', 'AL12', 'AL32', 'AL31'])
            elif 'L13' in instant_sel_value:
                Disable_Text_Related_Element(windows, ['L2N', 'L31'])
                Enable_Text_Related_Element(windows, ['L1N', 'L12', 'L3N', 'L13', 'L21', 'L23', 'L32'])
                Disable_Text_Related_Element(windows, ['AL2N', 'AL31'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL12', 'AL3N', 'AL13', 'AL21', 'AL23', 'AL32'])
        elif no_of_sel == 2:
            pass
        elif no_of_sel == 3:
            # ['L1N', 'L2N', 'L3N', 'L12', 'L23', 'L31', 'L21', 'L32', 'L13']
            if selection == 6:  # L1N_L2N_L3N
                Disable_Text_Related_Element(windows, ['L12', 'L23', 'L31', 'L21', 'L32', 'L13'])
                Enable_Text_Related_Element(windows, ['L1N', 'L2N', 'L3N'])
                Disable_Text_Related_Element(windows, ['AL12', 'AL23', 'AL31', 'AL21', 'AL32', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL3N'])
                #Empty_Text_Related_Element(windows, ['L12', 'L23', 'L31', 'L21', 'L32', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL12', 'AL23', 'AL31', 'AL21', 'AL32', 'AL13'])
            elif selection == 131:  # L21_L31_L1N
                Disable_Text_Related_Element(windows, ['L2N', 'L3N', 'L12', 'L23', 'L32', 'L13'])
                Enable_Text_Related_Element(windows, ['L1N', 'L31', 'L21'])
                Disable_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL12', 'AL23', 'AL32', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL31', 'AL21'])
                #Empty_Text_Related_Element(windows, ['L2N', 'L3N', 'L12', 'L23', 'L32', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL12', 'AL23', 'AL32', 'AL13'])
            elif selection == 401:  # L21_L13_L1N
                Disable_Text_Related_Element(windows, ['L2N', 'L3N', 'L12', 'L23', 'L31', 'L32'])
                Enable_Text_Related_Element(windows, ['L1N', 'L21', 'L13'])
                Disable_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL12', 'AL23', 'AL31', 'AL32'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL21', 'AL13'])
                #Empty_Text_Related_Element(windows, ['L2N', 'L3N', 'L12', 'L23', 'L31', 'L32'])
                #Empty_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL12', 'AL23', 'AL31', 'AL32'])
            elif selection == 41:  # L12_L31_L1N
                Disable_Text_Related_Element(windows, ['L2N', 'L3N', 'L23', 'L21', 'L32', 'L13'])
                Enable_Text_Related_Element(windows, ['L1N', 'L12', 'L31'])
                Disable_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL23', 'AL21', 'AL32', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL12', 'AL31'])
                #Empty_Text_Related_Element(windows, ['L2N', 'L3N', 'L23', 'L21', 'L32', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL23', 'AL21', 'AL32', 'AL13'])
            elif selection == 311:  # L12_L13_L1N
                Disable_Text_Related_Element(windows, ['L2N', 'L3N', 'L23', 'L31', 'L21', 'L32'])
                Enable_Text_Related_Element(windows, ['L1N', 'L12', 'L13'])
                Disable_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL23', 'AL31', 'AL21', 'AL32'])
                Enable_Text_Related_Element(windows, ['AL1N', 'AL12', 'AL13'])
                #Empty_Text_Related_Element(windows, ['L2N', 'L3N', 'L23', 'L31', 'L21', 'L32'])
                #Empty_Text_Related_Element(windows, ['AL2N', 'AL3N', 'AL23', 'AL31', 'AL21', 'AL32'])
            elif selection == 212:  # L12_L32_L2N
                Disable_Text_Related_Element(windows, ['L1N', 'L3N', 'L23', 'L31', 'L21', 'L13'])
                Enable_Text_Related_Element(windows, ['L2N', 'L12', 'L32'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL23', 'AL31', 'AL21', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL2N', 'AL12', 'AL32'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L3N', 'L23', 'L31', 'L21', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL23', 'AL31', 'AL21', 'AL13'])
            elif selection == 32:  # L12_L23_L2N
                Disable_Text_Related_Element(windows, ['L1N', 'L3N', 'L31', 'L21', 'L32', 'L13'])
                Enable_Text_Related_Element(windows, ['L2N', 'L12', 'L23'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL31', 'AL21', 'AL32', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL2N', 'AL12', 'AL23'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L3N', 'L31', 'L21', 'L32', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL31', 'AL21', 'AL32', 'AL13'])
            elif selection == 302:  # L21_L32_L2N
                Disable_Text_Related_Element(windows, ['L1N', 'L3N', 'L12', 'L23', 'L31', 'L13'])
                Enable_Text_Related_Element(windows, ['L2N', 'L21', 'L32'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL12', 'AL23', 'AL31', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL2N', 'AL21', 'AL32'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L3N', 'L12', 'L23', 'L31', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL12', 'AL23', 'AL31', 'AL13'])
            elif selection == 122:  # L21_L23_L2N
                Disable_Text_Related_Element(windows, ['L1N', 'L3N', 'L12', 'L31', 'L32', 'L13'])
                Enable_Text_Related_Element(windows, ['L2N', 'L23', 'L21'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL12', 'AL31', 'AL32', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL2N', 'AL23', 'AL21'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L3N', 'L12', 'L31', 'L32', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL3N', 'AL12', 'AL31', 'AL32', 'AL13'])
            elif selection == 323:  # L13_L23_L3N
                Disable_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L31', 'L21', 'L32'])
                Enable_Text_Related_Element(windows, ['L3N', 'L23', 'L13'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL31', 'AL21', 'AL32'])
                Enable_Text_Related_Element(windows, ['AL3N', 'AL23', 'AL13'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L31', 'L21', 'L32'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL31', 'AL21', 'AL32'])
            elif selection == 503:  # L13_L32_L3N
                Disable_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L23', 'L31', 'L21'])
                Enable_Text_Related_Element(windows, ['L3N', 'L32', 'L13'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL23', 'AL31', 'AL21'])
                Enable_Text_Related_Element(windows, ['AL3N', 'AL32', 'AL13'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L23', 'L31', 'L21'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL23', 'AL31', 'AL21'])
            elif selection == 53:  # L31_L23_L3N
                Disable_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L21', 'L32', 'L13'])
                Enable_Text_Related_Element(windows, ['L3N', 'L23', 'L31'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL21', 'AL32', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL3N', 'AL23', 'AL31'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L21', 'L32', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL21', 'AL32', 'AL13'])
            elif selection == 233:  # L31_L32_L3N
                Disable_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L23', 'L21', 'L13'])
                Enable_Text_Related_Element(windows, ['L3N', 'L31', 'L32'])
                Disable_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL23', 'AL21', 'AL13'])
                Enable_Text_Related_Element(windows, ['AL3N', 'AL31', 'AL32'])
                #Empty_Text_Related_Element(windows, ['L1N', 'L2N', 'L12', 'L23', 'L21', 'L13'])
                #Empty_Text_Related_Element(windows, ['AL1N', 'AL2N', 'AL12', 'AL23', 'AL21', 'AL13'])

        final_choice = choice[selection]

    except:
        final_choice = ''
    return final_choice


# Check Analysis Selection
def Check_Analysis_Selection(no_of_sel, selection, windows, instant_sel, instant_sel_value):
    calchoice = {'-SL1N-': 1, '-SL2N-': 2, '-SL3N-': 3,
                 '-SL12-': 10, '-SL23-': 20, '-SL31-': 30,
                 '-SL21-': 100, '-SL32-': 200, '-SL13-': 300}

    if no_of_sel == 3:
        if instant_sel_value == True:
            windows[instant_sel].update(False)
            final_selection = Decode_Selection(no_of_sel, selection, windows, instant_sel, 'Test')
            if final_selection == '':
                print(">>> Wrong combination of 3 input parameters, only these 13 combinations are valid.")
                print('>>> L1N_L2N_L3N')
                print('>>> L21_L31_L1N')
                print('>>> L21_L13_L1N')
                print('>>> L12_L31_L1N')
                print('>>> L12_L13_L1N')
                print('>>> L12_L32_L2N')
                print('>>> L12_L23_L2N')
                print('>>> L21_L32_L2N')
                print('>>> L21_L23_L2N')
                print('>>> L13_L23_L3N')
                print('>>> L13_L32_L3N')
                print('>>> L31_L23_L3N')
                print('>>> L31_L32_L3N')
                print('\n')
            else:
                print('>>> Reach maximum 3 input parameters selection, your next action is to either:')
                print('>>> (1) click < Calculate & Add Record > to run calculation OR ')
                print('>>> (2) reduce existing parameters selection to try other possible combination.')
                print('\n')
        else:
            no_of_sel = no_of_sel - 1
            selection = selection - calchoice[instant_sel]
            print('>>> Select 1 more input parameters...')
            print('\n')
    elif no_of_sel == 2:
        if instant_sel_value == True:
            no_of_sel = no_of_sel + 1
            selection = selection + calchoice[instant_sel]
            final_selection = Decode_Selection(no_of_sel, selection, windows, instant_sel, 'Test')
            if final_selection == '':
                print(">>> Wrong combination of 3 input parameters, only these 13 combinations are valid.")
                print('>>> L1N_L2N_L3N')
                print('>>> L21_L31_L1N')
                print('>>> L21_L13_L1N')
                print('>>> L12_L31_L1N')
                print('>>> L12_L13_L1N')
                print('>>> L12_L32_L2N')
                print('>>> L12_L23_L2N')
                print('>>> L21_L32_L2N')
                print('>>> L21_L23_L2N')
                print('>>> L13_L23_L3N')
                print('>>> L13_L32_L3N')
                print('>>> L31_L23_L3N')
                print('>>> L31_L32_L3N')
                print('\n')
            else:
                print('>>> Reach maximum 3 input parameters selection, your next action is to either:')
                print('>>> (1) click < Calculate & Add Record > to run calculation OR ')
                print('>>> (2) reduce existing parameters selection to try other possible combination.')
                print('\n')
        else:
            no_of_sel = no_of_sel - 1
            selection = selection - calchoice[instant_sel]
            print('>>> Continue to select 2 more input parameters ...')
            print('\n')
    elif no_of_sel == 1:
        if instant_sel_value == True:
            no_of_sel = no_of_sel + 1
            selection = selection + calchoice[instant_sel]
            print('>>> Continue to select 1 more input parameter ...')
            print('\n')
        else:
            no_of_sel = no_of_sel - 1
            selection = selection - calchoice[instant_sel]
            print('>>> Continue to select up to 3 input parameters ...')
            print('\n')
    elif no_of_sel == 0:
        if instant_sel_value == True:
            no_of_sel = no_of_sel + 1
            selection = selection + calchoice[instant_sel]
            print('>>> Continue to select 2 more input parameter ...')
            print('\n')

    final_selection = Decode_Selection(no_of_sel, selection, windows, instant_sel, 'Test')
    #final_selection = 0

    return no_of_sel, selection, final_selection


''' main loop of the program '''
def main():
    ''' create instant of window '''
    g = Gui()
    first_start_up = True

    ''' initialize the properties of the elements within the window '''
    sel_count = 3  # 3 inputs parameters selected
    selection = 6  # L1N, L2N, L3N input parameters are selected
    final_sel = 'L31_L21_L1N'

    round_up = lambda num: int(num + 1) if int(num) != num else int(num)

    ''' initialize empty dataframe to hold the full set of calculation result '''
    column_names = ['L1N', 'AL1N', 'L2N', 'AL2N', 'L3N', 'AL3N',
                    'L12', 'AL12', 'L23', 'AL23', 'L31', 'AL31',
                    'L21', 'AL21', 'L32', 'AL32', 'L13', 'AL13',
                    'Un_ref_LN', 'Un_ref_LL',
                    'LN_Min', 'LN_Max', 'LN_Asy',
                    'LN_%UV', 'LN_%OV', 'LN_%ASY',
                    'LL31_21_32_Min', 'LL31_21_32_Max', 'LL31_21_32_Asy',
                    'LL31_21_32_%UV', 'LL31_21_32_%OV', 'LL31_21_32_%ASY',
                    'LL13_23_12_Min', 'LL13_23_12_Max', 'LL13_23_12_Asy',
                    'LL13_23_12_%UV', 'LL13_23_12_%OV', 'LL13_23_12_%ASY',
                    'LL12_32_13_Min', 'LL12_32_13_Max', 'LL12_32_13_Asy',
                    'LL12_32_13_%UV', 'LL12_32_13_%OV', 'LL12_32_13_%ASY']

    pd.pandas.set_option('display.max_columns', None)  # All dataframe data will be printed without truncation
    df3P = pd.DataFrame(columns=column_names)
    df3P_Gen = pd.DataFrame(columns=column_names)

    #column_types = ['float', 'float', 'float', 'float', 'float', 'float',
    #                'float', 'float', 'float', 'float', 'float', 'float',
    #                'float', 'float', 'float', 'float', 'float', 'float',
    #                'float', 'float'
    #                'float', 'float', 'float',
    #                'float', 'float', 'float',
    #                'float', 'float', 'float',
    #                'float', 'float', 'float',
    #                'float', 'float', 'float',
    #                'float', 'float', 'float',
    #                'float', 'float', 'float',
    #                'float', 'float', 'float']
    #df3P = pd.DataFrame(columns=column_names, dtype=column_types)

    while True:
        event, values = g.window.read()

        ''' Keep updating all 3 phases parameters into variables '''
        try:
            L1N = float(values['L1N'])
            AL1N = float(values['AL1N'])
            L2N = float(values['L2N'])
            AL2N = float(values['AL2N'])
            L3N = float(values['L3N'])
            AL3N = float(values['AL3N'])
            L12 = float(values['L12'])
            AL12 = float(values['AL12'])
            L23 = float(values['L23'])
            AL23 = float(values['AL23'])
            L31 = float(values['L31'])
            AL31 = float(values['AL31'])
            L21 = float(values['L21'])
            AL21 = float(values['AL21'])
            L32 = float(values['L32'])
            AL32 = float(values['AL32'])
            L13 = float(values['L13'])
            AL13 = float(values['AL13'])
            Un_SRefLN = float(values['Un_SRefLN'])
            Un_SRefLL = float(values['Un_SRefLL'])

            LL_Start = float(values['LL_Start'])
            LN_Start = float(values['LN_Start'])
            PH_Start = float(values['PH_Start'])
            LL_Stop = float(values['LL_Stop'])
            LN_Stop = float(values['LN_Stop'])
            PH_Stop = float(values['PH_Stop'])
            V_Step = float(values['V_Step'])
            PH_Step = float(values['PH_Step'])
            Un_GRefLN = float(values['Un_GRefLN'])
            Un_GRefLL = float(values['Un_GRefLL'])

        except:
            print('>>> Check your input parameters value. Only whole number or decimal number allow.')
            print('\n')
            pass


        ''' Run only 1 time when the program is initiated '''
        if first_start_up == True:
            sel_count, selection, final_sel = Check_Analysis_Selection(3, 6, g.window, '-SL12-', True)
            #print('>>> First Start Up')
            #sg.Popup('Ok clicked', keep_on_top=True)
            first_start_up = False


        ''' Ensure user input on 3 phases parameters consist only these characters: 0123456789. '''
        if (event == 'L1N' or event == 'L2N' or event == 'L3N' or
            event == 'L12' or event == 'L23' or event == 'L31' or
            event == 'L21' or event == 'L32' or event == 'L13' or event == 'Un_SRefLN' or event == 'Un_SRefLL' or
            event == 'LL_Start' or event == 'LN_Start' or
            event == 'LL_Stop' or event == 'LN_Stop' or
            event == 'V_Step' or event == 'Un_GRefLN' or event == 'Un_GRefLL') and \
                (len(values[event]) > 0):

            if values[event][0:1] == '0' and values[event][1:2] not in '.':
                g.window[event].update(values[event][0:1] + '.' + values[event][1:])

            if values[event][-1] not in '0123456789.':
                g.window[event].update(values[event][:-1])

        if (event == 'AL1N'or event == 'AL2N' or event == 'AL3N' or
            event == 'AL12' or event == 'AL23' or event == 'AL31' or
            event == 'AL21' or event == 'AL32' or event == 'AL13' or
            event == 'PH_Start' or event == 'PH_Stop' or event == 'PH_Step') and \
                (len(values[event]) > 0):

            if values[event][0:1] == '0' and values[event][1:2] not in '.':
                g.window[event].update(values[event][0:1] + '.' + values[event][1:])

            if values[event][0:2] == '-0' and values[event][2:3] not in '.':
                g.window[event].update(values[event][0:2] + '.' + values[event][2:])

            if values[event][-1] not in '0123456789.-':
                g.window[event].update(values[event][:-1])


        ''' Updating user selection of reference phase '''
        if event == '-RL1N-':
            Convert_Ref_Phase(AL1N, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL2N-':
            Convert_Ref_Phase(AL2N, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL3N-':
            Convert_Ref_Phase(AL3N, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL12-':
            Convert_Ref_Phase(AL12, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL23-':
            Convert_Ref_Phase(AL23, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL31-':
            Convert_Ref_Phase(AL31, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL21-':
            Convert_Ref_Phase(AL21, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL32-':
            Convert_Ref_Phase(AL32, g.window, values)
            #print('>>> ', 'A' + event[2:5])
        elif event == '-RL13-':
            Convert_Ref_Phase(AL13, g.window, values)
            #print('>>> ', 'A' + event[2:5])

        ''' Updating user selection of phases for analysis '''
        if event == '-SL1N-' or event == '-SL2N-' or event == '-SL3N-' or \
                event == '-SL12-' or event == '-SL23-' or event == '-SL31-' or \
                event == '-SL21-' or event == '-SL32-' or event == '-SL13-':
            sel_count, selection, final_sel = Check_Analysis_Selection(sel_count, selection, g.window, event, values[event])
            #print('>>> Debug: ', selection, '-', final_sel, '-', sel_count)
            #print(event, '-', values[event])


        if event == '_SHOW PHASOR_':
            calEngine.get_polar_plot()


        if event == '_SHOW WAVEFORM_':
            print('>>> Under development')
            calEngine.get_waveform_plot()


        if event == '_SAVE RECORD_':
            if values['FILENAME'] == '':
                print('>>> No filename defined, no save operation is allowed!')
                print('\n')
            else:
                if df3P.empty:
                    print('>>> Single added record is empty, no save operation is allowed!')
                    print('\n')
                else:
                    try:
                        start = time.time()  # Record start time
                        print('>>> Saving single added record now...')

                        # save single added results to file as .xlsx
                        result_path = os.path.join(values['DESTINATION_FOLDER_PATH'], values['FILENAME'] + '.xlsx')

                        ''' Calculated Fields '''
                        #df3P = df3P.fillna(0)
                        df3P['LN_Min'] = round(df3P[['L1N', 'L2N', 'L3N']].min(axis=1), 2)
                        df3P['LN_Max'] = round(df3P[['L1N', 'L2N', 'L3N']].max(axis=1), 2)
                        df3P['LN_Asy'] = round((df3P['LN_Max'] - df3P['LN_Min']), 2)
                        df3P['LN_%UV'] = round((df3P['LN_Min'] - df3P['Un_ref_LN'])*100 / df3P['Un_ref_LN'], 2)
                        df3P['LN_%OV'] = round((df3P['LN_Max'] - df3P['Un_ref_LN'])*100 / df3P['Un_ref_LN'], 2)
                        df3P['LN_%ASY'] = round((df3P['LN_Asy'])*100 / df3P['Un_ref_LN'], 2)
                        df3P['LL31_21_32_Min'] = round(df3P[['L31', 'L21', 'L32']].min(axis=1), 2)
                        df3P['LL31_21_32_Max'] = round(df3P[['L31', 'L21', 'L32']].max(axis=1), 2)
                        df3P['LL31_21_32_Asy'] = round((df3P['LL31_21_32_Max'] - df3P['LL31_21_32_Min']), 2)
                        df3P['LL31_21_32_%UV'] = round((df3P['LL31_21_32_Min'] - df3P['Un_ref_LL'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL31_21_32_%OV'] = round((df3P['LL31_21_32_Max'] - df3P['Un_ref_LL'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL31_21_32_%ASY'] = round((df3P['LL31_21_32_Asy'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL13_23_12_Min'] = round(df3P[['L13', 'L23', 'L12']].min(axis=1), 2)
                        df3P['LL13_23_12_Max'] = round(df3P[['L13', 'L23', 'L12']].max(axis=1), 2)
                        df3P['LL13_23_12_Asy'] = round((df3P['LL13_23_12_Max'] - df3P['LL13_23_12_Min']), 2)
                        df3P['LL13_23_12_%UV'] = round((df3P['LL13_23_12_Min'] - df3P['Un_ref_LL'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL13_23_12_%OV'] = round((df3P['LL13_23_12_Max'] - df3P['Un_ref_LL'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL13_23_12_%ASY'] = round((df3P['LL13_23_12_Asy'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL12_32_13_Min'] = round(df3P[['L12', 'L32', 'L13']].min(axis=1), 2)
                        df3P['LL12_32_13_Max'] = round(df3P[['L12', 'L32', 'L13']].max(axis=1), 2)
                        df3P['LL12_32_13_Asy'] = round((df3P['LL12_32_13_Max'] - df3P['LL12_32_13_Min']), 2)
                        df3P['LL12_32_13_%UV'] = round((df3P['LL12_32_13_Min'] - df3P['Un_ref_LL'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL12_32_13_%OV'] = round((df3P['LL12_32_13_Max'] - df3P['Un_ref_LL'])*100 / df3P['Un_ref_LL'], 2)
                        df3P['LL12_32_13_%ASY'] = round((df3P['LL12_32_13_Asy'])*100 / df3P['Un_ref_LL'], 2)

                        df3P.to_excel(result_path, index=False, header=True, sheet_name=values['FILENAME'],
                                      engine='xlsxwriter')

                        # save results to file as .xlsx
                        result_path = os.path.join(values['DESTINATION_FOLDER_PATH'],
                                                   values['FILENAME'] + '_Gen' + '.xlsx')
                        df3P_Gen.to_excel(result_path, index=False, header=True, sheet_name=values['FILENAME'] + '_Gen',
                                          engine='xlsxwriter')
                    except:
                        print('>>> Single added record is not saved, close it and try again...')
                        print('\n')
                        pass
                    else:
                        stop = time.time()  # Record start time
                        print('>>> Save single added record completed. Total time taken is ', stop - start, 's')
                        print('\n')

                if df3P_Gen.empty:
                    print('>>> Data generation record is empty, no save operation is allowed!')
                    print('\n')
                else:
                    try:
                        start = time.time()  # Record start time
                        print('>>> Saving data generation record now...')

                        # save data generation results to file as .xlsx
                        result_path = os.path.join(values['DESTINATION_FOLDER_PATH'],
                                                   values['FILENAME'] + '_Gen' + '.xlsx')

                        ''' Calculated Fields '''
                        # df3P_Gen = df3P_Gen.fillna(0)
                        df3P_Gen['LN_Min'] = round(df3P_Gen[['L1N', 'L2N', 'L3N']].min(axis=1), 2)
                        df3P_Gen['LN_Max'] = round(df3P_Gen[['L1N', 'L2N', 'L3N']].max(axis=1), 2)
                        df3P_Gen['LN_Asy'] = round((df3P_Gen['LN_Max'] - df3P_Gen['LN_Min']), 2)
                        df3P_Gen['LN_%UV'] = round((df3P_Gen['LN_Min'] - df3P_Gen['Un_ref_LN']) * 100 / df3P_Gen['Un_ref_LN'], 2)
                        df3P_Gen['LN_%OV'] = round((df3P_Gen['LN_Max'] - df3P_Gen['Un_ref_LN']) * 100 / df3P_Gen['Un_ref_LN'], 2)
                        df3P_Gen['LN_%ASY'] = round((df3P_Gen['LN_Asy']) * 100 / df3P_Gen['Un_ref_LN'], 2)
                        df3P_Gen['LL31_21_32_Min'] = round(df3P_Gen[['L31', 'L21', 'L32']].min(axis=1), 2)
                        df3P_Gen['LL31_21_32_Max'] = round(df3P_Gen[['L31', 'L21', 'L32']].max(axis=1), 2)
                        df3P_Gen['LL31_21_32_Asy'] = round((df3P_Gen['LL31_21_32_Max'] - df3P_Gen['LL31_21_32_Min']), 2)
                        df3P_Gen['LL31_21_32_%UV'] = round((df3P_Gen['LL31_21_32_Min'] - df3P_Gen['Un_ref_LL']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL31_21_32_%OV'] = round((df3P_Gen['LL31_21_32_Max'] - df3P_Gen['Un_ref_LL']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL31_21_32_%ASY'] = round((df3P_Gen['LL31_21_32_Asy']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL13_23_12_Min'] = round(df3P_Gen[['L13', 'L23', 'L12']].min(axis=1), 2)
                        df3P_Gen['LL13_23_12_Max'] = round(df3P_Gen[['L13', 'L23', 'L12']].max(axis=1), 2)
                        df3P_Gen['LL13_23_12_Asy'] = round((df3P_Gen['LL13_23_12_Max'] - df3P_Gen['LL13_23_12_Min']), 2)
                        df3P_Gen['LL13_23_12_%UV'] = round((df3P_Gen['LL13_23_12_Min'] - df3P_Gen['Un_ref_LL']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL13_23_12_%OV'] = round((df3P_Gen['LL13_23_12_Max'] - df3P_Gen['Un_ref_LL']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL13_23_12_%ASY'] = round((df3P_Gen['LL13_23_12_Asy']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL12_32_13_Min'] = round(df3P_Gen[['L12', 'L32', 'L13']].min(axis=1), 2)
                        df3P_Gen['LL12_32_13_Max'] = round(df3P_Gen[['L12', 'L32', 'L13']].max(axis=1), 2)
                        df3P_Gen['LL12_32_13_Asy'] = round((df3P_Gen['LL12_32_13_Max'] - df3P_Gen['LL12_32_13_Min']), 2)
                        df3P_Gen['LL12_32_13_%UV'] = round((df3P_Gen['LL12_32_13_Min'] - df3P_Gen['Un_ref_LL']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL12_32_13_%OV'] = round((df3P_Gen['LL12_32_13_Max'] - df3P_Gen['Un_ref_LL']) * 100 / df3P_Gen['Un_ref_LL'], 2)
                        df3P_Gen['LL12_32_13_%ASY'] = round((df3P_Gen['LL12_32_13_Asy']) * 100 / df3P_Gen['Un_ref_LL'], 2)

                        df3P_Gen.to_excel(result_path, index=False, header=True, sheet_name=values['FILENAME'] + '_Gen',
                                          engine='xlsxwriter')
                    except:
                        print('>>> Data generation record is not saved, close it and try again...')
                        print('\n')
                        pass
                    else:
                        stop = time.time()  # Record start time
                        print('>>> Save data generation record completed. Total time taken is ', stop - start, 's')
                        print('\n')


        if event in (None, '_CANCEL BUTTON_'):
            print(">>> Program is aborted")
            print('\n')
            break


        if event == '_DELETE RECORD_':
            if df3P.empty:
                print('>>> Single added record is empty, cannot perform delete operation!')
                print('\n')
            else:
                df3P = df3P[:-1]

                g.window['OUTPUT'].Update('')
                print('>>> Total ', len(df3P), 'records found as follow:')
                print(df3P.iloc[:, 0:18])
                print('\n')


        if event == '_SHOW RECORD_':
            if df3P.empty:
                print('>>> Single added record is empty, no record is shown!')
                print('\n')
            else:
                g.window['OUTPUT'].Update('')
                print('>>> Total ', len(df3P), 'records found as follow:')
                print(df3P.iloc[:, 0:18])
                print('\n')


        if event == '_CALCULATE_':
            g.window['_SHOW PHASOR_'].Update(disabled=False)
            g.window['_SHOW WAVEFORM_'].Update(disabled=False)

            if final_sel != '' and sel_count == 3:
                calEngine = ThreePhaseCalcEngine(Calc_Mode=final_sel,
                                                 Magnitude_L1N=L1N, Phase_L1N=any_degree_to_half_angle_radians(AL1N),
                                                 Magnitude_L2N=L2N, Phase_L2N=any_degree_to_half_angle_radians(AL2N),
                                                 Magnitude_L3N=L3N, Phase_L3N=any_degree_to_half_angle_radians(AL3N),
                                                 Magnitude_L12=L12, Phase_L12=any_degree_to_half_angle_radians(AL12),
                                                 Magnitude_L23=L23, Phase_L23=any_degree_to_half_angle_radians(AL23),
                                                 Magnitude_L31=L31, Phase_L31=any_degree_to_half_angle_radians(AL31),
                                                 Magnitude_L21=L21, Phase_L21=any_degree_to_half_angle_radians(AL21),
                                                 Magnitude_L32=L32, Phase_L32=any_degree_to_half_angle_radians(AL32),
                                                 Magnitude_L13=L13, Phase_L13=any_degree_to_half_angle_radians(AL13)
                                                 )

                if final_sel == 'L1N_L2N_L3N':
                    calEngine.calc_result_givenby_L1N_L2N_L3N()
                elif final_sel == 'L21_L31_L1N':
                    calEngine.calc_result_givenby_L21_L31_L1N()
                elif final_sel == 'L21_L13_L1N':
                    calEngine.calc_result_givenby_L21_L13_L1N()
                elif final_sel == 'L12_L31_L1N':
                    calEngine.calc_result_givenby_L12_L31_L1N()
                elif final_sel == 'L12_L13_L1N':
                    calEngine.calc_result_givenby_L12_L13_L1N()
                elif final_sel == 'L12_L32_L2N':
                    calEngine.calc_result_givenby_L12_L32_L2N()
                elif final_sel == 'L12_L23_L2N':
                    calEngine.calc_result_givenby_L12_L23_L2N()
                elif final_sel == 'L21_L32_L2N':
                    calEngine.calc_result_givenby_L21_L32_L2N()
                elif final_sel == 'L21_L23_L2N':
                    calEngine.calc_result_givenby_L21_L23_L2N()
                elif final_sel == 'L13_L23_L3N':
                    calEngine.calc_result_givenby_L13_L23_L3N()
                elif final_sel == 'L13_L32_L3N':
                    calEngine.calc_result_givenby_L13_L32_L3N()
                elif final_sel == 'L31_L23_L3N':
                    calEngine.calc_result_givenby_L31_L23_L3N()
                elif final_sel == 'L31_L32_L3N':
                    calEngine.calc_result_givenby_L31_L32_L3N()

                g.window['L1N'].update(round(calEngine.Magnitude_L1N, 2))
                g.window['AL1N'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L1N), 2))
                g.window['L2N'].update(round(calEngine.Magnitude_L2N, 2))
                g.window['AL2N'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L2N), 2))
                g.window['L3N'].update(round(calEngine.Magnitude_L3N, 2))
                g.window['AL3N'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L3N), 2))
                g.window['L12'].update(round(calEngine.Magnitude_L12, 2))
                g.window['AL12'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L12), 2))
                g.window['L23'].update(round(calEngine.Magnitude_L23, 2))
                g.window['AL23'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L23), 2))
                g.window['L31'].update(round(calEngine.Magnitude_L31, 2))
                g.window['AL31'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L31), 2))
                g.window['L21'].update(round(calEngine.Magnitude_L21, 2))
                g.window['AL21'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L21), 2))
                g.window['L32'].update(round(calEngine.Magnitude_L32, 2))
                g.window['AL32'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L32), 2))
                g.window['L13'].update(round(calEngine.Magnitude_L13, 2))
                g.window['AL13'].update(round(any_radians_to_half_angle_degree(calEngine.Phase_L13), 2))

                new_datarow = {'L1N': round(calEngine.Magnitude_L1N, 2),
                               'AL1N': round(any_radians_to_half_angle_degree(calEngine.Phase_L1N), 2),
                               'L2N': round(calEngine.Magnitude_L2N, 2),
                               'AL2N': round(any_radians_to_half_angle_degree(calEngine.Phase_L2N), 2),
                               'L3N': round(calEngine.Magnitude_L3N, 2),
                               'AL3N': round(any_radians_to_half_angle_degree(calEngine.Phase_L3N), 2),
                               'L12': round(calEngine.Magnitude_L12, 2),
                               'AL12': round(any_radians_to_half_angle_degree(calEngine.Phase_L12), 2),
                               'L23': round(calEngine.Magnitude_L23, 2),
                               'AL23': round(any_radians_to_half_angle_degree(calEngine.Phase_L23), 2),
                               'L31': round(calEngine.Magnitude_L31, 2),
                               'AL31': round(any_radians_to_half_angle_degree(calEngine.Phase_L31), 2),
                               'L21': round(calEngine.Magnitude_L21, 2),
                               'AL21': round(any_radians_to_half_angle_degree(calEngine.Phase_L21), 2),
                               'L32': round(calEngine.Magnitude_L32, 2),
                               'AL32': round(any_radians_to_half_angle_degree(calEngine.Phase_L32), 2),
                               'L13': round(calEngine.Magnitude_L13, 2),
                               'AL13': round(any_radians_to_half_angle_degree(calEngine.Phase_L13), 2),
                               'Un_ref_LN': round(Un_SRefLN, 2),
                               'Un_ref_LL': round(Un_SRefLL, 2)}

                df3P = df3P.append(new_datarow, ignore_index=True)

                g.window['OUTPUT'].Update('')
                print('>>> Total ', len(df3P), 'records found as follow:')
                print(df3P.iloc[:, 0:18])
                print('\n')

            else:
                print(">>> Wrong combination of 3 input parameters, only these 13 combinations are valid.")
                print('>>> L1N_L2N_L3N')
                print('>>> L21_L31_L1N')
                print('>>> L21_L13_L1N')
                print('>>> L12_L31_L1N')
                print('>>> L12_L13_L1N')
                print('>>> L12_L32_L2N')
                print('>>> L12_L23_L2N')
                print('>>> L21_L32_L2N')
                print('>>> L21_L23_L2N')
                print('>>> L13_L23_L3N')
                print('>>> L13_L32_L3N')
                print('>>> L31_L23_L3N')
                print('>>> L31_L32_L3N')
                print('\n')

        if event == '_GEN_DATA_':

            ''' Calculation iteration cycles '''
            #Total_LN_Interation = abs(LN_Stop - LN_Start) / V_Step
            #Total_LL_Interation = abs(LL_Stop - LL_Start) / V_Step
            #Total_AG_Interation = abs(PH_Stop - PH_Start) / PH_Step

            Total_LN_Interation = int(round_up(LN_Stop - LN_Start) / V_Step)+ 1
            Total_LL_Interation = int(round_up(LL_Stop - LL_Start) / V_Step) + 1
            Total_AG_Interation = int(round_up(PH_Stop - PH_Start) / PH_Step) + 1

            Total_Iteration = ((Total_LN_Interation + 1) * (Total_LL_Interation + 1) * (Total_AG_Interation + 1)) * \
                              ((Total_LN_Interation + 1) * (Total_LL_Interation + 1) * (Total_AG_Interation + 1))

            z = 0
            ContinueGenerate = True

            print(LN_Start, ",", LN_Stop, ",", LL_Start, ",", LL_Stop, ",", V_Step, ",", PH_Step, ",")
            print(Total_LN_Interation, ",", Total_LL_Interation, ",", Total_AG_Interation, ",")

            #LNTemp = LN_Start
            for i in range(Total_LN_Interation + 1):
                #LNTemp = LNTemp + V_Step
                LNTemp = (V_Step * i) + LN_Start

                if i == (Total_LN_Interation):
                    LNTemp = LN_Stop
                T_L1N = float(LNTemp)
                T_L2N = float(LNTemp)
                T_L3N = float(LNTemp)
                if ContinueGenerate == False:
                    break

                #PHLNTemp = PH_Start
                for j in range(Total_AG_Interation + 1):
                    #PHLNTemp = PHLNTemp + PH_Step
                    PHLNTemp = (PH_Step * j) + PH_Start

                    if j == (Total_AG_Interation):
                        PHLNTemp = PH_Stop
                    T_AL1N = float(PHLNTemp)
                    T_AL2N = float(PHLNTemp)
                    T_AL3N = float(PHLNTemp)
                    if ContinueGenerate == False:
                        break

                    #LLTemp1 = LL_Start
                    for k in range(Total_LL_Interation + 1):
                        #LLTemp1 = LLTemp1 + V_Step
                        LLTemp1 = (V_Step * k) + LL_Start

                        if k == (Total_LL_Interation):
                            LLTemp1 = LL_Stop
                        T_L21 = float(LLTemp1)
                        T_L13 = float(LLTemp1)
                        T_L12 = float(LLTemp1)
                        if ContinueGenerate == False:
                            break

                        #PHLLTemp1 = PH_Start
                        for l in range(Total_AG_Interation + 1):
                            #PHLLTemp1 = PHLLTemp1 + PH_Step
                            PHLLTemp1 = (PH_Step * l) + PH_Start

                            if l == (Total_AG_Interation):
                                PHLLTemp1 = PH_Stop
                            T_AL21 = float(PHLLTemp1)
                            T_AL13 = float(PHLLTemp1)
                            T_AL12 = float(PHLLTemp1)
                            if ContinueGenerate == False:
                                break

                            #LLTemp2 = LL_Start
                            for m in range(Total_LL_Interation + 1):
                                #LLTemp2 = LLTemp2 + V_Step
                                LLTemp2 = (V_Step * m) + LL_Start

                                if m == (Total_LL_Interation):
                                    LLTemp2 = LL_Stop
                                T_L31 = float(LLTemp2)
                                T_L23 = float(LLTemp2)
                                T_L32 = float(LLTemp2)
                                if ContinueGenerate == False:
                                    break

                                #PHLLTemp2 = PH_Start
                                for n in range(Total_AG_Interation + 1):
                                    #PHLLTemp2 = PHLLTemp2 + PH_Step
                                    PHLLTemp2 = (PH_Step * n) + PH_Start

                                    if n == (Total_AG_Interation):
                                        PHLLTemp2 = PH_Stop
                                    T_AL31 = float(PHLLTemp2)
                                    T_AL23 = float(PHLLTemp2)
                                    T_AL32 = float(PHLLTemp2)

                                    ''' Display counter windows'''
                                    z = z + 1
                                    ContinueGenerate = sg.one_line_progress_meter('Data Generation',
                                                                                  z,
                                                                                  round(Total_Iteration, 0),
                                                                                  'key',
                                                                                  'Generating data ...',
                                                                                  orientation='horizontal')

                                    if values['L31_L21_L1N'] == True:
                                        #print('L31_L21_L1N')
                                        calEngine = ThreePhaseCalcEngine(
                                            Calc_Mode='L21_L31_L1N',
                                            Magnitude_L1N=T_L1N, Phase_L1N=any_degree_to_half_angle_radians(T_AL1N),
                                            Magnitude_L2N=T_L2N, Phase_L2N=any_degree_to_half_angle_radians(T_AL2N),
                                            Magnitude_L3N=T_L3N, Phase_L3N=any_degree_to_half_angle_radians(T_AL3N),
                                            Magnitude_L12=T_L12, Phase_L12=any_degree_to_half_angle_radians(T_AL12),
                                            Magnitude_L23=T_L23, Phase_L23=any_degree_to_half_angle_radians(T_AL23),
                                            Magnitude_L31=T_L31, Phase_L31=any_degree_to_half_angle_radians(T_AL31),
                                            Magnitude_L21=T_L21, Phase_L21=any_degree_to_half_angle_radians(T_AL21),
                                            Magnitude_L32=T_L32, Phase_L32=any_degree_to_half_angle_radians(T_AL32),
                                            Magnitude_L13=T_L13, Phase_L13=any_degree_to_half_angle_radians(T_AL13))
                                        calEngine.calc_result_givenby_L21_L31_L1N()

                                    elif values['L13_L23_L3N'] == True:
                                        #print('L13_L23_L3N')
                                        calEngine = ThreePhaseCalcEngine(
                                            Calc_Mode='L13_L23_L3N',
                                            Magnitude_L1N=T_L1N, Phase_L1N=any_degree_to_half_angle_radians(T_AL1N),
                                            Magnitude_L2N=T_L2N, Phase_L2N=any_degree_to_half_angle_radians(T_AL2N),
                                            Magnitude_L3N=T_L3N, Phase_L3N=any_degree_to_half_angle_radians(T_AL3N),
                                            Magnitude_L12=T_L12, Phase_L12=any_degree_to_half_angle_radians(T_AL12),
                                            Magnitude_L23=T_L23, Phase_L23=any_degree_to_half_angle_radians(T_AL23),
                                            Magnitude_L31=T_L31, Phase_L31=any_degree_to_half_angle_radians(T_AL31),
                                            Magnitude_L21=T_L21, Phase_L21=any_degree_to_half_angle_radians(T_AL21),
                                            Magnitude_L32=T_L32, Phase_L32=any_degree_to_half_angle_radians(T_AL32),
                                            Magnitude_L13=T_L13, Phase_L13=any_degree_to_half_angle_radians(T_AL13))
                                        calEngine.calc_result_givenby_L13_L23_L3N()

                                    elif values['L12_L32_L2N'] == True:
                                        #print('L12_L32_L2N')
                                        calEngine = ThreePhaseCalcEngine(
                                            Calc_Mode='L12_L32_L2N',
                                            Magnitude_L1N=T_L1N, Phase_L1N=any_degree_to_half_angle_radians(T_AL1N),
                                            Magnitude_L2N=T_L2N, Phase_L2N=any_degree_to_half_angle_radians(T_AL2N),
                                            Magnitude_L3N=T_L3N, Phase_L3N=any_degree_to_half_angle_radians(T_AL3N),
                                            Magnitude_L12=T_L12, Phase_L12=any_degree_to_half_angle_radians(T_AL12),
                                            Magnitude_L23=T_L23, Phase_L23=any_degree_to_half_angle_radians(T_AL23),
                                            Magnitude_L31=T_L31, Phase_L31=any_degree_to_half_angle_radians(T_AL31),
                                            Magnitude_L21=T_L21, Phase_L21=any_degree_to_half_angle_radians(T_AL21),
                                            Magnitude_L32=T_L32, Phase_L32=any_degree_to_half_angle_radians(T_AL32),
                                            Magnitude_L13=T_L13, Phase_L13=any_degree_to_half_angle_radians(T_AL13))
                                        calEngine.calc_result_givenby_L12_L32_L2N()

                                    new_datarow = \
                                        {
                                        'L1N': round(calEngine.Magnitude_L1N, 2),
                                        'AL1N': round(any_radians_to_half_angle_degree(calEngine.Phase_L1N), 2),
                                        'L2N': round(calEngine.Magnitude_L2N, 2),
                                        'AL2N': round(any_radians_to_half_angle_degree(calEngine.Phase_L2N), 2),
                                        'L3N': round(calEngine.Magnitude_L3N, 2),
                                        'AL3N': round(any_radians_to_half_angle_degree(calEngine.Phase_L3N), 2),
                                        'L12': round(calEngine.Magnitude_L12, 2),
                                        'AL12': round(any_radians_to_half_angle_degree(calEngine.Phase_L12), 2),
                                        'L23': round(calEngine.Magnitude_L23, 2),
                                        'AL23': round(any_radians_to_half_angle_degree(calEngine.Phase_L23), 2),
                                        'L31': round(calEngine.Magnitude_L31, 2),
                                        'AL31': round(any_radians_to_half_angle_degree(calEngine.Phase_L31), 2),
                                        'L21': round(calEngine.Magnitude_L21, 2),
                                        'AL21': round(any_radians_to_half_angle_degree(calEngine.Phase_L21), 2),
                                        'L32': round(calEngine.Magnitude_L32, 2),
                                        'AL32': round(any_radians_to_half_angle_degree(calEngine.Phase_L32), 2),
                                        'L13': round(calEngine.Magnitude_L13, 2),
                                        'AL13': round(any_radians_to_half_angle_degree(calEngine.Phase_L13), 2),
                                        'Un_ref_LN': round(Un_GRefLN, 2),
                                        'Un_ref_LL': round(Un_GRefLL, 2)
                                        }

                                    df3P_Gen = df3P_Gen.append(new_datarow, ignore_index=True)

                                    #g.window['OUTPUT'].Update('')
                                    print('>>> Total ', len(df3P_Gen), 'records found as follow:')
                                    print(df3P_Gen.iloc[:, 0:18])
                                    print('\n')

                                    if ContinueGenerate == False:
                                        break


        if event == '_CLEAR_DATA_':
            if df3P_Gen.empty:
                print('>>> Data generation record is empty, cannot perform delete operation!')
                print('\n')
            else:
                df3P_Gen = df3P_Gen[0:0]   #Clear data frame

                g.window['OUTPUT'].Update('')
                print('>>> Total ', len(df3P_Gen), 'records found as follow:')
                print(df3P_Gen.iloc[:, 0:18])
                print('\n')

    g.window.close()

if __name__ == '__main__':
    timestamp = datetime.now()
    default_save_path = os.path.join('C:\\', 'Users', os.getlogin().lower(), 'Downloads')
    default_filename = '3_Phase_Record'
    print("<< Starting program... by", os.getlogin(), "under " + sys.platform + " operating system >>")
    main()
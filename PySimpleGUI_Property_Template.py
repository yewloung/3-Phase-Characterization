import sys

'''Applicable to Text, InputText, Radio, Checkbox, Combo, Listbox, Output'''
def Disable_Text_Related_Element(windows, key_list):
    for x in range(len(key_list)):
        try:
            #print(key_list[x])
            windows[key_list[x]].update(disabled=True, text_color='#8E8E8E', background_color='#555555')
        except:
            print("Oops!", sys.exc_info()[0], "occurred, next try continue...")
            print()
    return 0


def Enable_Text_Related_Element(windows, key_list):
    for x in range(len(key_list)):
        try:
            #print(key_list[x])
            windows[key_list[x]].update(disabled=False, text_color='#000000', background_color='#FFFFFF')
        except:
            print("Oops!", sys.exc_info()[0], "occurred, next try continue...")
            print()
    return 0


def Empty_Text_Related_Element(windows, key_list):
    for x in range(len(key_list)):
        try:
            #print(key_list[x])
            windows[key_list[x]].update('')
        except:
            print("Oops!", sys.exc_info()[0], "occurred, next try continue...")
            print()
    return 0
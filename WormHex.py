import os
import re
import PySimpleGUI as sg
import numpy as np

sg.SetOptions(background_color = 'lightblue',
            element_background_color = 'lightblue',
            text_element_background_color = 'lightblue',
            text_color='Black',
            font= ('Calibri', 14, 'bold'))
layout2 =[
    [sg.Text('Select the file you want to process', justification='center'),
      sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse()],
    [sg.Text('Select the application you want to process', justification='center')],
    [sg.InputCombo(values=['WhatsApp', 'Twitter', 'Telegram'],enable_events=True, 
    key='combo', size=(30, 6)),  sg.Button('Analyze')],
    [sg.Listbox(values =[''], size = (50, 15), font = ('Calibri', 16), background_color ='White',
    key = '_display_') ]]


layout1 =[[sg.Image('wormHex logo.png', key='__IMAGE__', size=(540, 200) )],
    [sg.Text('Welcome to WormHex Tool', font = ('Calibri', 24,'bold'), justification='center',
     text_color='black')],
    [sg.Text('Developed By:', font = ('Calibri', 18,'bold'), justification='center', 
    text_color='Black')],
    [sg.Text('Wadha Almatter\n'+'Nora Almubairik\n'+'Amani Alqarni',font = ('Calibri', 16),
     justification='center', text_color='Black')],
    [sg.Button('Start'), sg.Button('Exit')]
    ]
layout = [[sg.Column(layout1, size=(580,500), key='-COL1-', element_justification="center"), sg.Column(layout2, element_justification="center", visible=False, size=(580, 500), key='-COL2-')],
          ]

window = sg.Window('WormHex', element_justification="center"
).Layout(layout)

#function to display list
def display_list(list1):
    global list_displayed
    #store list in Multiline text globally
    list_displayed = list1
    #add list elements with new line
    values = [l for l in list1]          
    window.FindElement('_display_').Update(values)
        
def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    # return string   
    return str1  
layout = 1 
while True:
    event, values = window.Read()

    if event is None or event == 'Exit':
        break
    if event == 'Start':
        window[f'-COL{layout}-'].update(visible=False)
        layout = layout + 1 if layout < 3 else 1
        window[f'-COL{layout}-'].update(visible=True)
    if event == 'Analyze':
        # Whatsaap: Extract Mobile Numbers (Regex)
        line=['********************']
        dirname, filename = os.path.split(os.path.abspath(__file__))
        pathname = values["-FILE-"]
        my_file_handle=open(pathname,encoding='unicode_escape')
        mem = my_file_handle.read()
        application=values['combo']
        if application == 'WhatsApp':
            list_of_lists2 = []
            m='Mobile Numbers'
            list_of_lists2.append(m)
            list_of_lists2.append(line)

            Mobiles = re.findall(r'\d{12}@s.whatsapp.net',mem)
            if Mobiles != None:
                Mobiles = np.unique(re.findall(r'\d{12}',listToString(Mobiles)))
            for p in Mobiles: 
                list_of_lists2.append(p)
            display_list(list_of_lists2)
        else:
            if application=='Twitter':
                list_of_lists=[]                
                t='Tweets'
                list_of_lists.append(t)
                list_of_lists.append(line)
                tweets_regex = re.findall(r'"full_text":.*?,',mem)
                tweets = [re.sub(r'"full_text":','',i)  for i in tweets_regex]
                for p in tweets: 
                    list_of_lists.append(p)
                list_of_lists.append('\n')
                a='Accounts Names'
                list_of_lists.append(a)
                list_of_lists.append(line)
                name_regex = re.findall(r'"name":".*?,',mem)
                for p in name_regex: 
                    list_of_lists.append(p)
                list_of_lists.append('\n')
                s='Screen Names'
                list_of_lists.append(s)
                list_of_lists.append(line)
                screenName_regex = re.findall(r'"screen_name":".*?,',mem)
                for p in screenName_regex: 
                    list_of_lists.append(p)
                list_of_lists.append('\n')
                ts='Tweets timestamp'
                list_of_lists.append(ts)
                list_of_lists.append(line)
                Account_regex = re.findall(r'"created_at.*?,',mem)
                for p in Account_regex: 
                    list_of_lists.append(p)
                list_of_lists.append('\n')
                f='Normal followers count'
                list_of_lists.append(f)
                list_of_lists.append(line)
                followers_regex = re.findall(r'normal_followers_count.*?,',mem)
                for p in followers_regex:
                    list_of_lists.append(p)
                display_list(list_of_lists)
            else:
                if application=='Telegram':
                    display_list(['***There is no data***'])
window.close()

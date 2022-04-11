import PySimpleGUI as sg



def fixVal():
    layout = [[sg.Text('Enter the Correct Value From your Bottle for')],  # this sort of field can be updated...
              [sg.Input('', enable_events=True, key='-INPUT-', )],
              # [sg.Button('Ok', key='-OK-'), sg.Button('Exit')],
              [sg.Button('Submit', visible=False, bind_return_key=True)]

              ]

    window = sg.Window('Window Title', layout)

    tempVar = ''
    while True:
        event, values = window.read()

        if len(values['-INPUT-']) and values['-INPUT-'][-1] not in ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+{}[];'",.<`~>:/?"):
        # delete last char from input
            window['-INPUT-'].update(values['-INPUT-'][:-1])

        elif event == 'Submit':
        # print('You have submited %s' % window['-INPUT-'].get())
            tempVar = window['-INPUT-'].get()

            window.close()
            return tempVar

    # elif event == 'Ok':
    #     # print('You have submited %s' % window['-INPUT-'].get())
    #     window.close()

#
# window.close()

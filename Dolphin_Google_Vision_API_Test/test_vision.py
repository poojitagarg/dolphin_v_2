import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import pandas as pd
from proto.marshal.collections.repeated import RepeatedComposite
import proto
import json
import numpy as np
from google.protobuf.json_format import MessageToJson
from google.cloud.vision_v1 import AnnotateImageResponse
from flask import Flask
from flask import request
from flask import render_template
import cv2
import imutils

from test import file_path 
from test import f_p
app = Flask(__name__)

UPLOAD_FOLDER = "/Users/mac/Desktop/Minor project/web_app/static"
alphabet = "abcdefghijklmnopqrstuvwxyz 0123456789,;.!?:'\"/\\|_@#%^&*~`+-=<>()[]{}"
char_len = len(alphabet)
output1 = ""
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'dolphin-393123-2ac6bf25dfab.json'

client=vision.ImageAnnotatorClient()
print("print llll",f_p)





file_name=os.path.abspath('/Users/Poojita/Desktop/Dolphin_Google_Vision_API_Test/IMG_7080.jpg')

with io.open(file_name,'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.text_detection(image=image)  #returns textAnnotation

# serialize / deserialize proto (binary)
serialized_proto_plus = AnnotateImageResponse.serialize(response)
response = AnnotateImageResponse.deserialize(serialized_proto_plus)
# print("response.full_text_annotation.textpppppppp",response.full_text_annotation)

#annotations
string_data=response.full_text_annotation.text

#Download text file 
def download_text_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

#Append text file
def append_text_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)


#----> FOR NOW SINGLE FILE 
file_name="code_file.js"
if os.path.exists(file_name):
    # If the file exists, remove it
    os.remove(file_name)



# #Create databse for command <-> Code <-> argument1 <-> argument2 <-> argument3
# db_code_arr = {
#     'Command': ['CHANNEL', 'SEND A', 'PRESS BUTTON'],
#     'Code': [f"basic.forever(function(){{radio.setGroup({{{arg_1}}});if (true){{ }} }})","p" ,'''o''' ],
#     'arg_1':[120,0,0],
#     'arg_2':[0,0,0],
#     'code_w_arg':["","",""]
# }
# db_code = pd.DataFrame(db_code_arr)
# print(db_code)

# def populate_code(row):
#     message = row['Message']
#     message = message.replace('{name_placeholder}', row['arg_1'])

#     return message

# db_code['Code'] = db_code.apply(populate_code, axis=1)



# # db_code['Code'] = db_code['Code'].apply(lambda x: x.format(arg_1=db_code['arg_1']))
# print("bbbbbbbb",db_code)

##### Cascading parameters to use in the last!! ----------for CODE_CHANNEL !!!!!!(forever loop only)


# CHANNEL LOOP IF
forever_loop_default_if= "" 
forever_if_condition_input_1 = "true"
forever_if_condition_input_2 = "true"
forever_if_condition_input_3 = "true"
forever_if_condition_input_4 = "true"
forever_if_condition_input_5 = "true"


# CHANNEL LOOP ELIF
forever_loop_elseif_cond_input = "true"
forever_loop_elseif_default_if= "" 

# CHANNEL LOOP ELSE
forever_loop_else_default= "" 

and_or=""
code_channel=''


# VARIABLES FOR RADIO RECEIVED LOOP MAIN
 

radio_received_if_condition_input = "HI"
radio_received_loop_default_if= "" 


code_radio_received=''





#variables
channel_no=0
loop_change_index=100
forever_else_if_change_index_jump = 100
forever_else_change_index_jump = 100








#Extracting commands
commands = string_data.split("\n")
# print(commands)
df = pd.DataFrame({"command": commands,"full_command":0,"code_command":0})



for index, row in df.iterrows():
    value = row['command']
    
    if 'GET A MESSAGE' == value:
        # print("Get a message", index)
        loop_change_index = index
        get_a_msg_row = df[df['command'] == 'GET A MESSAGE'].index[0]
        print(get_a_msg_row)
        radio_received_if_condition_input =df.loc[get_a_msg_row+1, 'command']
  
    else:
        pass

    if 'ELSE IF' == value:
        # print("ELSE IF", index)
        forever_else_if_change_index_jump = index
      
    else:
        pass

    if 'ELSE' == value:
        # print("ELSE", index)
        forever_else_change_index_jump = index
       
    else:
        pass
    
    #processign for "On shake" command
    if 'SHAKE' == value:
        if index > loop_change_index:
            # radio_received_loop_default_if="input.isGesture(Gesture.Shake)"
            pass
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_cond_input="input.isGesture(Gesture.Shake)"
        else:
            forever_if_condition_input_1="input.isGesture(Gesture.Shake)"
    else:
        pass
    
    #processing for "Hear sound" command
    if 'HEAR' == value:
        print("index imp",index,loop_change_index,forever_else_if_change_index_jump)
        if index > loop_change_index:
            # radio_received_loop_default_if="input.soundLevel() >= 0"
            pass
        
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_cond_input="input.soundLevel() >= 0"
            pass
        
        else:
            forever_if_condition_input_2="input.soundLevel() >= 0"
    else:
        pass

    if 'PRESS BUTTON' == value:

        filtered_button_row = df[df['command'] == 'PRESS BUTTON'].index[0]
      
        button_letter ='A'
        if index > loop_change_index:
            pass
            # radio_received_loop_default_if="input.buttonIsPressed(Button.%s);"%(button_letter)
        
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_cond_input="input.buttonIsPressed(Button.%s)"%(button_letter) 
            pass
        else:
            forever_if_condition_input_3="input.buttonIsPressed(Button.%s)"%(button_letter) 
    else:
        pass


    # processing for smaller than and greater than ------------forever_if_condition_input_second
    if ('SMALLER THAN' == value): 
        filtered_send_row = df[df['command'] == 'SMALLER THAN'].index[0]
        comparing_no=df.loc[filtered_send_row+1, 'command']

        
        if index > loop_change_index:
            pass
            # radio_received_loop_default_if="input.buttonIsPressed(Button.%s);"%(button_letter)
        
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_cond_input='''pins.analogReadPin(AnalogPin.P0) < %d'''%(int(comparing_no))
            pass
        
        else:
            forever_if_condition_input_4='''pins.analogReadPin(AnalogPin.P0) < %d'''%(int(comparing_no))
    
    else:
        pass

    # processing for larger than  ------------forever_if_condition_input_second
    if ('LARGER THAN' == value): 
        filtered_send_row = df[df['command'] == 'LARGER THAN'].index[0]
        comparing_no=df.loc[filtered_send_row+1, 'command']

        # if index > loop_change_index:
        #     radio_received_loop_default_if=radio_received_loop_default_if+code_send
        # else:
        if index > loop_change_index:
            pass
            # radio_received_loop_default_if="input.buttonIsPressed(Button.%s);"%(button_letter)
        
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_cond_input='''pins.analogReadPin(AnalogPin.P0) > %d'''%(int(comparing_no))
            pass
        
        else:
            forever_if_condition_input_5='''pins.analogReadPin(AnalogPin.P0) > %d'''%(int(comparing_no))
    
    else:
        pass


#End of IF conditions input cases


#Start of action cases ----------------------------------------------------------------------

   #processing for "SEND A" Command
    if 'SEND A' == value: 
        filtered_send_row = df[df['command'] == 'SEND A'].index[0]
        df.loc[filtered_send_row, 'full_command'] = 'MESSAGE '+df.loc[filtered_send_row+2, 'command']
        # send_msg=df.loc[filtered_send_row+2, 'command']
        code_send='''radio.sendString("HI");'''
        df.loc[filtered_send_row, 'code_command']=code_send

        if index > loop_change_index:
            radio_received_loop_default_if=radio_received_loop_default_if+code_send
     
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_default_if = forever_loop_elseif_default_if+code_send
        
        elif index > forever_else_change_index_jump:
            forever_loop_else_default = forever_loop_else_default+code_send
        
        else:
            forever_loop_default_if=forever_loop_default_if+code_send
    else:
        pass






    #processing for 'PLAY SOUND'

    if 'PLAY' == value:
        if index > loop_change_index:
            print("ppppppppooooo")
            radio_received_loop_default_if=radio_received_loop_default_if+"music.play(music.builtinPlayableSoundEffect(soundExpression.happy), music.PlaybackMode.UntilDone);"
            print("ppppppp")
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_default_if = forever_loop_elseif_default_if+"music.play(music.builtinPlayableSoundEffect(soundExpression.happy), music.PlaybackMode.UntilDone);"
      
        elif index > forever_else_change_index_jump:
            forever_loop_else_default = forever_loop_else_default+"music.play(music.builtinPlayableSoundEffect(soundExpression.happy), music.PlaybackMode.UntilDone);"
        
        else:
            forever_loop_default_if =forever_loop_default_if+"music.play(music.builtinPlayableSoundEffect(soundExpression.happy), music.PlaybackMode.UntilDone);"
    else:
        pass


    #processing for 'SHOW'
    if 'SHOW' == value:

        if index > loop_change_index:
            radio_received_loop_default_if=radio_received_loop_default_if+"basic.showIcon(IconNames.Heart);"
        
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_default_if = forever_loop_elseif_default_if+"basic.showIcon(IconNames.Heart);"
       
        elif index > forever_else_change_index_jump:
            forever_loop_else_default = forever_loop_else_default+"basic.showIcon(IconNames.Heart);"
        
        else:
            forever_loop_default_if= forever_loop_default_if+"basic.showIcon(IconNames.Heart);"
    else:
        pass

    #processing for 'TURN ON'
    if 'TURN ON' == value:

        if index > loop_change_index:
            radio_received_loop_default_if=radio_received_loop_default_if+"pins.digitalWritePin(DigitalPin.P0, 1);"
        
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_default_if = forever_loop_elseif_default_if+"pins.digitalWritePin(DigitalPin.P0, 1);"
       
        elif index > forever_else_change_index_jump:
            forever_loop_else_default = forever_loop_else_default+"pins.digitalWritePin(DigitalPin.P0, 1);"
        
        
        else:
            forever_loop_default_if= forever_loop_default_if+"pins.digitalWritePin(DigitalPin.P0, 1);"
    else:
        pass

    #processing for 'TURN OFF'
    if 'TURN OFF' == value:

        if index > loop_change_index:
            radio_received_loop_default_if=radio_received_loop_default_if+"pins.digitalWritePin(DigitalPin.P0, 0);"
       
        elif index > forever_else_if_change_index_jump:
            forever_loop_elseif_default_if = forever_loop_elseif_default_if+"pins.digitalWritePin(DigitalPin.P0, 0);"
       
        elif index > forever_else_change_index_jump:
            forever_loop_else_default = forever_loop_else_default+"pins.digitalWritePin(DigitalPin.P0, 0);"
        
        
        else:
            forever_loop_default_if= forever_loop_default_if+"pins.digitalWritePin(DigitalPin.P0, 0);"
    else:
        pass


    #processing for AND
    if 'AND' == value:
        and_or="AND"
    else:
        pass

    #processing for OR
    if 'OR' == value:
        and_or="OR"
    else:
        pass
    
     



    #processing for "CHANNEL" Command [only for the Forever loop!!!!!]
    if 'CHANNEL' == value:
        filtered_channel_row = df[df['command'] == 'CHANNEL'].index[0]
        df.loc[filtered_channel_row, 'full_command'] = df.loc[filtered_channel_row-1, 'command']+" "+'CHANNEL'
        if(filtered_channel_row == 0 ):
            channel_no = 0
        else: 
            channel_no=df.loc[filtered_channel_row-1, 'command']
    

    else:
        pass


## --------ONLY for CHANNEL aka Forever loop code!!! Still left for on radio received code!!!

channel_if_condition_data = {
    "forever_if_condition_input_1": forever_if_condition_input_1,
    "forever_if_condition_input_2": forever_if_condition_input_2,
    "forever_if_condition_input_3": forever_if_condition_input_3,
    "forever_if_condition_input_4": forever_if_condition_input_4,
    "forever_if_condition_input_5": forever_if_condition_input_5,
}



# Find values where the corresponding values are not equal to "true"
not_true_values = [value for value, value in channel_if_condition_data.items() if value != "true"]




if len(not_true_values) == 1:
    code_channel = '''basic.forever(function () {radio.setGroup(%d);if (%s) {%s } else if (%s) {%s } else {%s}});'''%(int(channel_no),str(not_true_values[0]),str(forever_loop_default_if),str(forever_loop_elseif_cond_input),str(forever_loop_elseif_default_if),str(forever_loop_else_default))





elif len(not_true_values) ==2:
    # print("ppppppp00-----",not_true_values[1])
    if and_or == "AND":
        code_channel = '''basic.forever(function () {radio.setGroup(%d);if (%s && %s) {%s } else if (%s) {%s } else {%s}});'''%(int(channel_no),str(not_true_values[0]),str(not_true_values[1]),str(forever_loop_default_if),str(forever_loop_elseif_cond_input),str(forever_loop_elseif_default_if),str(forever_loop_else_default))
    elif and_or == "OR":
        code_channel = '''basic.forever(function () {radio.setGroup(%d);if (%s || %s) {%s } else if (%s) {%s } else {%s}});'''%(int(channel_no),str(not_true_values[0]),str(not_true_values[1]),str(forever_loop_default_if),str(forever_loop_elseif_cond_input),str(forever_loop_elseif_default_if),str(forever_loop_else_default))




code_radio_received = '''radio.onReceivedString(function (receivedString) {if (receivedString == "HI") {%s  }});'''%(str(radio_received_loop_default_if))

append_text_to_file(file_name, code_channel)
append_text_to_file(file_name, code_radio_received)
# print(df)






















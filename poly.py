print(
    """
######################################################################################
######################################################################################

   ▄███████▄  ▄██████▄   ▄█       ▄██   ▄          ▄▄▄▄███▄▄▄▄    ▄█  ████████▄   ▄█  
  ███    ███ ███    ███ ███       ███   ██▄      ▄██▀▀▀███▀▀▀██▄ ███  ███   ▀███ ███  
  ███    ███ ███    ███ ███       ███▄▄▄███      ███   ███   ███ ███▌ ███    ███ ███▌ 
  ███    ███ ███    ███ ███       ▀▀▀▀▀▀███      ███   ███   ███ ███▌ ███    ███ ███▌ 
▀█████████▀  ███    ███ ███       ▄██   ███      ███   ███   ███ ███▌ ███    ███ ███▌ 
  ███        ███    ███ ███       ███   ███      ███   ███   ███ ███  ███    ███ ███  
  ███        ███    ███ ███▌    ▄ ███   ███      ███   ███   ███ ███  ███   ▄███ ███  
 ▄████▀       ▀██████▀  █████▄▄██  ▀█████▀        ▀█   ███   █▀  █▀   ████████▀  █▀   
                        ▀                                                            
######################################################################################
######################################################################################
""")

print("A simple tool that allows you to capture midi notes from one source and send them on different channels to a destination to achiece polyphony")

import mido

no_of_voices = int(input("Choose number of voices (1-16):"))
print(mido.get_input_names())
input_device = mido.get_input_names()[int(input(f'Choose input device [0-{len(mido.get_input_names())-1}]:'))]
print(f'Selected: {input_device}')

print(mido.get_output_names())
output_device = mido.get_output_names()[int(input(f'Choose output device [0-{len(mido.get_output_names())-1}]:'))]
print(f'Selected: {output_device}')
voices = {}

for n in range(no_of_voices):
    voices[f'v{n}'] = {'channel': n ,'pressed': False, 'note': 0}

def get_free_voice():
    for voice in voices:
        if (not voices[voice]['pressed']):
            print(f'Free voice found: {voices[voice]}')
            return voices[voice]
        
with mido.open_input(input_device) as inport:
    outport = mido.open_output(output_device)
    for message in inport:
        print(message)
        if (message.type == 'note_on'):
            free_voice = get_free_voice()
            if (free_voice == None):
                print('no free voice available')
            else:
                free_voice['pressed'] = True
                free_voice['note'] = message.note
                outport.send(message.copy(channel=free_voice['channel']))
            
        if (message.type == 'note_off'):
            for voice in voices:
                if (voices[voice]['note'] == message.note):
                    outport.send(message.copy(channel=voices[voice]['channel']))
                    print(f'releasing voice: {voice}')
                    voices[voice]['pressed'] = False

        print(voices)
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

no_of_voices = input("Choose number of voices [1-16] (default: 4):")
if (no_of_voices == ''): no_of_voices = 4
else: no_of_voices = int(no_of_voices)

channel_offset = input("Set channel offset (default: 0):")
if (channel_offset == ''): channel_offset = 0 
else: channel_offset = int(channel_offset)

voices = []
for n in range(no_of_voices):
    voices.append({'channel': n + channel_offset ,'pressed': False, 'note': 0})

def print_devices(devices):
    for c in range(len(devices)):
        print(f'[{c}] {devices[c]}')

print_devices(mido.get_input_names())
input_device = mido.get_input_names()[int(input(f'Choose input device [0-{len(mido.get_input_names())-1}]:'))]
print(f'Selected: {input_device}')

print_devices(mido.get_output_names())
output_device = mido.get_output_names()[int(input(f'Choose output device [0-{len(mido.get_output_names())-1}]:'))]
print(f'Selected: {output_device}')

broadcast = input("Enable broadcast (default=True):")
if (broadcast == ''): broadcast = True
else: broadcast = bool(broadcast)

def get_free_voice():
    for voice in voices:
        if (not voice['pressed']):
            print(f'Free voice found: {voice}')
            return voice
        
with mido.open_input(input_device) as inport:
    outport = mido.open_output(output_device)
    for message in inport:
        if not (message.type == 'clock'): print(message)

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
                if (voice['note'] == message.note):
                    outport.send(message.copy(channel=voice['channel']))
                    print(f'releasing voice: {voice}')
                    voice['pressed'] = False

        if (broadcast and message.type == 'control_change'):
            for voice in voices:
                if not (voice['channel'] == message.channel):
                    outport.send(message.copy(channel=voice['channel']))
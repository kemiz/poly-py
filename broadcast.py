print(
    """
######################################################################################
######################################################################################


▀█████████▄     ▄████████  ▄██████▄     ▄████████ ████████▄   ▄████████    ▄████████    ▄████████     ███     
  ███    ███   ███    ███ ███    ███   ███    ███ ███   ▀███ ███    ███   ███    ███   ███    ███ ▀█████████▄ 
  ███    ███   ███    ███ ███    ███   ███    ███ ███    ███ ███    █▀    ███    ███   ███    █▀     ▀███▀▀██ 
 ▄███▄▄▄██▀   ▄███▄▄▄▄██▀ ███    ███   ███    ███ ███    ███ ███          ███    ███   ███            ███   ▀ 
▀▀███▀▀▀██▄  ▀▀███▀▀▀▀▀   ███    ███ ▀███████████ ███    ███ ███        ▀███████████ ▀███████████     ███     
  ███    ██▄ ▀███████████ ███    ███   ███    ███ ███    ███ ███    █▄    ███    ███          ███     ███     
  ███    ███   ███    ███ ███    ███   ███    ███ ███   ▄███ ███    ███   ███    ███    ▄█    ███     ███     
▄█████████▀    ███    ███  ▀██████▀    ███    █▀  ████████▀  ████████▀    ███    █▀   ▄████████▀     ▄████▀   
               ███    ███                                                                                     
                        ▀                                                            
######################################################################################
######################################################################################
""")

print("A simple tool that allows you to capture midi notes from one source and send them to a range of channels of a destination")

import mido

no_of_channels = input("Choose number of channels [1-16] (default=4):")
if (no_of_channels == ''): no_of_channels = 8
else: no_of_channels = int(no_of_channels)

channel_offset = input("Set channel offset (default=0):")
if (channel_offset == ''): channel_offset = 0 
else: channel_offset = int(channel_offset)

channels = []
for n in range(no_of_channels):
    channels.append(n + channel_offset)

def print_devices(devices):
    for c in range(len(devices)):
        print(f'[{c}] {devices[c]}')

print_devices(mido.get_input_names())
input_device = mido.get_input_names()[int(input(f'Choose input device [0-{len(mido.get_input_names())-1}]:'))]
print(f'Selected: {input_device}')

print_devices(mido.get_output_names())
output_device = mido.get_output_names()[int(input(f'Choose output device [0-{len(mido.get_output_names())-1}]:'))]
print(f'Selected: {output_device}')

with mido.open_input(input_device) as inport:
    outport = mido.open_output(output_device)
    for message in inport:
        if not(message.type == 'clock'):
            print(message)
            for channel in channels:
                outport.send(message.copy(channel=channel))
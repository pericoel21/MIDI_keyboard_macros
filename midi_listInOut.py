import time
import rtmidi

midi_out = rtmidi.MidiOut()
midi_in = rtmidi.MidiIn()

out_ports = midi_out.get_ports()
in_ports = midi_in.get_ports()

def print_listPorts(list):
    x = 0
    for i in list:
        print (f'{x}. {i}')
        x +=1

if __name__ == '__main__':
    print('INPUT PORTS')
    print_listPorts(in_ports)
    print('')
    print('OUTPUT PORTS')
    print_listPorts(out_ports)
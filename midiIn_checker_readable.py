import time
import rtmidi

#midi_port = input('Specify the port to be opened: ')
midi_port = 2

# initialise midi in class
midi_in = rtmidi.MidiIn()

# connect to a device
midi_in.open_port(midi_port)

def numToNote (midi_value):
    # Define a list of note names
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Calculate the octave and note index
    octave = (midi_value // 12) - 1
    note_index = midi_value % 12
    
    # Get the note name and combine it with the octave
    note_name = note_names[note_index]
    full_note_name = f"{note_name}{octave}"
    
    return full_note_name

def numToOperation(midi_value):
    # Define a dictionary mapping operation codes to descriptions
    operation_map = {
        '0x8' : "Note Off",
        '0x9' : "Note On",
        '0xa' : "Polyphonic Key Pressure (Aftertouch)",
        '0xb' : "Control Change",
        '0xc' : "Program Change",
        '0xd' : "Channel Pressure (Aftertouch)",
        '0xe' : "Pitch Bend Change",
        '0xf' : "System Message"
    }

    # Check if the operation code is in the dictionary
    if str(midi_value) in operation_map:
        return operation_map[midi_value]
    else:
        return "Unknown Operation"


# get midi msgs
while True:
    # get a message, returns None if there's no msg in queue
    # also include the time since the last msg
    msg_and_dt = midi_in.get_message()

    # check to see if there is a message
    if msg_and_dt:
        # unpack the msg and time tuple
        (msg, dt) = msg_and_dt

        # convert the command integer to a hex so it's easier to read
        channelNum = str(hex(msg[0]))[:1]
        command = hex(msg[0])[:-1]
        command_name = numToOperation(str(command))
        note = msg[1]
        note_name = numToNote(note)
        print(f'MIDI port: {midi_port}, Channel: {channelNum}, Command: {command} = {command_name}, Note: {note} = {note_name}, dT = {dt}')
    else:
        # add a short sleep so the while loop doesn't hammer your cpu
        time.sleep(0.001)
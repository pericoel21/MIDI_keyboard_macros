#IMPORTANT: MIDIloop or other third party may be needed!
#This third party software is used to reroute MIDI internally,
#via a virtual MIDI channel.
#This is not necessary for the typing functionality, just to use the
#MIDI keyboard as an actual MIDI controller.

import threading
import MIDI_keyboard_macros.midi_utils as midu
import pyautogui as pui

voices = 5 #Number of threads to be created.
# In music production, we call voices to the number of
# keys a synthetizer can play simultaneously


#Initialization of the MIDI input & output ports. 
input_port_num = 2 #It might be necessary to
#check which port the MIDI controlled is connected to.
port_in = midu.openPorts_input(input_port_num) #Input port

output_port_num = 0 #For the output port 2 options are available on Windows.
#First option: Output to the Microsoft GS Wavetable Synth, usually port num. 0
#Second option: Use a third party software to create a virtual MIDI output port.
#This port can be re-routed into a Digital Audio Workspace.
port_out = midu.openPorts_output(output_port_num)
send_out = True

#List of characters
letters = (' ','\n','\t',
           '.',':',',',';','_','-','¿','?','¡','!',
           '1','2','3','4','5','6','7','8','9','0',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W','X','Y','Z',
           ':)','UwU','3==D', '')

i = 50 #Starting note. 50 is a C2 (Do)
#using list comprehension, a dictionary is created to asociate each character
#in "letters" to a note value, starting with the note "i". 
noteToLetter = {(index + i):letter for index, letter in enumerate(letters)}

#Main function of this script, given a note returns a letter
def getLetter(midi, v_treshold = 64, dict = noteToLetter):
    """
    Returns a character given a letter.

    ARGUMENTS:
    midi: dictionary (usually generated by msgParse()) containing the keys:
        Value: Decimal integer with the value (pitch) of the note (0 to 127)
        Command: String, values needed are "Note Off" and "Note On"
        Velocity: Decimal integer with the velocity (volume) of the note (0 to 127)
    
    v_treshold: Integer. Determines the upper-lower case behavior. Default of 64.

    dict: Dictionary containing the values of the notes as the keys, and the 
        correspondong character for each value.

    RETURN:
    This function returns a string containing a character.
    If the character is a letter, it is upper case if the velocity of the iput
    exceeds the treshold value ("v_treshold").
    """
    note = midi['Value']
    command = midi['Command']
    vel = midi['Velocity']

    if command == 'Note On' and note in noteToLetter:
        result = noteToLetter[note]

        if vel <= v_treshold:
            return str.lower(result)
        else:
            return str.upper(result)
        
#Function loop to be used as a thread target
def midiLetter_operator(port_in = int, port_out = 0, send_out = False):
    """
    This function contains a "while True" loop.
    It manages the execution of getLetter() and sends output MIDI messages.

    ARGUMENTS:
    port_in: Input MIDI port

    port_out: Output MIDI port.
        The default value is 0 (Usually the MS GS Wavetable Synth is in this channel)

    send_out: If True, the function sends MIDI messages 
    """
    while True:
        raw_midi_in= midu.input_handler(port_in)

        if raw_midi_in:
            midi_in = raw_midi_in[2]
            letter = getLetter(midi_in)
            if letter:
                print(letter)
                pui.write(letter)

                if send_out:
                    port_out.send_message(raw_midi_in[1])

            elif midi_in['Command'] == 'Note Off' and send_out:
                port_out.send_message(raw_midi_in[1])

#Creates a number of threads in a list
def midiThread_init(num):
    """
    This function creates a list given the desired number of elements.
    Each element is a thread which manages MIDI input/output messages
    thanks to the "midiLetter_operator()" function.

    ARGUMENTS:
    num: Number of threads. This determines the number of simultaneous i/o.
    """
    threads = [threading.Thread(target = midiLetter_operator,
                                args=(port_in, port_out, send_out))
               for _ in range (num)]

    return threads

if __name__ == '__main__':
    threads = midiThread_init(voices)
    
    for thr in threads:
        thr.start()
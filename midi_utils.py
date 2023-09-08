import time
import rtmidi
import threading

def numToNote (midi_value):
    """
    Transforms MIDI pitch values into notes in English musical notation
    """
    # Define a list of note names
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Calculate the octave and note index
    octave = (midi_value // 12) - 1
    note_index = midi_value % 12
    
    # Get the note name and combine it with the octave
    note_name = note_names[note_index]
    
    return (note_name, octave)

def numToOperation(midi_value):
    """
    Creates a dictionary which maps MIDI operation codes to descriptions
    """
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
        #raise 404
        return "Unknown Operation"

def msgParse(msg_and_dt = tuple):
    """
    Given a MIDI message, returns its components within a dictionary.
    
    ARGUMENT: msg_and_dt: Tuple with the MIDI info

    RETURN DICTIONARY:
    Channel: Integer, number of the MIDI channel
    Note: Name of the note in English musical notation
    Value: Decimal MIDI value of the note (0 to 127)
    Velocity: MIDI value of the velocity (0 to 127)
    Command: Name of the executed command
    Delta Time: Time passed since the last MIDI message
    """
    
    # unpack the msg and time tuple
    (msg, dt) = msg_and_dt

    # convert the command integer to a hex so it's easier to read
    channelNum = str(hex(msg[0]))[:1]
    command = hex(msg[0])[:-1]
    command_name = numToOperation(str(command))
    vel = msg[2]
    note = msg[1]
    note_name = numToNote(note)

    msg_map = {
        'Channel' : int(channelNum)+1,
        'Note' : note_name,
        'Value' : note,
        'Velocity' : vel,
        'Command' : command_name,
        'Delta Time' : dt
    }

    return msg_map

def mapRange(value = float, in_ran = (0,127), out_ran = (0,1)):
  """
  Remaps a value from a range to a target range.

  ARGUMENTS:
    value: Float, the value to be remapped.
    
    in_ran: Tuple, contains the lower and higher bounds of the range
    to remap from.

    out_ran: Tuple, contains the lower and higher bounds of the range
    to remap to.

  RETURNS: Float, the remapped value.
  """
  from_min = in_ran[0]
  from_max = in_ran[1]
  to_min = out_ran[0]
  to_max = out_ran[1]

  difference = from_max - from_min
  ratio = (value - from_min) / difference
  
  return float(to_min + ratio * (to_max - to_min))

def openPorts_input(portNum):
    """
    Initializes a MIDI input port

    ARGUMENT: Number of the MIDI input port
    RETURN: Initialized rtmidi.MidiIn object
    """
    try:
        # initialise midi in class
        midi_in = rtmidi.MidiIn()
        # connect to a device
        midi_in.open_port(portNum)
        return midi_in
    except:
        raise f'ERROR. {portNum} must be an already existing MIDI input port'

def openPorts_output(portNum):
    """
    Initializes a MIDI output port

    ARGUMENT: Number of the MIDI output port
    RETURN: Initializedrtmidi.MidiIn object
    """
    try:
        midi_out = rtmidi.MidiOut()
        midi_out.open_port(portNum)
        return midi_out
    except:
        raise f'ERROR. {portNum} must be an already existing MIDI output port'

def input_handler(open_port, t_sleep = 0.001):
        """
        Function which simplifies the use of the rtmidi module.
        Its main use is to be called inside loops, avoiding errors raised when
        None is returned by the rtmidi .get_message() function.

        ARGUMENTS:
        open_port: Input MIDI port creted with rtmidi MidiIn() + .open_port()
            I recommend using the openPorts_input() function in this module.
        
        t_sleep: Timer. When there's no input this function waits with time.sleep().
            Defaulted to 0.001 seconds.
        
        RETURNS: 
        raw_msg: Tuple. Raw input from the .get_message() function.
            It contains "msg" and "dt", dt is the time elapsed
            since the last MIDI message.

        msg: List. Raw input from the .get_message() function.
            It contains all the MIDI information.

        parsed_msg: Return from the parseMessage() function in this module.
            Contains the same information as "raw_msg" but in a dictionary format,
            with easily accesible keys (Channel, Note, Value, Velocity, Command, Delta Time)
        """
        raw_msg = open_port.get_message()
        if raw_msg:
            (msg, dt) = raw_msg
            parsed_msg = msgParse(raw_msg)
            return raw_msg, msg, parsed_msg, dt
        else:
            time.sleep(t_sleep)
    
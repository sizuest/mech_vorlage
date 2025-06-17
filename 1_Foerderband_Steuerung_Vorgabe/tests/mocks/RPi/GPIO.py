# This is a mock for testing RPi-related classes on non-RPi systems

# constants that are used by the encoder; the values are irrelevant for testing
BCM = 1
BOTH = 1
IN = 1
PUD_DOWN = 1

# This variable hold the last callback provided with add_event_detect
stored_callback = None

# This variable holds the input values for the channels:
input_values = {
}

def setwarnings(warnings_on):
    pass


def setmode(mode):
    pass


def setup(pin, direction, **kwargs):
    pass


def add_event_detect(pin, edges, **kwargs):
    if "callback" in kwargs:
        global stored_callback
        stored_callback = kwargs["callback"]


def remove_event_detect(pin):
    pass


def input(channel):
    return input_values[channel]


ticker_counter = 0


def next_edge_on_encoder(encoder, direction="forward"):
    if encoder.input_a in input_values and encoder.input_b in input_values:
        global ticker_counter
        if direction == "forward":
            ticker_counter = (ticker_counter + 1) % 4
        else:
            ticker_counter = (ticker_counter + 3) % 4
        if ticker_counter == 0:
            input_values[encoder.input_a] = 0
            input_values[encoder.input_b] = 0
            stored_callback(encoder.input_a)
        elif ticker_counter == 1:
            input_values[encoder.input_a] = 0
            input_values[encoder.input_b] = 1
            stored_callback(encoder.input_b)
        elif ticker_counter == 2:
            input_values[encoder.input_a] = 1
            input_values[encoder.input_b] = 1
            stored_callback(encoder.input_a)
        elif ticker_counter == 3:
            input_values[encoder.input_a] = 1
            input_values[encoder.input_b] = 0
            stored_callback(encoder.input_b)
    else:
        input_values[encoder.input_a] = 0
        input_values[encoder.input_b] = 0

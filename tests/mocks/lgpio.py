DUMMY_HANDLE = 0

# Modes:
SET_PULL_DOWN = 1

# Alert edges:
BOTH_EDGES = 1

# This variable hold the last callback provided with add_event_detect
stored_callback = None
# This variable holds the input values for the channels:
input_values = {
}


class CallbackWrapper:
    """A simple wrapper that is used to return from the callback() function so
    that it is possible to call cancel() on."""
    def cancel(self):
        pass


def gpiochip_open(_chip):
    return DUMMY_HANDLE


def gpio_claim_input(_chip_handle, _gpio, _mode):
    pass


def gpio_claim_alert(_chip_handle, _gpio, _edges):
    pass


def callback(_chip_handle, _gpio, _edges, callback):
    global stored_callback
    stored_callback = callback
    return CallbackWrapper()


# Testing interface
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
            stored_callback(DUMMY_HANDLE, encoder.input_a, input_values[encoder.input_a], ticker_counter)
        elif ticker_counter == 1:
            input_values[encoder.input_a] = 0
            input_values[encoder.input_b] = 1
            stored_callback(DUMMY_HANDLE, encoder.input_b, input_values[encoder.input_b], ticker_counter)
        elif ticker_counter == 2:
            input_values[encoder.input_a] = 1
            input_values[encoder.input_b] = 1
            stored_callback(DUMMY_HANDLE, encoder.input_a, input_values[encoder.input_a], ticker_counter)
        elif ticker_counter == 3:
            input_values[encoder.input_a] = 1
            input_values[encoder.input_b] = 0
            stored_callback(DUMMY_HANDLE, encoder.input_b, input_values[encoder.input_b], ticker_counter)
    else:
        input_values[encoder.input_a] = 0
        input_values[encoder.input_b] = 0

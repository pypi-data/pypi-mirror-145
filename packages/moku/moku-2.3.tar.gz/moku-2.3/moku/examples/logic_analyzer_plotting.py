#
# moku example: Basic Logic Analyzer
#
# This example demonstrates how you can configure the Logic
# Analyzer instrument to retrieve a single frame of data for 
# all 16 channels
#
# (c) 2021 Liquid Instruments Pty. Ltd.
#
from moku.instruments import LogicAnalyzer

# Connect to your Moku by its ip address using
# LogicAnalyzer('192.168.###.###')
# or by its serial number using
# LogicAnalyzer(serial=123)
i = LogicAnalyzer('192.168.###.###')

try:
    # Configure the Logic Analyzer pins
    # Pin 1 as output
    # Pin 2 as High
    # Pin 3 as Low
    # Pin 4 as Input
    pin_config = [{"pin": 1, "state": "O"}, {"pin": 2, "state": "H"},
                  {"pin": 3, "state": "L"}, {"pin": 4, "state": "I"}]

    i.set_pins(pin_config)

    # Pin 5 turned off
    i.set_pin(5, "X")

    # Configure the output pattern for Pin 1
    i.generate_pattern(1, [1, 0, 0, 0, 0, 0, 0, 0])

    # Start the output on all pins that are set as output
    i.start_all()

    # Collect a frame of data from all 16 pins
    data = i.get_data()

    print(data)

except Exception as e:
    raise e
    # print(f'Exception occurred: {e}')

finally:
    # Close the connection to the Moku device
    # This ensures network resources and released correctly
    i.relinquish_ownership()

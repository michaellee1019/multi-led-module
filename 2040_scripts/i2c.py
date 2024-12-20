from smbus2 import SMBus, i2c_msg
import json

# Initialize the I2C bus
bus_number = 1  # Use 1 for I2C-1 on most Raspberry Pi models
i2c_address = 0x40  # Replace with your device's I2C address

def divide_chunks(l, n):
    
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

# Open the I2C bus
with SMBus(bus_number) as bus:
    # # Write a single byte to a device
    register = 0x00  # Register to write to
    # data = 0xFF      # Data to write
    # bus.write_byte_data(i2c_address, register, data)
    # print(f"Wrote byte {hex(data)} to register {hex(register)} at address {hex(i2c_address)}")

    # # Write a block of data to a device
    # block_data = [0x12, 0x34, 0x56]  # Data to send

    # Write raw data using `i2c_msg` for more control
    raw_data = {1: {"set_animation": "blink", "color": "red", "speed": 0.2}}
    # raw_data = {"hello": "world"}
    byte_string = json.dumps(raw_data).encode("utf-8")
    chunks = divide_chunks(byte_string, 32)
    for chunk in chunks:
        bus.write_i2c_block_data(i2c_address, register, chunk)
        print(f"Wrote block {chunk} to register {hex(register)}")

    # msg = i2c_msg.write(i2c_address, byte_string)
    # bus.i2c_rdwr(msg)
    # print(f"Sent raw data {raw_data} to device at address {hex(i2c_address)}")

import json

# Initialize the I2C bus
bus_number = 1  # Use 1 for I2C-1 on most Raspberry Pi models
i2c_address = 0x40  # Replace with your device's I2C address

def divide_chunks(l, n):
    
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


raw_data = {1: {"set_animation": "blink", "color": "red", "speed": 0.2}}
byte_string = json.dumps(raw_data).encode("utf-8")
chunks = divide_chunks(byte_string, 32)

full_msg = bytearray()
for chunk in chunks:
    full_msg.extend(chunk)
    
reconstructed_message = full_msg.decode()
unserialized = json.loads(reconstructed_message)
print(unserialized)
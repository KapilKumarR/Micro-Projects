def name_to_binary(name):
    binaryArray = ""
    for char in name:
        binaryCH = bin(ord(char))[2:].zfill(8)
        binaryArray += binaryCH  # Append each 8-bit binary to the full binaryArray
    return binaryArray

def BraceletSequence(binaryArray):
    # Dictionary to map binary bits to colors
    table = {'0': 'Black', '1': 'White'}
    sequence = [f"{index}: {table[bit]}" for index, bit in enumerate(binaryArray, start=1)]
    return sequence 

def display_bracelet(name):
    # Convert the name to binary
    binaryArray = name_to_binary(name)
    count_ones = binaryArray.count('1')
    count_zeros = binaryArray.count('0') 
    # Display information
    print(f"Binary representation of '{name}': {binaryArray}")
    print(f"Number of '1's (Black): {count_ones}")
    print(f"Number of '0's (White): {count_zeros}")
    # convert str into binary and display
    text_pattern = BraceletSequence(binaryArray)
    # to print each item in newline
    print(f"Bracelet pattern (text): {text_pattern}")
    for item in text_pattern:
        print(item) 

while True:
    name_input = input("Enter your name: ")
    display_bracelet(name_input)
    choice = input("\nPress any key to continue Program:\nPress 0 for EXIT:\n")
    if choice == '0':
        print("Exit")
        break 
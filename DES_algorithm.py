import textwrap

pt = input("enter 64 bit plain text:")
key = input("enter 64 bit key:")
sbox_count = input("enter sbox to be used for encryption:")

# Table of Position of 64 bits at initial level: Initial Permutation Table
initial_permu = [58, 50, 42, 34, 26, 18, 10, 2,
                 60, 52, 44, 36, 28, 20, 12, 4,
                 62, 54, 46, 38, 30, 22, 14, 6,
                 64, 56, 48, 40, 32, 24, 16, 8,
                 57, 49, 41, 33, 25, 17, 9, 1,
                 59, 51, 43, 35, 27, 19, 11, 3,
                 61, 53, 45, 37, 29, 21, 13, 5,
                 63, 55, 47, 39, 31, 23, 15, 7]

# Expansion P-box Table
exp_p = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]

# Straight Permutation Table
per = [16, 7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2, 8, 24, 14,
       32, 27, 3, 9,
       19, 13, 30, 6,
       22, 11, 4, 25]

# S-box Table
SBOX = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

# --parity bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]


# Subkey generation and Rounding
def apply_PC1(pc1_table, keys_64bits):
    """ This function takes Permutation table and initial key as input and return 56 bits key as output"""
    keys_56bits = ""
    for index in pc1_table:
        keys_56bits += keys_64bits[index - 1]
    # Python list index start with 0
    # so index -1 will cover the difference between the index
    return keys_56bits


keys_56bits = apply_PC1(keyp, key)


def split_in_half(key_56bits):
    """ Split the 56 bits key into two equal half """
    left_keys, right_keys = key_56bits[:28], key_56bits[28:]
    return left_keys, right_keys


left56, right56 = split_in_half(keys_56bits)


def circular_left_shift(bits, number_of_bits):
    """This method will circularly shift the given bit string according to the number of bits"""
    shifted_bits = bits[number_of_bits:] + bits[:number_of_bits]
    return shifted_bits


circularShiftedBits = circular_left_shift(bits, number_of_bits)


def apply_PC2(pc2_table, key_56bits):
    """ This will take Compression table and combined both half as input and return a 48-bits string as output"""
    keys_48bits = ""
    for index in pc2_table:
        keys_48bits += key_56bits[index - 1]
    return keys_48bits


subkey = apply_PC2(key_comp, left56 + right56)


def generate_keys(key_64bits):
    round_keys = list()
    pc1_out = apply_PC1(keyp, key_64bits)
    L0, R0 = split_in_half(pc1_out)
    for roundnumber in range(16):
        newL = circular_left_shift(L0, shift_table[roundnumber])
        newR = circular_left_shift(R0, shift_table[roundnumber])
        roundkey = apply_PC2(key_comp, newL + newR)
        round_keys.append(roundkey)
        L0 = newL
        R0 = newR
    return round_keys


sub_keys = generate_keys(key)
# The sub_keys will have all 16 keys as Python list
print(sub_keys)


def split_in_half2(pt_64bits):
    """ Split the 56 bits key into two equal half """
    left_keys, right_keys = pt_64bits[:32], pt_64bits[32:]
    return left_keys, right_keys


left64, right64 = split_in_half2(pt)


def apply_Expansion(expansion_table, bits_32):
    """ This will take expansion table and 32-bit binary string as input and output a 48-bit binary stirng"""
    bits48 = ""
    for index in expansion_table:
        bits48 += bits_32[index - 1]
    return bits48


bits32 = right64
out_bits48 = apply_Expansion(exp_p, bits32)
print(out_bits48)


def XOR(bits1, bits2):
    """perform a XOR operation and return the output"""
    # Assuming both bit string of same length
    xor_result = ""
    for index in range(len(bits1)):
        if bits1[index] == bits2[index]:
            xor_result += '0'
        else:
            xor_result += '1'
    return xor_result


print(XOR(sub_keys[0], out_bits48))


# s boxes computations

def split_in_6bits(XOR_48bits):
    """split 48 bits into 6 bits each """
    list_of_6bits = textwrap.wrap(XOR_48bits, 6)
    return list_of_6bits


# Below are some supportive function used for smooth the process

def get_first_and_last_bit(bits6):
    """Return first and last bit from a binary string"""
    twobits = bits6[0] + bits6[-1]
    return twobits


def get_middle_four_bit(bits6):
    """Return first and last bit from a binary string"""
    fourbits = bits6[1:5]
    return fourbits


def binary_to_decimal(binarybits):
    """ Convert binary bits to decimal"""
    # helps during list access

    decimal = int(binarybits, 2)
    return decimal


def decimal_to_binary(decimal):
    """ Convert decimal to binary bits"""
    binary4bits = bin(decimal)[2:].zfill(4)
    return binary4bits


def sbox_lookup(sboxcount, first_last, middle4):
    """ take three parameter and access the Sbox accordingly and return the value"""
    d_first_last = binary_to_decimal(first_last)
    d_middle = binary_to_decimal(middle4)

    sbox_value = SBOX[sboxcount][d_first_last][d_middle]
    return decimal_to_binary(sbox_value)


# Example:
bits6 = '100000'
first_last = get_first_and_last_bit(bits6)  # '10' -> 2
middle4 = get_middle_four_bit(bits6)  # '0000' -> 0

# suppose we are processing the first 6-bit so the sbox number will be sboxcount = 1
result = sbox_lookup(sbox_count, first_last, middle4)


def apply_Permutation(permu_table, sbox_32bits):
    """ It takes Sboxes output and a permutation table and return 32 bit binary string"""
    final_32bits = ""
    for index in permu_table:
        final_32bits += sbox_32bits[index - 1]
    return final_32bits


def functionF(pre32bits, key48bits):
    """This is main function to perform function F """
    results = ""
    expanded_left_half = apply_Expansion(exp_p, pre32bits)
    xor_value = XOR(expanded_left_half, key48bits)
    bits6list = split_in_6bits(xor_value)
    for sboxcount, bits6 in enumerate(bits6list):
        first_last = get_first_and_last_bit(bits6)
        middle4 = get_middle_four_bit(bits6)
        sboxvalue = sbox_lookup(sboxcount, first_last, middle4)
        results += sboxvalue
    final32bits = apply_Permutation(per, results)
    return final32bits


HEX_to_Binary = {'0': '0000',
                 '1': '0001',
                 '2': '0010',
                 '3': '0011',
                 '4': '0100',
                 '5': '0101',
                 '6': '0110',
                 '7': '0111',
                 '8': '1000',
                 '9': '1001',
                 'A': '1010',
                 'B': '1011',
                 'C': '1100',
                 'D': '1101',
                 'E': '1110',
                 'F': '1111',
                 }


def hexDigit_to_binary_bits(hex_digit):
    binary_4bits = HEX_to_Binary[hex_digit]
    return binary_4bits


def hexString_to_binary_bits1(hex_string):
    binary_bits = ""
    for hex_digit in hex_string:
        binary_bits += hexDigit_to_binary_bits(hex_digit)
    return binary_bits


def hexString_to_binary_bits2(hexdigits):
    binary_digits = ""
    for hex_digit in hexdigits:
        binary_digits += bin(int(hex_digit, 16))[2:].zfill(4)
    return binary_digits


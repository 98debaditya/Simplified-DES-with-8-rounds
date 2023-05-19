# Python3 code for 32bit Simplified DES with 8 rounds

# Hexadecimal to binary conversion
def hex2bin(s): #For 32bit
	return bin(int(('0x'+s), 16))[2:].zfill(32)
def hex2bin24(s): #For 24bit
	return bin(int(('0x'+s), 16))[2:].zfill(24)

# Binary to hexadecimal conversion
def bin2hex16(s): #For 16bit
	return hex(int(('0b'+s), 2))[2:].zfill(4).upper()
def bin2hex32(s): #For 32bit
	return hex(int(('0b'+s), 2))[2:].zfill(8).upper()
def bin2hex24(s): #For 24bit
	return hex(int(('0b'+s), 2))[2:].zfill(6).upper()

# Binary to decimal conversion
def bin2dec(binary):
	return int(str(binary),2)

# Decimal to binary conversion
def dec2bin(num):
	return bin(int(str(num),10))[2:].zfill(4)

# Permute function to rearrange the bits
def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + k[arr[i] - 1]
    return permutation

# shifting the bits towards left by nth shifts
def shift_left(k):
    return k[1:] + k[0]

# string XOR operation
import bitarray
def xor(a, b):
    ba1 = bitarray.bitarray(a)
    ba2 = bitarray.bitarray(b)
    result = ba1 ^ ba2
    return result.to01()

# Table of Position of 32 bits at initial level: Initial Permutation Table
initial_perm = [7,11,23,29,14,19,5,27,
                13,6,24,30,15,20,2,10,
                28,17,1,32,21,3,22,25,
                4,26,9,31,8,12,16,18]

# Expansion D-box Table
exp_d = [1, 2, 3, 4, 5, 4,
         5, 6, 7, 8, 9, 8,
         9,10,11,12,13,12,
         13,14,15,16,16,1]
 
# Straight Permutation Table
per = [16,7,12,1,
	   15,5,10,2,
	   8,14,3,9,
	   13,6,11,4]
 
# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
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
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]]

# Final Permutation Table
final_perm = [19,15,22,25,7,10,1,29,
              27,16,2,30,9,5,13,31,
              18,32,6,14,21,23,3,11,
              24,26,8,17,4,12,28,20]

def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)
    # Initial Permutation
    pt = permute(pt, initial_perm, 32)
    print("After initial permutation", bin2hex32(pt))
    # Splitting
    left = pt[0:16]
    right = pt[16:32]
    for i in range(0, 8):
        #  Expansion D-box: Expanding the 16 bits data into 24 bits
        right_expanded = permute(right, exp_d, 24)
        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])
        # S-boxex: substituting the value from s-box table by calculating row and column
        sbox_str = ""
        for j in range(0, 4):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)
        # Straight D-box: After substituting rearranging the bits
        sbox_str = permute(sbox_str, per, 16)
        # XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result
        # Swapper
        if(i != 7):
            left, right = right, left
        print("Round ", i + 1, " ", bin2hex16(left),
              " ", bin2hex16(right), " ", rk[i])
    # Combination
    combine = left + right
    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm, 32)
    return cipher_text

pt = "A65FB32D"
key = "8DFA19"
print('Origianl plain text: ',pt)
print('Key: ', key)

# Key generation
key = hex2bin24(key) # --hex to binary

# Splitting
left = key[0:12]
right = key[12:24]

rkb = [] # rkb for RoundKeys in binary
rk = [] # rk for RoundKeys in hexadecimal
for i in range(0, 8):
    # Shifting the bits by nth shifts by checking from shift table
    left = shift_left(left)
    right = shift_left(right)
    # Combination of left and right string
    round_key = left + right
    rkb.append(round_key)
    rk.append(bin2hex24(round_key))

print("Encryption")
cipher_text = bin2hex32(encrypt(pt, rkb, rk))
print("Cipher Text : ", cipher_text)

print("Decryption")
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]
text = bin2hex32(encrypt(cipher_text, rkb_rev, rk_rev))
print("Plain Text after Decryption: ", text)





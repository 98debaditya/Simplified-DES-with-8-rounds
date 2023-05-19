def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans
print(xor('111','101'))
def dec2bin(num):
	return bin(int(str(num),10))[2:].zfill(4)
def xor1(a, b):
	return dec2bin(int(a,2)^int(b,2))
print(type(xor1('111','101')))

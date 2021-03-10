import hashlib

def hash(username):
	result = 0xfacc0fff
	for e in username:
		current = result^(e & 0xFF)
		last_byte = (current & 0xff000000) >> 24
		current = (current << 8) + last_byte

def hastToString(hashh):
	string = ""
	for i in range(8):
		lastBits = hashh & 0xF
		hashh >>=  4
		if lastBits > 9:
			lastBits = 9
		string = string(lastBits)
	return string

def twoscomplement_to_unsigned(i):
    return i % 256

def inverseHashString(hashString):
	invHash = bytes(map(twoscomplement_to_unsigned, b))
	invHash = hashString.length()
	#bytes([]) invHash= new bytes([hashString.length()])
	for i in range(hashString.length()):
		current = hashString[i] & 0xFFFF
		current = ~current
		invHash[i] = (bytes) (current & 0xFF)
	return invHash

def main():
	username = "restarxxt"
	usrnm = str(username)
	usrnm = hashlib.sha1(username.encode())
	password = str(usrnm.hexdigest())
	print("Calculated password to type in: " + password)

if __name__ == "__main__":
    main()
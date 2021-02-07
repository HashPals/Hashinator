import binascii, hashlib, ujson

# TODO Change this file nme to the one you're working on
filename = "500-worst-passwords.txt"


# TODO add more hashing methods if ya find them
def md5(text):
    return hashlib.md5(text).hexdigest().strip(), "MD5"

def sha1(text):
    return hashlib.sha1(text).hexdigest().strip(), "SHA-1"

def sha256(text):
    return hashlib.sha256(text).hexdigest().strip(), "SHA-256"

def sha512(text):
    return hashlib.sha512(text).hexdigest().strip(), "SHA-512"

def sha384(text):
    return hashlib.sha384(text).hexdigest().strip(), "SHA-384"

def sha224(text):
    return hashlib.sha224(text).hexdigest().strip(), "SHA-224"

def ntlm(text):
    return binascii.hexlify(hashlib.new('md4', text.decode("utf-8").encode('utf-16le')).digest()), "NTLM"




with open(filename) as f:
    content = f.read().splitlines()

hashing = [md5, sha1, sha256, sha512, sha384, sha224, ntlm]
output = []

for i in content:
    plaintext = bytes(i, "utf-8").strip()
    for hash in hashing:
        to_insert = hash(plaintext)
        hashed_value = to_insert[0]
        if not isinstance(hashed_value, str):
            try:
                hashed_value = hashed_value.decode("utf-8")
            except:
                continue
        output.append({"Hash": to_insert[0], "Plaintext": i, "Type": to_insert[1], "Verified": True})


new_filename = filename.split(".")[0]

with open(new_filename + ".json", 'w') as outfile:
    ujson.dump(output, outfile, reject_bytes=False)
    

# -*- coding: iso-8859-15 -*-

import binascii
import hashlib
import re
import ujson
import os
import dynamo_json
import time
import boto3
import random

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table("hash_lookup")
escapes = ''.join([chr(char) for char in range(1, 32)])

# TODO Change this file name to the one you're working on
# path = input("Enter file path --> ")
path = "/mnt/e/Hashinator"
# Basically all puncuation, lowercase, uppercaese, numbers, emails, etc.
# Removes Asian characters, emojis, etc etc.
regexp = re.compile(r"""^[A-Za-z.\s_@"!£$%^&*(){}#~';:?>.<,|\/\][0123456789+=\-_-]+$""")


# TODO Add more hashing methods if ya find them
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
    # BUG this might be a bit weird, NTLM hashes are typically uppercase. Please triple check your NTLMs :)
    text = text.decode("utf-8")
    hash = hashlib.new("md4", text.encode("utf-16le")).digest()
    return binascii.hexlify(hash).upper(), "NTLM"




hashing = [md5, sha1, sha256, sha512, ntlm, sha384, sha224]
text_files = [f for f in os.listdir(path) if f.endswith('.txt')]
random.shuffle(text_files)
counter = 0
print_counter = 0
total = 0
for text_file in text_files:
    output = {}
    with open(text_file, 'rb') as f:
        content = f.read().splitlines()

    debug = False

    for i in content:
        # If it is "weird" do not add it to the DB.
        try:
            i = i.decode("utf-8")
        except:
            continue

        i = i.translate(escapes)
        i = i.replace("\n", "").replace("\t", "").replace("\r", "")

        if len(i) <= 3:
            continue
        if len(i) >= 20:
            continue
        if not regexp.search(i):
            continue
        if "\t" in i:
            continue
        if "\\x" in i:
            continue
        plaintext = bytes(i, "utf-8").strip()
        for hash in hashing:
            to_insert = hash(plaintext)
            hashed_value = to_insert[0]
            if not isinstance(hashed_value, str):
                try:
                    hashed_value = hashed_value.decode("utf-8")
                except Exception:
                    continue

            output_add = {
                    "Hash": hashed_value.strip(),
                    "Plaintext": i.strip(),
                    "Type": to_insert[1],
                    "Verified": True,
                }

            
            table.put_item(Item=output_add)
            print_counter += 1
            if print_counter >= 100:
                print("100 items processed")
                total += print_counter
                print_counter = 0
                print(f"**** Total is {total}")
    os.remove(text_file)
print("I am done!")

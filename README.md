1. Install UJSON `pip3 install ujson`
2. Edit the filename in hasinator
3. Go to S3
4. Select the file to upload
5. Click "advanced"
6. Find storage-class
7. Click "intelligent-tiering"
8. Click upload
9. Wait a couple seconds
10. Should be in DB, query the API :D

Note: If plaintext is not UTF-8 it is basically ignored.

You can add and remove hash types by removing or adding them to this list:

```
hashing = [md5, sha1, sha256, sha512, ntlm]
```

We do not have SHA-224 and SHA-384 by default. To add them:

```
hashing = [md5, sha1, sha256, sha512, ntlm, sha224, sha384]
```

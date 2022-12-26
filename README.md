# Stidium

## Description
Python based ransomware that uses Symmetric key encryption (AES), Believe it or not I made the first version under 24 hours (So expect the code to be messy). It has stuff like a normal ransomware do, a list of encrypted files, the amount, the btc address to pay, decryptor, and it saves even after restart. This code is tested per piece so I am not sure if it works but theoritically it should. **This version is still not production ready.**

`main.py` might be out of date compared to `main - development.py`, this is not because I forgot about it. It is just me still trying to find a reason to do a 5 min work that I could do right now instead of postponing it. (P.S. Just remove most `"""` and some `#` at the end you'd be good to go)
CURRENT STATUS: **main.py is outdated**

This project is for educational purposes only to show how would a ransomware possibly work and encrypt your data

## TODO
- [ ] Test it on a VM
- [ ] Finish up `post-infect` function that infects it with [Project Gideon](https://github.com/Not-Baguette/Project-Gideon/)
- [X] fix it so it doesnt quit before decrypting all files
- [x] Fix first run issue
- [ ] Check if the amount of files are actually real later
- [ ] Fix the grammar error on the label
- [ ] Make a 128 long random string as the name incase the user uses `taskkill /f` (Which still doesn't decrypt the file though)

## Preview
![image](https://user-images.githubusercontent.com/94969176/209453408-bd16a293-23e2-43e0-8f96-29de4b4069dd.png)

## Dependencies
- tkinter (for the ransomware demand screen)
- cryptography (To encrypt and decrypt)

## Installation
TBD
### For developers
- Get 2 burner emails
- Put it on `SENDER` and `RECEIVER` variable on the top

![image](https://user-images.githubusercontent.com/94969176/209453494-5b28cf52-523c-4ffa-9ff8-4d07c4d9a6b6.png)
- Get an app password for the `SENDER` email
- Install dependencies modules
- remove the commented out encryptor, decryptor, and find_file function alongside the function call on the bottom for inserting to startup and sending via email (I heavily advice against removing the commented out tkinter attributes and configs)
- Change the BTC address to your own (Unnecessary if you just want a preview)

## More information (Nice to know basis)
- `file header encryptor & decryptor.py` is another way to encrypt a file, instead of encrypting the whole file, it encrypts just the header.

- This uses `AES (Advanced Encryption Standard)` algorithm to encrypt but I suggest you look at other algs like `RSA (Rivest-Shamir-Adleman)`, `Blowfish`, `Twofish`, `3DES (Triple DES)`, and `Serpent`. I might consider to move to Blowfish or Twofish for it's speed but we'll see

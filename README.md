# Stidium

## Description
Python based ransomware that uses Symmetric key encryption, Believe it or not I made the first version under 24 hours (So expect the code to be messy). It has stuff like a normal ransomware do, a list of encrypted files, the amount, the btc address to pay, decryptor, and it saves even after restart.

This code is tested per piece so I am not sure if it works but theoritically it should. **This version is still not production ready.**

`main.py` might be out of date compared to `main - development.py`, this is not because I forgot about it. It is just me still trying to find a reason to do a 5 min work that I could do right now instead of postponing it. (P.S. Just remove most `"""` and some `#` at the end you'd be good to go)

## TODO
- [ ] Test it on a VM
- [ ] Finish up `post-infect` function that infects it with [Project Gideon](https://github.com/Not-Baguette/Project-Gideon/)
- [X] fix it so it doesnt quit before decrypting all files
- [x] Fix first run issue
- [ ] Check if the amount of files are actually real later

## Preview
![image](https://user-images.githubusercontent.com/94969176/209453408-bd16a293-23e2-43e0-8f96-29de4b4069dd.png)

## Dependencies
- tkinter (for the ransomware demand screen)
- cryptography (To encrypt and decrypt)

## Installation
TBD

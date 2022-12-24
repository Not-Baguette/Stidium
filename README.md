# Stidium

## Description
Python based ransomware that uses Symmetric key encryption, Believe it or not I made it under 24 hours (So expect the code to be messy). It has stuff like a normal ransomware do, a list of encrypted files, the amount, the btc address to pay, decryptor, and it saves even after restart.

This code is tested per piece so I am not sure if it works but theoritically it should. **This version is still not production ready.**

## TODO
- [ ] Test it on a VM
- [ ] Finish up `post-infect` function that infects it with [Project Gideon](https://github.com/Not-Baguette/Project-Gideon/)
- [X] fix it so it doesnt quit before decrypting all files
- [x] Fix first run issue

## Dependencies
- tkinter (for the ransomware demand screen)
- cryptography (To encrypt and decrypt)

## Installation
TBD

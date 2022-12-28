# Tests

## Description
This folder is filled with comparisons between other algorithms, this can differentiate wildly depending on the PC too. Make sure they have their own folder else tons of `txt` files will appear on the directory. this is a redo because of the faulty tests in older readme.md file

## Todo
- [ ] instead of making seperate files, just make one file that contain all the algs and let the user pick
- [X] Auto clean the directory

## Dependencies
- pycryptodomex
- cryptography

## How to use
Open up `generator.py` and change `range(1000):` to any number you want `e.g. range(10):` will output 10 files on *current directory*, so make sure to put it on a folder for itself (It also will encrypt and decrypt any other `txt` files on that directory if you have). After that, open up a comparator to compare both algs.

## Protocol to test
The protocol is personal, you dont need to follow it.
- Change the files every test
- Stop indexing ASAP

#### 10,000 files - 1024 bytes each (1.0 KB)

TBA

- Blowfish Encryption time:  Seconds
- Blowfish Decryption time:  Seconds
- AES Encryption time:  Seconds
- AES Encryption time:  Seconds

Conclusion: Blowfish is far better than AES when presented with huge amount of files, which is what we need. And doing it to 100,000 files is not good. But AES seems to perform better at smaller amount of files. More testing needed to validate the data. Also I noticed alot of files come out still somewhat corrupted, Might be faulty Blowfish algorithm on my part

## Results
These results are *relative*, they are just for documentation purposes only.

### AES vs Blowfish
#### 100,000 files - 1024 bytes each (1.0 KB)

TBA

- Blowfish Encryption time:  Minutes
- Blowfish Decryption time:  Minutes
- AES Encryption time:  Minutes
- AES Encryption time:  Minutes

## Twofish vs Blowfish

#### 10,000 files -  1024 bytes each (1.0 KB) - First test

![image](https://user-images.githubusercontent.com/94969176/209753715-db48e3d8-f7e0-4ed5-86a5-6a46d984730a.png)

- Twofish Encryption time: 15 Seconds
- Twofish Decryption time: 14 Seconds
- Blowfish Encryption time: 13 Seconds
- Blowfish Encryption time: 13 Seconds

Conclusion: Twofish is approximately 3 seconds slower but it is too small to take any definitive results.

#### 10,000 files -  1024 bytes each (1.0 KB) - Second test

![image](https://user-images.githubusercontent.com/94969176/209754315-45a9b67c-cb79-43a9-ac64-94e79a209c7b.png)

- Twofish Encryption time: 13 Seconds
- Twofish Decryption time: 12 Seconds
- Blowfish Encryption time: 12 Seconds
- Blowfish Encryption time: 12 Seconds

Conclusion: Twofish is approximately 1 seconds slower but it is even small to take any definitive results.

#### 100,000 files -  1024 bytes each (1.0 KB)

ONGOING

- Twofish Encryption time:  Minutes
- Twofish Decryption time:  Minutes
- Blowfish Encryption time:  Minutes
- Blowfish Encryption time:  Minutes

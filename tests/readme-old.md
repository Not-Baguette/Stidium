# Tests

## Description
This folder is filled with comparisons between other algorithms, this can differentiate wildly depending on the PC too. Make sure they have their own folder else tons of `txt` files will appear on the directory

## Todo
- [ ] instead of making seperate files, just make one file that contain all the algs and let the user pick
- [X] Auto clean the directory

## Dependencies
- pycryptodomex
- cryptography

## How to use
Open up `generator.py` and change `range(1000):` to any number you want `e.g. range(10):` will output 10 files on *current directory*, so make sure to put it on a folder for itself (It also will encrypt and decrypt any other `txt` files on that directory if you have). After that, open up a comparator to compare both algs.

## Results
These results are *relative*, they are just for documentation purposes only.

### AES vs Blowfish
#### 100,000 files - 1024 bytes each (1.0 KB)

![image](https://user-images.githubusercontent.com/94969176/209466151-4c896bfd-4be4-496c-9e77-56a618f2817a.png)

- Blowfish Encryption time: 22.86 Minutes
- Blowfish Decryption time: 4.34 Minutes
- AES Encryption time: 43.8 Minutes
- AES Encryption time: 36.73 Minutes

#### 10,000 files - 1024 bytes each (1.0 KB)

![image](https://user-images.githubusercontent.com/94969176/209751930-ce16d278-6e41-48ac-ac9d-194758d258f7.png)

- Blowfish Encryption time: 15 Seconds
- Blowfish Decryption time: 12 Seconds
- AES Encryption time: 13 Seconds
- AES Encryption time: 13 Seconds

Conclusion: Blowfish is far better than AES when presented with huge amount of files, which is what we need. And doing it to 100,000 files is not good. But AES seems to perform better at smaller amount of files. More testing needed to validate the data. Also I noticed alot of files come out still somewhat corrupted, Might be faulty Blowfish algorithm on my part

## Twofish vs Blowfish

#### 10,000 files -  1024 bytes each (1.0 KB)

![image](https://user-images.githubusercontent.com/94969176/209752657-0a159ec6-abdb-4b09-ad7c-80079e79f714.png)

- Twofish Encryption time: 15 Seconds
- Twofish Decryption time: 22 Seconds
- Blowfish Encryption time: 30 Seconds
- Blowfish Encryption time: 12 Seconds

Conclusion: **After the first test, I noticed an oddity at the results, on the Blowfish vs AES test, Blowfish is doing the same amount of files for just 13 seconds, I realized that pycharm indexing might slowed it down severely. it meant most tests up here are relatively faulty. Suggestion to archive and redo this is accepted.**

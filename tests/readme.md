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

Conclusion: Blowfish is far better than AES when presented with huge amount of files, which is what we need. And doing it to 100,000 files is not good. But AES seems to perform better at smaller amount of files. More testing needed to validate the data. Also I noticed alot of files come out still somewhat corrupted, Might be faulty Blowfish algorithm on my part (Update: I tried it with `.pdf`s and it doesnt seem to cause an issue.)

## Results
These results are *relative*, they are just for documentation purposes only.

### AES vs Blowfish
#### 10,000 files - 1024 bytes each (1.0 KB)

TBA

- Blowfish Encryption time:  Seconds
- Blowfish Decryption time:  Seconds
- AES Encryption time:  Seconds
- AES Encryption time:  Seconds

#### 100,000 files - 1024 bytes each (1.0 KB)

![image](https://user-images.githubusercontent.com/94969176/209466151-4c896bfd-4be4-496c-9e77-56a618f2817a.png)

- Blowfish Encryption time: 22.86 Minutes
- Blowfish Decryption time: 4.34 Minutes
- AES Encryption time: 43.8 Minutes
- AES Encryption time: 36.73 Minutes

Conclusion: I have decided that I am going to use the result from `readme.md` as even if it's a little inaccurate, the results are very clear

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

![image](https://user-images.githubusercontent.com/94969176/209772987-3ccd3c08-5ff8-4272-9914-bcc1f33b7c9d.png)

- Twofish Encryption time: 29.11 Minutes
- Twofish Decryption time: 21.67 Minutes
- Blowfish Encryption time: 18.65 Minutes
- Blowfish Encryption time: 21.43 Minutes

Conclusion: `Twofish` is approximately 11 minutes slower but have better security, since we are pretty much looking for fastness, `Blowfish` should be the fastest. The results might be increased because I forgot that my discord, youtube, etc. were open, but since it's a nearly constant thing, it shouldn't matter relative to each another.

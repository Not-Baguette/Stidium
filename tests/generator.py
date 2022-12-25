import os


# generate 100 txt files with random data
def get_random_bytes(n):
    return os.urandom(n)


for i in range(10000):
    with open(str(i+1) + ".txt", "wb") as file:
        file.write(get_random_bytes(1024))
        file.close()

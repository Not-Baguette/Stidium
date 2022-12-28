import os


# generate 100 txt files with random data
def get_random_bytes(n):
    return os.urandom(n)


# delete all txt and enc files
for file in os.listdir():
    if file.endswith(".txt") or file.endswith(".enc"):
        os.remove(file)

print("Previous .txt and .enc Files deleted")

for i in range(10000):
    with open(str(i+1) + ".txt", "wb") as file:
        file.write(get_random_bytes(1024))
        file.close()

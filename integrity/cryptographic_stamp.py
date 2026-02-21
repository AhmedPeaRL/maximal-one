import hashlib
import os

def hash_directory(path):
    sha = hashlib.sha256()
    for root, _, files in os.walk(path):
        for file in sorted(files):
            with open(os.path.join(root, file), 'rb') as f:
                sha.update(f.read())
    return sha.hexdigest()

if __name__ == "__main__":
    digest = hash_directory(".")
    print("Repository integrity hash:", digest)

import os 
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, filename):
    chunkSize = 64*1024 
    outputFile = "{EncryptedFile}"+filename
    fileSize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16) 

    encryptor = AES.new(key, AES.MODE_CBC, IV) 

    with open(filename,'rb') as infile:
        with open(outputFile,'wb') as outfile:
                outfile.write(fileSize.encode('utf-8'))
                outfile.write(IV)

                while True:
                    chunk = infile.read(chunkSize) 
                    if(len(chunk) == 0):
                        break 
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16)) 
                    outfile.write(encryptor.encrypt(chunk))

def decrypt(key,filename):
    chunkSize = 64*1024 
    outputFile = "{DecryptedFile}" + filename[11:]

    with open(filename,'rb') as infile:
        filesize = int(infile.read(16)) 
        IV = infile.read(16)

        decryptor = AES.new(key,AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunkSize) 
                if(len(chunk) == 0):
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8')) 
    return hasher.digest() 

def Main():
    message = input("Encrypt or Decrypt the file ? " )
    if(message == 'e'):
        filename = input("Enter Filename to encrypt ") 
        pwd = input("Enter Password: ")
        encrypt(getKey(pwd),filename)
        print ("Done.")
    elif message == 'd':
        filename = input("Enter Filename to decrypt ") 
        pwd = input("Enter Password: ")
        decrypt(getKey(pwd),filename)
        print ("Done.")


if __name__ == '__main__':
    Main()

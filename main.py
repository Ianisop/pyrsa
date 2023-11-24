import translator

emessage = translator.encrypt("ianis is best", "RSA_demo_pubkey.txt")

print(str(emessage))

a = input("Decrypt?: ")
if a != "":
    bmessage = translator.decrypt(emessage, "RSA_demo_privkey.txt")
    print(str(bmessage))




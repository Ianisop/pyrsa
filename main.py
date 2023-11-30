import translator

emessage = translator.encrypt("microsoft", "_pubkey.txt")

print(str(emessage))

a = input("Decrypt?: ")
if a != "":
    bmessage = translator.decrypt(emessage, "_privkey.txt")
    print(str(bmessage))




def encrypt(text='Hello World',key = 1):
    encrypted = []
    for letter in text:
        i = chr(ord(letter) + key)
        encrypted += i
    encrypted = (''.join(encrypted))
    return(encrypted)
def decryptwithkey(text='ifmmp!xpsme',key = 1):
    decrypted = []
    for letter in text:
        i = chr(ord(letter) - key)
        decrypted += i
    decrypted = (''.join(decrypted))
    return(decrypted)
def decryptwithoutkey(text = 'ifmmp!xpsme',name = 'text.txt',maxkey=256):
    f = open(name,'x')
    num = 1
    while num <= maxkey:
        decrypted = []
        for letter in text:
            a = chr(ord(letter) - num)
            decrypted += a
        decrypted = (str(num)+'.'+''.join(decrypted) + '\n')
        f.write(decrypted)
        num += 1
print(encrypt('hello world',256))
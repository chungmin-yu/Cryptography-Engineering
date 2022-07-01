# -*- coding: utf-8 -*-
letters={}
num=0
for i in range(26):
    letters.update({chr(i+65):0})
cipher=input('ciphertext:')
for i in range(len(cipher)):
    if(cipher[i] == ' ' or cipher[i] == '\t'):
        continue
    tmp=letters[cipher[i]]
    num=num+1
    letters.update({cipher[i]:tmp+1})
for i in range(26):
    percentage = letters[chr(i+65)]/num * 100
    print(chr(i+65)+ ':' +str(letters[chr(i+65)]) +"     "+ str(percentage) + '%')
#print(letters)
#K YZWLNKXKJWGN QUGN ETNMX MPLMZOMXYM K TMMJOXA XEN TKZ ZMQEBMF TZEQ KJKZQ EX KXKJWDOXA KXF MPLJEZM NHM TJEEF ET XMI CXEIJMFAM IHOYH MKYH WMKZ RZOXAG IONH ON
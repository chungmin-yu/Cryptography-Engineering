# -*- coding: utf-8 -*-
import math

vowels=['A', 'E', 'I', 'O', 'U']
ciphertext = "EOEYE GTRNP SECEH HETYH SNGND DDDET OCRAE RAEMHTECSE USIAR WKDRI RNYAR ANUEY ICNTT CEIET US"
plaintext_ref="WITHM ALICE TOWAR DNONE WITHC HARIT YFORA LLWIT HFIRM NESSI NTHER IGHTA SGODG IVESU STOSE ETHER IGHTL ETUSS TRIVE ONTOF INISH THEWO RKWEA REINT OBIND UPTHE NATIO NSWOU NDSTO CAREF ORHIM WHOSH ALLHA VEBOR NETHE BATTL EANDF ORHIS WIDOW ANDHI SORPH ANTOD OALLW HICHM AYACH IEVEA NDCHE RISHA JUSTA NDLAS TINGP EACEA MONGO URSEL VESAN DWITH ALLNA TIONS GREEC EANNO UNCED YESTE RDAYT HEAGR AGREE MENTW ITHTR UKEYE NDTHE CYPRU STHAT THEGR EEKAN DTURK ISHCO NTING ENTSW HICHA RETOP ARTIC IPATE INTHE TRIPA RTITE HEADQ UARTE RSSHA LLCOM PRISE RESPE CTIVE LYGRE EKOFF ICERS NONCO MMISS IONED OFFIC ERSAN DMENA NDTUR KISHO FFICE RSNON COMMI SSION EDOFF ICERS ANDME NTHEP RESID ENTAN DVICE PRESI DENTO FTHER EPUBL ICOFC YPRUS ACTIN GINAG REEME NTMAY REQUE STTHE GREEK ANDTU RKISH GOVER NMENT STOIN CREAS EORRE DUCET HEGRE EKAND TURKI SHCON TINGE NTSIT ISAGR EEDTH ATTHE SITES OFTHE CANTO NMENT SFORT HEGRE EKAND TURKI SHCON TINGE NTSPA RTICI PATIN GINTH ETRIP ARTIT EHEAD QUART ERSTH EIRJU RIDIC ALSTA TUSFA CILIT IESAN DEXEM PTION SINRE SPECT OFCUS TOMSA NDTAX ESASW ELLAS OTHER IMMUN ITIES ANDPR IVILE GESAN DANYO THERM ILITA RYAND TECHN ICALQ UESTI ONSCO NCERN INGTH EORGA NIZAT IONAN DOPER ATION OFTHE HEADQ UARTE RSMEN TIONE DABOV ESHAL LBEDE TERMI NEDBY ASPEC IALCO NVENT IONWH ICHSH ALLCO MEINT OFORC ENOTL ATERT HANTH ETREA TYOFA LLIAN CE"
plaintext_ref = plaintext_ref.replace(' ', '')
plaintext_ref = plaintext_ref.replace('\t', '')
plaintext_ref = plaintext_ref.replace('\n', '')

def train(msg, trigram, bigram):
    for i in range(len(msg)-2):
        if (msg[i:i+3] not in trigram):
            trigram.update({msg[i:i+3]:1})
        else:
            tmp = trigram[msg[i:i+3]]
            trigram.update({msg[i:i+3]:tmp+1})
        if (msg[i:i+2] not in bigram):
            bigram.update({msg[i:i+2]:1})
        else:
            tmp = bigram[msg[i:i+2]]
            bigram.update({msg[i:i+2]:tmp+1})

### training process
trigram={}
bigram={}
train(plaintext_ref, trigram, bigram)
#for i in (sorted(trigram.items(), key=lambda kv: kv[1], reverse=True)):
    #print(i)
#for i in (sorted(bigram.items(), key=lambda kv: kv[1], reverse=True)):
    #print(i)


print("first step: ")
# rectangle 7*11
rect711=[]
idx=0
for i in range(11):
    rect711.append([])
    for j in range(7):
        if(ord(ciphertext[idx]) < 65  or ord(ciphertext[idx]) > 90):
            idx += 1
        rect711[i].append(ciphertext[idx])
        idx += 1
        
print("rectangle 7*11")
diff711=0
for i in range(7):
    vowelNum=0
    for j in range(11):
        if(rect711[j][i] in vowels):
            vowelNum += 1
        print(rect711[j][i], end=' ')
    diff=round(abs(vowelNum - 0.4 * 11), 1)
    diff711 += diff
    print("\tdifference: " + str(diff))
print("average difference: " + str(diff711/7))

# rectangle 11*7
rect117=[]    
idx=0
for i in range(7):
    rect117.append([])
    for j in range(11):
        if(ord(ciphertext[idx]) < 65  or ord(ciphertext[idx]) > 90):
            idx += 1
        rect117[i].append(ciphertext[idx])
        idx += 1  
        
print("\nrectangle 11*7")         
diff117=0
for i in range(11):
    vowelNum=0
    for j in range(7):
        if(rect117[j][i] in vowels):
            vowelNum += 1
        print(rect117[j][i], end=' ')
    diff=round(abs(vowelNum - 0.4 * 7), 1)
    diff117 += diff
    print("\tdifference: " + str(diff))   
print("average difference: " + str(diff117/11))

### according to first step, we know the rectangle's size is 11*7
### we know first three letters are "GRE"
hint=['G', 'R', 'E']
print("\nThe answer is (second step): ")
ansRect=[]
row=0
col=0
if( (diff117/11) < (diff711/7) ):
    ansRect=rect117
    row=11
    col=7
else:
    ansRect=rect711
    row=7
    col=11    

# construct according to hint
for h in range(2):
    for i in range(col):
        if (ansRect[i][0] == hint[h]):
            #swap
            for j in range(row):
                ansRect[i][j], ansRect[h][j] = ansRect[h][j], ansRect[i][j]

# training        
for i in range(col-2):
    #test column
    change=i+2
    Pr=0
    for k in range(i+2, col):
        prob=0
        for j in range(row):
            word2=ansRect[i][j]+ansRect[i+1][j]
            word3=word2+ansRect[k][j]
            if ((word2 not in bigram) or (word3 not in trigram)):
                prob += 0
            else:
                prob += math.log(26*(trigram[word3]/bigram[word2]))
        if(prob>Pr):
            Pr = prob
            change = k
    #swap column
    for j in range(row):
        ansRect[i+2][j], ansRect[change][j] = ansRect[change][j], ansRect[i+2][j]

# print answer
for j in range(row):
    for i in range(col):
        print(ansRect[i][j], end=' ')
    print()
            





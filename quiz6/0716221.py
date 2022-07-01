#!/bin/python

import string
import math
import random

character="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
def pruning(msg):
    msg=msg.strip().upper()
    msg_list = []
    for i in range(len(msg)):
        if msg[i] in character:
            msg_list.append(msg[i])
        else:
            msg_list.append(' ')
    new_msg = ''.join(msg_list)
    return new_msg

def create_cipher_dict(key):
    cipher_dict = {}
    alphabet_list = list(string.ascii_uppercase)
    for i in range(len(key)):
        cipher_dict[alphabet_list[i]] = key[i]

    return cipher_dict

def encrypt(text, key):
    cipher_dict = create_cipher_dict(key)
    text = list(text)
    newtext = ""
    for elem in text:
        if elem.upper() in cipher_dict:
            newtext += cipher_dict[elem.upper()]
        else:
            newtext += " "
    return newtext

# This function takes input as a path to a long text and creates scoring_params dict which contains the
# number of time each pair of alphabet appears together
# Ex. {'AB':234,'TH':2343,'CD':23 ..}
# Note: Take whitespace into consideration

def create_scoring_params_dict(longtext_path):
    #TODO
    #pass
      
    with open(longtext_path,'r', encoding="utf-8") as f:
        ref_text = f.read()
        
    bigrams={}
    ref_text = pruning(ref_text)    
    for i in range(len(ref_text)-1):
        if (ref_text[i:i+2] not in bigrams):
            bigrams.update({ref_text[i:i+2]:1})
        else:
            tmp = bigrams[ref_text[i:i+2]]
            bigrams.update({ref_text[i:i+2]:tmp+1})
    return bigrams

# This function takes input as a text and creates scoring_params dict which contains the
# number of time each pair of alphabet appears together
# Ex. {'AB':234,'TH':2343,'CD':23 ..}
# Note: Take whitespace into consideration

def score_params_on_cipher(text):
    #TODO
    #pass
    bigrams={}
    text=pruning(text)    
    for i in range(len(text)-1):
        if (text[i:i+2] not in bigrams):
            bigrams.update({text[i:i+2]:1})
        else:
            tmp = bigrams[text[i:i+2]]
            bigrams.update({text[i:i+2]:tmp+1})
    return bigrams

# This function takes the text to be decrypted and a cipher to score the cipher.
# This function returns the log(score) metric

def get_cipher_score(text,cipher,scoring_params):
    #TODO
    #pass
    decrypted_text=encrypt(text, cipher)
    train_params=score_params_on_cipher(decrypted_text)
    
    tmp_score=0
    for param in train_params:
        if param not in scoring_params:
            continue
        else:
            base=scoring_params[param]
            power=train_params[param]
            # get log of socre
            #tmp_score = tmp_score * pow(base, power)
            tmp_score += power * math.log(base)
     
    return tmp_score

# Generate a proposal cipher by swapping letters at two random location
def generate_cipher(cipher):
    #TODO
    #pass
    loc1=random.randint(0,25)
    loc2=random.randint(0,25)
    while loc1 == loc2:
        loc2=random.randint(0,25)
    if loc1<loc2:
        new_cipher=cipher[:loc1]+cipher[loc2]+cipher[loc1+1:loc2]+cipher[loc1]+cipher[loc2+1:]
    else:
        new_cipher=cipher[:loc2]+cipher[loc1]+cipher[loc2+1:loc1]+cipher[loc2]+cipher[loc1+1:]
    return new_cipher

# Toss a random coin with robability of head p. If coin comes head return true else false.
def random_coin(p):
    #TODO
    #pass
    coin = random.uniform(0,1)
    if coin>=p:
        return False
    else:
        return True

# Takes input as a text to decrypt and runs a MCMC algorithm for n_iter. Returns the state having maximum score and also
# the last few states
def MCMC_decrypt(n_iter,cipher_text,scoring_params):
    current_cipher = string.ascii_uppercase # Generate a random cipher to start
    best_state = ''
    score = 0
    for i in range(n_iter):
        proposed_cipher = generate_cipher(current_cipher)
        score_current_cipher = get_cipher_score(cipher_text,current_cipher,scoring_params)
        score_proposed_cipher = get_cipher_score(cipher_text,proposed_cipher,scoring_params)
        try:
            acceptance_probability = min(1,math.exp(score_proposed_cipher-score_current_cipher))
        except OverflowError:
            acceptance_probability = 1
        if score_current_cipher>score:
            best_state = current_cipher
        if random_coin(acceptance_probability):
            current_cipher = proposed_cipher
        if i%500==0:
            print("iter",i,":",encrypt(cipher_text,current_cipher)[0:99])
    return best_state

def main():
    ## Run the Main Program:

    scoring_params = create_scoring_params_dict('war_and_peace.txt')

    with open('ciphertext.txt','r') as f:
        cipher_text = f.read()
    print(cipher_text)

    print("Text To Decode:", cipher_text)
    print("\n")
    best_state = MCMC_decrypt(10000,cipher_text,scoring_params)
    print("\n")
    plain_text = encrypt(cipher_text,best_state)
    print("Decoded Text:",plain_text)
    print("\n")
    print("MCMC KEY FOUND:",best_state)

    with open('plaintext.txt','w+') as f:
        f.write(plain_text)


if __name__ == '__main__':
    main()

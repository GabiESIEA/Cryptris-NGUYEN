from ctypes import sizeof
import random
import numpy as np
import msvcrt
from tabulate import tabulate

tabChar = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN&é-éù$:;123456789"


def generation_clePrivee(difficulty):
    clePrivee = []
    for i in range(0, difficulty*4):
        clePrivee.append(random.randint(1, 9))
        
    return clePrivee

def generation_clePublique(ternary_representations, clePrivee, difficulty):
    g = []
    for i in range(0,difficulty*4):
        g.append(random.randint(-1, 1))
        
            
    clePublique = []
    
    for i in range(0,difficulty*4):
        temp = clePrivee[i] * g[i]
        clePublique.append(temp)
        
    return clePublique

def decimal_to_ternary_with_minus_one(decimal_number):
    if decimal_number == 0:
        return "0"

    ternary_digits = []
    while decimal_number > 0:
        remainder = decimal_number % 3
        if remainder == 2:
            ternary_digits.append(-1)
        else:
            ternary_digits.append(remainder)
        decimal_number //= 3

    ternary_digits.reverse()
    
    j = 1
    
    if(len(ternary_digits) % 4 != 0):
        i = 4
        
        while( j > 0):
            j = len(ternary_digits) - i
            i += 4
            
    ternary = []
            
      
    for i in range(0, j*-1):
        ternary.append(0)
    
    ternary.extend(ternary_digits)
    

    return ternary


def motAleatoire(filename):
    with open(filename,"r") as file:
       lignes = file.readlines()
       while True:
        choix = input("Choisissez la difficulté entre 1 et 4 : ")
        if choix.isdigit() and 1 <= int(choix) <= 4:
            
            choix = int(choix)-1
            motsTab = lignes[choix].split()
            mot = random.choice(motsTab)
            
            break
        else:
            print("Choisissez une difficultée valide\n")

    return mot,choix+2
        
def motToTernaire(mot):
    ternaire =[]
    
    for i in range (0,len(mot)):
        pos = tabChar.index(mot[i])+1
        ternaireTab = decimal_to_ternary_with_minus_one(pos)
        ternaire.extend(ternaireTab)
        
    return ternaire

def message_Chiffre(difficulty, clePublic, message):
    tempTab = [i * difficulty for i in clePublic]
    messageChiffre = [i + j for i,j in zip(tempTab, message)]
    
    return messageChiffre

def clePublicRightTurn(ClePublic):
    temp = ClePublic[len(ClePublic)-1]
    ClePublic[1:] = ClePublic[:-1]
    ClePublic[0] = temp
    return ClePublic

def clePublicLeftTurn(ClePublic):
    temp = ClePublic[0]
    ClePublic[:-1] = ClePublic[1:]
    ClePublic[len(ClePublic)-1] = temp
    return ClePublic



mot,difficulty = motAleatoire("mots.txt")
clePrivee = generation_clePrivee(difficulty)

ternary_representation = motToTernaire(mot)

clePublic = generation_clePublique(ternary_representation, clePrivee, difficulty)
message_Chiffre = message_Chiffre(difficulty, clePublic, ternary_representation)

clePublicF = ["Cle Public"] + clePublic
clePublicF = list(map(str,clePublicF))

message_ChiffreF = ["Message Chiffre"] + message_Chiffre
message_ChiffreF = list(map(str,message_ChiffreF))

tableaux = [clePublicF, message_ChiffreF]

resultat = tabulate(tableaux, tablefmt="plain")

print("\n"+resultat)

while not all(val in [1,-1,0] for val in message_Chiffre):
    while msvcrt.kbhit():

        
        user_input = msvcrt.getch()
        if user_input == b'\xe0':
            user_input = msvcrt.getch()
        
        
        if user_input == b'H':
            clePublic[:] = np.array(clePublic) * -1
        elif user_input == b'M':
            clePublic = clePublicRightTurn(clePublic)
        elif user_input == b'K':
            clePublic = clePublicLeftTurn(clePublic)
        elif user_input == b'P':
            message_Chiffre[:] = np.array(message_Chiffre) + np.array(clePublic)
            
        
        clePublicF = ["Cle Public"] + clePublic
        clePublicF = list(map(str,clePublicF))
        
        message_ChiffreF = ["Message Chiffre"] + message_Chiffre
        message_ChiffreF = list(map(str,message_ChiffreF))

        tableaux = [clePublicF, message_ChiffreF]

        resultat = tabulate(tableaux, tablefmt="plain")

        print("\n"+resultat)
        
print("Bravo le résultat était "+ '"'+mot+'"')

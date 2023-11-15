from ctypes import sizeof
import random
import numpy as np
import msvcrt
from tabulate import tabulate

tabChar = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN&é-éù$:;123456789"


def generation_clePublique(difficulty):
    clePublique = []
    for i in range(0, difficulty*4):
        clePublique.append(random.randint(1, 9))
        
    return clePublique

def generation_clePrivee(ternary_representations, clePublique, difficulty):
    g = []
    for i in range(0,difficulty*4):
        g.append(random.randint(-1, 1))
        
            
    clePrivee = []
    
    for i in range(0,difficulty*4):
        temp = clePublique[i] * g[i]
        clePrivee.append(temp)
        
    return clePrivee

def repTernaire(decimal_number):
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
        ternaireTab = repTernaire(pos)
        ternaire.extend(ternaireTab)
        
    return ternaire

def message_Chiffre(difficulty, clePrivee, message):
    tempTab = [i * difficulty for i in clePrivee]
    messageChiffre = [i + j for i,j in zip(tempTab, message)]
    
    return messageChiffre

def clePriveeRightTurn(ClePrivee):
    temp = ClePrivee[len(ClePrivee)-1]
    ClePrivee[1:] = ClePrivee[:-1]
    ClePrivee[0] = temp
    return ClePrivee

def clePriveeLeftTurn(ClePrivee):
    temp = ClePrivee[0]
    ClePrivee[:-1] = ClePrivee[1:]
    ClePrivee[len(ClePrivee)-1] = temp
    return ClePrivee



mot,difficulty = motAleatoire("mots.txt")
print(difficulty)
clePublique = generation_clePublique(difficulty)

repTernaire = motToTernaire(mot)

clePrivee = generation_clePrivee(repTernaire, clePublique, difficulty)
message_Chiffre = message_Chiffre(difficulty, clePrivee, repTernaire)

clePriveeF = ["Cle Privee"] + clePrivee
clePriveeF = list(map(str,clePriveeF))

message_ChiffreF = ["Message Chiffre"] + message_Chiffre
message_ChiffreF = list(map(str,message_ChiffreF))

tableaux = [clePriveeF, message_ChiffreF]

resultat = tabulate(tableaux, tablefmt="plain")

print("\n"+resultat)

while not all(val in [1,-1,0] for val in message_Chiffre):
    while msvcrt.kbhit():

        
        user_input = msvcrt.getch()
        if user_input == b'\xe0':
            user_input = msvcrt.getch()
        
        
        if user_input == b'H':
            clePrivee[:] = np.array(clePrivee) * -1
        elif user_input == b'M':
            clePrivee = clePriveeRightTurn(clePrivee)
        elif user_input == b'K':
            clePrivee = clePriveeLeftTurn(clePrivee)
        elif user_input == b'P':
            message_Chiffre[:] = np.array(message_Chiffre) + np.array(clePrivee)
            
        
        clePriveeF = ["Cle Privee"] + clePrivee
        clePriveeF = list(map(str,clePriveeF))
        
        message_ChiffreF = ["Message Chiffre"] + message_Chiffre
        message_ChiffreF = list(map(str,message_ChiffreF))

        tableaux = [clePriveeF, message_ChiffreF]

        resultat = tabulate(tableaux, tablefmt="plain")

        print("\n"+resultat)
        
print("Bravo le résultat était "+ '"'+mot+'"')

import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from warcio.archiveiterator import ArchiveIterator
import glob
import re
import os
import numpy as np
import sys
import time
from tkinter import *

file= pd.read_csv(r"C:\Users\shahz\OneDrive\Desktop\MSAI\cdx-00001\data_spilit_0.2.csv")
a=file['url']
temp=list()
data=[]

#below is the defination for the AND operation
def AND_op(word1,word2):
    if ((word1) and (word2)):
        return set(word1).intersection(word2)
    else:
        return set()

#below is the defination for OR operation
def OR_op(word1,word2):
    return set(word1).union(word2)

def NOT_op(word):
    if word is not dictionary:
        return doc_no


def postfix(infix_tokens):
    # precendence initialization
    precedence = {}
    precedence["NOT"] = 3
    precedence["AND"] = 2
    precedence["OR"] = 1
    precedence["("] = 0
    precedence[")"] = 0
    output = []
    operator_stack = []
# creating postfix expression
    for token in infix_tokens:
        if (token == "("):
            operator_stack.append(token)
        elif (token == ")"):
            operator = operator_stack.pop()
            while operator != "(":
                output.append(operator)
                operator = operator_stack.pop()
        elif (token in precedence):
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]
                        operator_stack.append(token)
        else:
            output.append(token.lower())

# while staack is not empty appending
        while (operator_stack):
            output.append(operator_stack.pop())
        return output

def process_query(q, dictionary_inverted):
    q = q.replace("(", "( ")
    q = q.replace(")", " )")
    q = q.split(" ")
    query = []
    for i in q:
        query.append(i)
        for i in range(0, len(query)):
            if (query[i] == "and" or query[i] == "or" or query[i] == "not"):
                query[i] = query[i].upper()
        results_stack = []
        postfix_queue = postfix(query)
        # evaluating postfix query expression
        for i in postfix_queue:
            if (i != "AND" and i != "OR" and i != "NOT"):
                i = i.replace("(", " ")
                i = i.replace(")", " ")
                i = i.lower()
                i = dictionary_inverted.get(i)
                results_stack.append(i)
            elif (i =="AND"):
                a = results_stack.pop()
                b = results_stack.pop()
                results_stack.append(AND_op(a, b))
            elif (i =="OR"):
                a = results_stack.pop()
                b = results_stack.pop()
                results_stack.append(OR_op(a, b))
            elif (i == "NOT"):
                a = results_stack.pop()
                print(a)
                results_stack.append(NOT_op(a))

            return results_stack.pop()

def fetch_data(file):

    for url in a:
        temp=url
        break

    for url in a:
        rqst = requests.get(temp)

        getcontent = BeautifulSoup(rqst.content, 'html.parser')

        elements = getcontent.findAll("div", class_="mw-body-content mw-content-ltr")
        for element in elements:
            title_element = element
            stipped = title_element.text.strip()
            stipped= stipped.lower()
            token_data=(nltk.word_tokenize(stipped))
            Stopwords = set(stopwords.words('english'))
            c_tokens = [''.join(e for e in string if e.isalnum()) for string in token_data]
            data = [x for x in c_tokens if x]
            return data

data = fetch_data(file)
fdist = nltk.FreqDist(data)
tmp = list()
frq = list()

for k,v in fdist.items():
    tmp.append((v,k))
tmp = sorted(tmp, reverse=True)
for kk,vv in tmp[:]:
    temp.append(vv)
    frq.append(kk)

temp_dict = {}
dictionary = {}
a = 0
for i in range(0,10):
 doc_no = i

key = temp
for x in key:
    key = x
    temp_dict.setdefault(key, [])
    temp_dict[key].append(a)
    a += 1
    for x in temp_dict:
        if dictionary.get(x):
            dictionary[x] = temp_dict.get(x)
        else:
            key = x
            dictionary.setdefault(key, [])
            dictionary[key] = {}
            dictionary[x][doc_no] = temp_dict.get(x)
            dictionary = {a: list(set(b)) for a, b in dictionary.items()}


dictionary_inverted=dictionary
#q=input("Enter Query")
#result=process_query(q, dictionary_inverted)
#print("document number is ::", doc_no, "....", "Location for required text is ::", result)
def button():
    query= Textinput.get()
    results=process_query(query, dictionary_inverted)
    var.set(results)
    var2.set(doc_no)
    print("document number is ::", doc_no, "....", "Location for required text is ::", results)

window=Tk()
window.geometry("400x300")
window.title("Search query")
icon= PhotoImage(file='aulogo.png')
window.iconphoto(True, icon)
main_label = Label(window,text="Search Engine",fg='black',bg='white', font=("arial",12,"bold")).pack()
main_label2 = Label(window,text="IRM project (211786)",fg='black',bg='grey',relief='solid', font=("arial",9,"bold")).pack()
var = StringVar()
var2 = StringVar()
doc=StringVar()
loc=StringVar()
doc.set("Document Number =>")
loc.set("Location =>")
main_label3 = Label(window, textvariable=var, relief=RAISED, font=("arial", 12)).place(x=300,y=170)
main_label4 = Label(window, textvariable=var2, relief=RAISED,font=("arial", 12)).place(x=300,y=200)
label=Label(window, textvariable=loc, relief=RAISED,font=("arial", 12)).place(x=110,y=170)
label2=Label(window, textvariable=doc, relief=RAISED,font=("arial", 12)).place(x=110,y=200)
Textinput = Entry(window, font=("arial", 12))
Textinput.place(x=110,y=120)

querybutton=Button(window,text="Search query",fg='black',bg='purple',relief='solid',command=button, font=("arial",10)).place(x=250,y=250)


window.mainloop()

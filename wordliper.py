#!/usr/bin/python3
#Writen by Jony Schats - Kadeeli - www.jonyschats.nl / https://github.com/Kadeeli
#Can probably be more efficient, but I can't code so it does its job :D
import argparse
import sys

##PARAMETERS##
parser = argparse.ArgumentParser(description='A simple wordlist generator to generate worldlists including custom strings such as company name, locations, months, periods and appending years, capitalizing first letters. Basicly permutating the wordlist.')
parser.add_argument('-s', '--strings', nargs='+', action='store', type=str, default=[], 
                    help='used to supply a(or multiple) strings such as company name(s), locations etc, seperated by spaces to be added to the wordlist')
parser.add_argument('-m', '--months', action='store_true', 
                    help='used to add all months of the year to the worldlist')
parser.add_argument('-se', '--seasons', action='store_true',
                    help='used to add all seaons of the year to the worldlist, like spring etc')
parser.add_argument('-aY', '--years', nargs='+', action='store', type=int, default=[], 
                    help='used to append a year range to every word in the wordlist, seperate them by spaces for example 2018 2020')
parser.add_argument('-f', '--file', action='store', type=str,
                    help='used to supply a file with words to be added as input for the wordlist')
parser.add_argument('-AS', '--asymbols', action='store_true',
                    help='used to append symbols to every word in the wordlist')
parser.add_argument('-As', '--astrings', nargs='+', action='store', type=str, default=[],
                    help='used to append strings to every word in the wordlist before the symbols are applied')
parser.add_argument('-PS', '--psymbols', action='store_true',
                    help='used to prepend symbols to every word in the wordlist')
parser.add_argument('-Ps', '--pstrings', nargs='+', action='store', type=str, default=[],
                    help='used to prepend strings to every word in the wordlist before the symbols are applied')
parser.add_argument('-C', '--capital', action='store_true', 
                    help='used to capitalize every first letter in the word')
parser.add_argument('-min', '--min', action='store', type=int,
                    help='used to set the minimum password length')
parser.add_argument('-max', '--max', action='store', type=int,
                    help='used to set the maximum password length')
parser.add_argument('-d', '--dutch', action='store_true', 
                    help='used to translate months and seasons to dutch')
parser.add_argument("-o", "--output", action='store', 
                    type=argparse.FileType('w'), dest='output',
                    help="Directs the output to a name of your choice")
args = parser.parse_args()

##VARIABLES, LISTS etc##
#List of dutch months used for the wordlist
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']
seasons = ['spring', 'summer', 'autumn','fall' , 'winter']
dutch_months = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli',
          'augustus', 'september', 'oktober', 'november', 'december']
dutch_seasons = ['lente', 'zomer', 'herfst', 'winter']
symbols = ['!', '@', '.', '-', '_', '#', '$', '&', '+', '?', '123']
wordlist = []
newwordlist = []
tempnewwordlist = []
tempnewwordlist2 = []

#print help message if no argument is supplied!
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

##MAKING THE WORDLIST##
if args.dutch:
    print("[+] Translating months and seasons to dutch variants")
    months = dutch_months
    seasons = dutch_seasons

if args.months:
    print("[+] Adding months to the worldlist")
    wordlist.extend(months)

if args.seasons:
    print("[+] Adding seasons to the worldlist")
    wordlist.extend(seasons)

if args.file:
    with open(args.file, 'r') as f:
        newworldlist = [line.strip() for line in f]
        wordlist.extend(newwordlist)


if args.strings != []:
    print("[+] Adding the provided strings to the worldlist")
    wordlist.extend(args.strings)

if args.years != []:
    print("[+] Appending years to every word in the wordlist")
    for i in range(args.years[0], args.years[1]+1):
        yearwordlist = [x + str(i) for x in wordlist]
        newwordlist.extend(yearwordlist)
    wordlist.extend(newwordlist)

if args.astrings != [] or args.pstrings != []:
    if args.astrings != []:
        print("[+] Appending strings to every word in the wordlist")
        for i in args.astrings:
            stringwordlist = [x + str(i) for x in wordlist]
            tempnewwordlist.extend(stringwordlist)

    if args.pstrings:
        print("[+] Prepending strings to every word in the wordlist")
        for i in args.pstrings:
            stringwordlist = [str(i) + x for x in wordlist]
            tempnewwordlist2.extend(stringwordlist)
    wordlist.extend(tempnewwordlist)
    wordlist.extend(tempnewwordlist2)

if args.asymbols or args.psymbols:
    if args.asymbols:
        print("[+] Appending symbols to every word in the wordlist")
        for i in symbols:
            symbolwordlist = [x + str(i) for x in wordlist]
            tempnewwordlist.extend(symbolwordlist)

    if args.psymbols:
        print("[+] Prepending symbols to every word in the wordlist")
        for i in symbols:
            symbolwordlist = [str(i) + x for x in wordlist]
            tempnewwordlist2.extend(symbolwordlist)
    wordlist.extend(tempnewwordlist)
    wordlist.extend(tempnewwordlist2)

if args.capital:
    print("[+] Capitalizing the first letter of every word")
    newwordlist = [words.capitalize() for words in wordlist]
    wordlist.extend(newwordlist)

if args.min and args.max:
    print("[-] Deleting words if smaller then", args.min, "characters and larger then", args.max,"characters")
    for word in wordlist:
        if (len(word) < args.min) or (len(word) > args.max): wordlist.remove(word)

if args.output:
    output_file = args.output
    output_file.write('\n'.join(str(word) for word in wordlist))
    print("[=] Generated", len(wordlist), "words")
else:
    print(*wordlist, sep = "\n")
    print("[=] Generated", len(wordlist), "words")

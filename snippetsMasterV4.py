### convert praat snippet written according to hash format for its usage in Vscode, Sublime text, Atom and Vim

## locate hash positions and stock them in a list
def listPositionHash(contents):
    positionOfHashes = []
    for lineNumber, lineContent in enumerate(contents):
        if lineContent.startswith('#') and not lineContent.startswith('##'):
            positionOfHashes.append(lineNumber)
    return positionOfHashes

## import all optional arguments used in command line
import argparse, sys
# create a parser
parser = argparse.ArgumentParser()
# introduce your praat snippets file as the second argument
with open(sys.argv[1], 'r') as fileInput:
    contents = fileInput.readlines()
    positionOfHashes = listPositionHash(contents)
parser.add_argument(sys.argv[1])
# add optional arguments to choose output file's format
for x in ["-vsc", "-atom", "-sublime", "-vim", "-all"]:
    parser.add_argument(x, action="store_true")
# add an argument to get our arguments from parser
args = parser.parse_args()



## transform body

# function 1: record existence of all symbols $ : , ( )" in a line and return a dictionary
def recordSymbols(bodyContent):
    existenceOfSymbols = {}
    for a, b in enumerate(bodyContent):
        if '$' in b and not b.endswith('$') and not b[-2:] == '$:' :
            existenceOfSymbols['dollarstart' + str(a)] = 1
        if b.endswith('$'):
            existenceOfSymbols['dollarend' + str(a)] = 1
        if b[-2:] == '$:':
            existenceOfSymbols['dollarcolon' + str(a)] = 1
        if ':' in b and not b[-2:] == '$:':
            existenceOfSymbols['colon' + str(a)] = 1
        if b.startswith('\"'):
            existenceOfSymbols['quoteopen' + str(a)] = 1
        if b.endswith('\"'):
            existenceOfSymbols['quoteclose' + str(a)] = 1
        if b[-2:] == '\",':
            existenceOfSymbols['quoteclose' + str(a)] = 1
        if '(' in b:
            existenceOfSymbols['bracketopen' + str(a)] = 1
            if '\"' in b:
                existenceOfSymbols['quoteopen' + str(a)] = 1
        if ')' in b:
            existenceOfSymbols['bracketclose' + str(a)] = 1
            if '\"' in b:
                existenceOfSymbols['quoteclose' + str(a)] = 1
        if ',' in b:
            existenceOfSymbols['comma' + str(a)] = 1
    return existenceOfSymbols

# function 2: remove all
def removeSymbols(bodyContent):
    for a, b in enumerate(bodyContent):
        for i in ['$', ':', '\"', ',', '(', ')']:
            bodyContent[a] = bodyContent[a].replace(i, '')
    return bodyContent

# function 3: transform body for VScode
# put back colon if colon existed (colona:1):
# if dollar existed at the same time, insert colon and add curly braces, ex. 1name > {1:name};
# else, add colon at the end, ex. draw > draw:
def transformBody(bodyContent):
    for a, b in enumerate(bodyContent):
        if existenceOfSymbols.get('colon' + str(a)) == 1:
            if existenceOfSymbols.get('dollarstart' + str(a)) == 1:
                bodyContent[a] = '{' + bodyContent[a][:1] + ':' + bodyContent[a][1:] + '}'
            else:
                bodyContent[a] = bodyContent[a] + ':'
        # put back dollar if dollar existed at the beginning (dollarstarta:1)
        if existenceOfSymbols.get('dollarstart' + str(a)) == 1:
            bodyContent[a] = '$' + bodyContent[a]
        # put back dollar if dollar existed at the end (dollarenda:1)
        if existenceOfSymbols.get('dollarend' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + '$'
        # put back dollar comma at the end (dollarcommaa:1)
        if existenceOfSymbols.get('dollarcolon' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + '$:'
        # put back quotes as '\\\"' if quotes existed at the beginning(quoteopena:1)
        if existenceOfSymbols.get('quoteopen' + str(a)) == 1:
            bodyContent[a] = '\\\"' + bodyContent[a]
        # put back quotes as '\\\"' if quotes existed at the end(quoteclosea:1)
        if existenceOfSymbols.get('quoteclose' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + '\\\"'
        # put back left bracket if it existed at the beginning (bracketopena:1)
        if existenceOfSymbols.get('bracketopen' + str(a)) == 1:
            bodyContent[a] = '(' + bodyContent[a]
        # put back right bracket if it existed at the end(bracketclosea:1)
        if existenceOfSymbols.get('bracketclose' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + ')'
        # put back comma if comma existed (commaa:1)
        if existenceOfSymbols.get('comma' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + ','
    transformedBody = ' '.join(bodyContent)
    return transformedBody
def transformBody2(bodyContent):
    for a, b in enumerate(bodyContent):
        if existenceOfSymbols.get('colon' + str(a)) == 1:
            if existenceOfSymbols.get('dollarstart' + str(a)) == 1:
                bodyContent[a] = '{' + bodyContent[a][:1] + ':' + bodyContent[a][1:] + '}'
            else:
                bodyContent[a] = bodyContent[a] + ':'
        # put back dollar if dollar existed at the beginning (dollarstarta:1)
        if existenceOfSymbols.get('dollarstart' + str(a)) == 1:
            bodyContent[a] = '$' + bodyContent[a]
        # put back dollar if dollar existed at the end (dollarenda:1)
        if existenceOfSymbols.get('dollarend' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + '$'
        # put back dollar colon at the end (dollarcolona:1)
        if existenceOfSymbols.get('dollarcolon' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + '$:'
        # put back quotes if quotes existed at the beginning (quoteopena:1)
        if existenceOfSymbols.get('quoteopen' + str(a)) == 1:
            bodyContent[a] = '\"' + bodyContent[a]
        # put back quotes if quotes existed at the end (quoteclosea:1)
        if existenceOfSymbols.get('quoteclose' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + '\"'
        # put back left bracket if it existed at the beginning(bracketopena:1)
        if existenceOfSymbols.get('bracketopen' + str(a)) == 1:
            bodyContent[a] = '(' + bodyContent[a]
        # put back right bracket if it existed at the end(bracketclosea:1)
        if existenceOfSymbols.get('bracketclose' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + ')'
        # put back comma if comma existed (commaa:1)
        if existenceOfSymbols.get('comma' + str(a)) == 1:
            bodyContent[a] = bodyContent[a] + ','
    transformedBody = ' '.join(bodyContent)
    return transformedBody

# write contents in new file for VScode
def writeVsc(filename):
    global existenceOfSymbols
    fileOutput1.write('{\n')
    for i in range(len(positionOfHashes) - 1):
        # content after hash in the same line is description
        description = contents[positionOfHashes[i]].split('# ')[1]
        # next line content after hash is prefix
        prefix = contents[positionOfHashes[i] + 1]
        # transform prefix and description
        fileOutput1.write('\"' + description[:-1] + '\": {\n')
        fileOutput1.write('\t\"prefix\": ' + '\"' + prefix[:-1] + '\",\n')
        fileOutput1.write('\t\"body\": [\n')
        # transform body
        for n in range(positionOfHashes[i] + 2, positionOfHashes[i + 1]):
            # exclude the comment line with three hashes
            if not contents[n].startswith('#'):
                # take apart line content to transform certain parts with special symbols
                bodyContent = contents[n].split()
                if contents[n].startswith(' '):
                    bodyContent = [' '] + bodyContent
                existenceOfSymbols = recordSymbols(bodyContent)
                removedSymbols = removeSymbols(bodyContent)
                transformedBody = transformBody(removedSymbols)
                fileOutput1.write('\t\t\"' + transformedBody + '\",\n')
        # add comma after brackets to separate snippets except last one
        fileOutput1.write('\t' + '],' + '\n')
        if i == (len(positionOfHashes) - 2):
            fileOutput1.write('\t\"description\": \"' + description[:-1] + '\"' + '\n' + '}\n')
        else:
            fileOutput1.write('\t\"description\": \"' + description[:-1] + '\"' + '\n' + '},\n')
    fileOutput1.write('}')
def writeSublime():
    global existenceOfSymbols
    for i in range(len(positionOfHashes) - 1):
            # content after hash in the same line is description
            description = contents[positionOfHashes[i]].split('# ')[1]
            # next line content after hash is prefix
            prefix = contents[positionOfHashes[i] + 1]
            with open (prefix + '.txt', 'w') as fileOutput2:
                fileOutput2.write('<snippet>\n')
                fileOutput2.write('\t<content><![CDATA[\n')
                # transform body
                for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
                    if not contents[n].startswith('#'):
                        bodyContent = contents[n].split()
                        existenceOfSymbols = recordSymbols(bodyContent)
                        removedSymbols = removeSymbols(bodyContent)
                        transformedBody = transformBody2(removedSymbols)
                        fileOutput2.write(transformedBody + "\n")
                fileOutput2.write(']]></content>\n')
                # transform description and prefix
                fileOutput2.write('\t<description>' + description[:-1] + '</description>\n')
                fileOutput2.write('\t<tabTrigger>' + prefix[:-1] + '</tabTrigger>\n')
                fileOutput2.write('</snippet>\n\n')
                # export all snippets in multiple files named as prefix.sublime-snippet
                # use prefix to locate every snippet and to name snippet files




def writeAtom(fileOutput3):
    global existenceOfSymbols
    for i in range(len(positionOfHashes) - 1):
        # content after hash in the same line is description
        description = contents[positionOfHashes[i]].split('# ')[1]
        # next line content after hash is prefix
        prefix = contents[positionOfHashes[i] + 1]
        # transform description and prefix
        fileOutput3.write("'" + description[:-1] + "':\n")
        fileOutput3.write("\t'prefix':" + "'" + prefix[:-1] + "'\n")
        fileOutput3.write("\t'body':" + '"""\n')
        # transform body
        for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
            if not contents[n].startswith('#'):
                bodyContent = contents[n].split()
                existenceOfSymbols = recordSymbols(bodyContent)
                removedSymbols = removeSymbols(bodyContent)
                transformedBody = transformBody2(removedSymbols)
                fileOutput3.write('\t\t' + transformedBody + '\n')
        fileOutput3.write('\t"""\n\n')

def writeVim(fileOutput4):
    global existenceOfSymbols
    for i in range(len(positionOfHashes) - 1):
        # content after hash in the same line is description
        description = contents[positionOfHashes[i]].split('# ')[1]
        # next line content after hash is prefix
        prefix = contents[positionOfHashes[i] + 1]
        # transform prefix
        fileOutput4.write('snippet ' + prefix)
        # transform body
        for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
            if not contents[n].startswith('#'):
                bodyContent = contents[n].split()
                existenceOfSymbols = recordSymbols(bodyContent)
                removedSymbols = removeSymbols(bodyContent)
                transformedBody = transformBody2(removedSymbols)
                fileOutput4.write(transformedBody + '\n')
        fileOutput4.write('endsnippet\n\n')



## rewrite contents in new files
# export file for Vscode
if args.vsc:
    with open('snippetsPraatVSC.txt', 'w') as fileOutput1:
        writeVsc(fileOutput1)
# export file for Sublime Text
if args.sublime:
    writeSublime()
# export file for Atom
if args.atom:
    with open('snippetsPraatAtom.txt', 'w') as fileOutput3:
        writeAtom(fileOutput3)
# export file for Vim
if args.vim:
    with open('snippetsPraatVim.txt', 'w') as fileOutput4:
        writeVim(fileOutput4)
# export all files
if args.all:
    with open('snippetsPraatVSC.txt', 'w') as fileOutput1:
        writeVsc(fileOutput1)
    with open('snippetsPraatSublime.txt', 'w') as fileOutput2:
        writeSublime(fileOutput2)
    with open('snippetsPraatAtom.txt', 'w') as fileOutput3:
        writeAtom(fileOutput3)
    with open('snippetsPraatVim.txt', 'w') as fileOutput4:
        writeVim(fileOutput4)
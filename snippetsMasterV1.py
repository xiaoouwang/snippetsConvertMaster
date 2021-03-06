# import the argparse module
import argparse
# create a parser
parser = argparse.ArgumentParser()
for x in ["-vsc", "-atom", "-sublime", "-vim", "-all"]:
    parser.add_argument(x, action="store_true")
# add an argument to get our arguments from parser
args = parser.parse_args()

# def transformBody2():
#     bodyContent = lines[n].split()
#     for a, b in enumerate(bodyContent):
#         if "$" in b and ":" in b:
#             bodyContent[a] = "{" + bodyContent[a] + "}"
#     body = ' '.join(bodyContent)
#     return body


def transformBody(bodyContent):
    # transform prompt in body
    for a, b in enumerate(bodyContent):
        if "$" in b and ":" in b and ("\"" not in b):
            bodyContent[a] = "${" + bodyContent[a].replace("\"","")[1:] + "}"
            bodyContent[a] = bodyContent[a].replace(",","")
            bodyContent[a] = bodyContent[a].replace('\"', '\\\"') + ","
        if "$" in b and ":" in b and "\"" in b:
            bodyContent[a] = "\"" + "${" + bodyContent[a].replace("\"","")[1:] + "}" + "\""
            bodyContent[a] = bodyContent[a].replace(",","")
        if "\"" in b:
            bodyContent[a] = bodyContent[a].replace('\"', '\\\"') + ","
    body = ' '.join(bodyContent)
    return body

def writeVsc(fileOutput1):
    # transform description and prefix
    fileOutput1.write('\n' + '"' + description[:-1] + '": {' + '\n')
    fileOutput1.write('\t' + '"prefix": "' + prefix[:-1] + '",' + '\n')
    fileOutput1.write('\t' + '"body": [' + '\n')
    # transform body
    for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
        if not lines[n].startswith('#'):
            bodyContent = lines[n].split()
            transformedBody = transformBody(bodyContent)
            fileOutput1.write('\t'*2 + '"' + transformedBody + '",' + '\n')
    fileOutput1.write('\t' + '],' + '\n')
    # exclude last
    if i == (len(positionOfHashes) - 2):
        fileOutput1.write('\t"description": "' + description[:-1] + '"' + '\n' + '}\n')
    else:
        fileOutput1.write('\t"description": "' + description[:-1] + '"' + '\n' + '},\n')

def writeSublime(fileOutput2):
    fileOutput2.write('<snippet>\n')
    fileOutput2.write('\t<content><![CDATA[\n')
    # transform body
    for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
        if not lines[n].startswith('#'):
            bodyContent = lines[n].split()
            transformedBody = transformBody(bodyContent)
            fileOutput2.write(transformedBody + "\n")
    fileOutput2.write(']]></content>\n')
    # transform description and prefix
    fileOutput2.write('\t<description>' + description[:-1] + '</description>\n')
    fileOutput2.write('\t<tabTrigger>' + prefix[:-1] + '</tabTrigger>\n')
    fileOutput2.write('</snippet>\n\n')

def writeAtom(fileOutput3):
    # transform description and prefix
    fileOutput3.write("'" + description[:-1] + "':\n")
    fileOutput3.write("\t'prefix':" + "'" + prefix[:-1] + "'\n")
    fileOutput3.write("\t'body':" + '"""\n')
    # transform body
    for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
        if not lines[n].startswith('#'):
            bodyContent = lines[n].split()
            transformedBody = transformBody(bodyContent)
            fileOutput3.write("\t\t" + transformedBody + "\n")
    fileOutput3.write('\t"""\n\n')

def writeVim(fileOutput4):
    # transform prefix
    fileOutput4.write('snippet ' + prefix)
    # transform body
    for n in range(positionOfHashes[i] + 2, positionOfHashes[i+1]):
        if not lines[n].startswith('#'):
            bodyContent = lines[n].split()
            transformedBody = transformBody(bodyContent)
            fileOutput4.write(transformedBody + "\n")
    fileOutput4.write('endsnippet\n\n')


# open the original text file and read the content line by line
with open("snippetsPraat.txt") as file:
    lines = file.readlines()
    # create a list which contains all line numbers of hashes
    positionOfHashes = []
    for lineNumber, lineContent in enumerate(lines):
        if lineContent.startswith('#') and not lineContent.startswith('###'):
            positionOfHashes.append(lineNumber)
# create new text files for writing output
with open("snippetsPraatVsc.txt", "w") as fileOutput1, open("snippetsPraatSublime.txt", "w") as fileOutput2, open("snippetsPraatAtom.txt", "w") as fileOutput3, open("snippetsPraatVim.txt", "w") as fileOutput4:
    fileOutput1.write('{')
    # use i to index the list of hashes'positions except the last one
    for i in range(len(positionOfHashes) - 1):
        # exclude the comment line with three hashes
        if not lines[positionOfHashes[i] + 1].startswith('#'):
            # content after hash is description
            description = lines[positionOfHashes[i]].split('# ')[1]
            # content of the first line after hash is prefix
            prefix = lines[positionOfHashes[i] + 1]
            # write lines in the new file that we just created

            ## convert to vsc snippets
            if args.vsc:
                writeVsc(fileOutput1)

            ## convert to sumblime text snippets
            if args.sublime:
                writeSublime(fileOutput2)

            ## convert to atom snippets
            if args.atom:
                writeAtom(fileOutput3)


            ## convert to vim snippets
            if args.vim:
                writeVim(fileOutput4)

            ## convert to all types of snippets
            if args.all:
                writeVsc(fileOutput1)
                writeSublime(fileOutput2)
                writeAtom(fileOutput3)
                writeVim(fileOutput4)
    fileOutput1.write('}')

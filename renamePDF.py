# Nicholas Barron - June 2023
# This program will extract metadata from a PDF file and rename the file 
# in a format consistent with the .README.txt.


#%% IMPORT LIBRARIES ******************************************************** #
import subprocess
#import sys
import os
import pybtex
import pybtex.database
#import keyword args
import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Rename PDFs')

parser.add_argument('-d', '--directory', type=str, default='.', help='Directory storing the PDFs to be renamed.')

os.chdir(parser.parse_args().directory)


#create output.log (overwrite if exists)
output = open(".output.log", "w")
#dayTime = subprocess.check_output(["date"]).decode()
output.write("Output log for renamePDF.py\n")

#open biblio.bib (append if exists)
biblio = open("./.bibliography/biblio.bib", "a")

# run kbib from command line, add output to bib variable
#kbib -pdf *.pdf
filenames = os.listdir("./.unprocessedPapers/")
for filename in filenames:
    if filename.endswith(".pdf"):
        try:
            print(filename)
            #run kbib from command line
            bib = subprocess.check_output(["kbib", "-pdf", "./.unprocessedPapers/"+filename])
            
            #remove everything before "@"
            bibRaw = bib[bib.find(b'@'):]
            bibID = bibRaw[bibRaw.find(b'{')+1:bibRaw.find(b',')].decode()
            
            #parse bib data
            bibData = pybtex.database.parse_string(bib.decode(), bib_format='bibtex')

            # get metadata from bibData
            firstAuthor = bibData.entries[bibID].persons['author'][0].last_names[0]
            year = bibData.entries[bibID].fields['year']
            newFilename = firstAuthor + year

            # additional authors
            for person in bibData.entries[bibID].persons['author'][1:]:
                nextAuthor = person.last_names[0]
                newFilename = newFilename + nextAuthor

            #set key to remain consistent with .README.txt
            bibIdNew = newFilename
            bibRaw = bibRaw.replace(bibID.encode(), bibIdNew.encode())
            #get title
            title = bibData.entries[bibID].fields['title']
            #capitalize first letter of each word in title
            title = title.title()
            #split title into words
            title = title.split()
            #capitalize first letter of each word
            title = [word.capitalize() for word in title]
            title = title[0] + title[1] + title[2] + title[3] + title[4]
            newFilename = newFilename + ' - ' + title + '.pdf'
            
            #move, rename, write log, and write biblio.bib
            
            print(bibData)
            query = input("mv ./.unprocessedPapers/"+filename+ "./Papers/"+newFilename+"? (y/n)")
            if query == "y":
                os.rename("./.unprocessedPapers/"+filename, "./"+newFilename)
                #add to output.log
                output.write("mv ./.unprocessedPapers/"+filename+ "./Papers/"+newFilename+ "\n")
                #add to ./bibliography/biblio.bib
                biblio.write(bibRaw.decode())
                output.write("Wrote bibtex entry for " + filename + "\n")
            else:
                print("File not renamed")
                #add to output.log
                output.write(filename+" not renamed\n")
        except:
            print("Error with " + filename)
            #add to output.log
            output.write("Error with " + filename + "\n")

#close output.log and biblio.bib
output.close()
biblio.close()



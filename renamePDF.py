# Nicholas Barron - June 2023
# This program will extract metadata from a PDF file and rename the file 
# in a format consistent with the .README.txt file in the /Papers/ directory.

#you may need to create a new virtual environment for this to work properly.
    # you can install the virtual env. by loading the requirements.txt file
    # and then running the following command:
    # pip install -r ./.renamePDF/requirements.txt


#%% IMPORT LIBRARIES ******************************************************** #
import subprocess
#import sys
import os


#%% INSTALL DEPENDENCIES *******************************************************
#kbib
#subprocess.check_call([sys.executable, "-m", "pip", "install", "kbib[pdf]"])
#pybtex
#subprocess.check_call([sys.executable, "-m", "pip", "install", "pybtex"])

#%% LOAD NEW LIBRARIES *********************************************************
import pybtex
import pybtex.database

#%% RUN KBIB ON ALL PDF FILES IN ./Papers/ ************************************
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



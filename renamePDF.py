# Nicholas Barron - June 2023
# This program will extract metadata from a PDF file and rename the file
# in a format consistent with the .README.txt.


# %% IMPORT LIBRARIES ******************************************************** #
import subprocess
# import sys
import os
import pybtex
import pybtex.database
from pybtex.database import BibliographyData, Entry

# import keyword args
import argparse

# %% functions

# Dictionary to hold citation information


def manualBib():
    # Error handling for failed DOI or pdf search.
    citation_info = {
        "type": "article",
        "fields": {}
    }

    # Prompting user for necessary information
    citation_info["fields"]["title"] = input(
        "Enter the title of the article: ")
    citation_info["fields"]["author"] = input(
        "Enter the author(s) of the article: ")
    citation_info["fields"]["journal"] = input("Enter the journal name: ")
    citation_info["fields"]["year"] = input("Enter the publication year: ")
    citation_info["fields"]["volume"] = input("Enter the volume number: ")
    citation_info["fields"]["pages"] = input("Enter the page numbers: ")
    citation_info["fields"]["doi"] = input(
        "Enter the DOI (optional, press enter to skip): ")

    # Creating the BibTeX entry
    entry = Entry(citation_info["type"], fields=citation_info["fields"])
    bib_data = BibliographyData(entries={"myCitation": entry})

    # Returning the formatted BibTeX entry
    return bib_data.to_bytes("bibtex")


def processBib(bib):
    # remove everything before "@"

    bibRaw = bib[bib.find(b'@'):]
    bibID = bibRaw[bibRaw.find(b'{')+1:bibRaw.find(b',')].decode()

    # parse bib data
    bibData = pybtex.database.parse_string(
        bib.decode(), bib_format='bibtex')

    # get metadata from bibData
    firstAuthor = bibData.entries[bibID].persons['author'][0].last_names[0]
    year = bibData.entries[bibID].fields['year']
    newFilename = firstAuthor + year

    # additional authors
    for person in bibData.entries[bibID].persons['author'][1:]:
        nextAuthor = person.last_names[0]
        newFilename = newFilename + nextAuthor

    # set key to remain consistent with .README.txt
    bibIdNew = newFilename
    bibRaw = bibRaw.replace(bibID.encode(), bibIdNew.encode())
    # get title
    title = bibData.entries[bibID].fields['title']
    # capitalize first letter of each word in title
    title = title.title()
    # split title into words
    title = title.split()
    # capitalize first letter of each word
    title = [word.capitalize() for word in title]
    shortTitle = ""
    for i in range(min(len(title), 5)):
        shortTitle += title[i]
    # remove non-alphanumeric characters
    shortTitle = ''.join(e for e in shortTitle if e.isalnum())
    # add title to newFilename
    newFilename = newFilename + ' - ' + shortTitle + '.pdf'

    # move, rename, write log, and write biblio.bib

    print(bibData)
    query = input("mv ./.unprocessedPapers/"+filename +
                  "./Papers/"+newFilename+"? (y/n)")
    if query == "y":
        os.rename("./.unprocessedPapers/"+filename, "./"+newFilename)
        # add to output.log
        output.write("mv ./.unprocessedPapers/" +
                     filename + "./Papers/"+newFilename + "\n")
        # add to ./bibliography/biblio.bib
        biblio = open("./.bibliography/biblio.bib", "a")
        biblio.write(bibRaw.decode())
        biblio.close()
        output.write("Wrote bibtex entry for " + filename + "\n")
    else:
        print("File not renamed")
        # add to output.log
        output.write(filename+" not renamed\n")


# %% MAIN PROGRAM ************************************************************ #
# parse arguments
parser = argparse.ArgumentParser(description='Rename PDFs')

parser.add_argument('-d', '--directory', type=str, default='.',
                    help='Directory storing the PDFs to be renamed.')

os.chdir(parser.parse_args().directory)


# create output.log (overwrite if exists)
output = open(".output.log", "w")
# dayTime = subprocess.check_output(["date"]).decode()
output.write("Output log for renamePDF.py\n")

# open biblio.bib (append if exists)


# run kbib from command line, add output to bib variable
# kbib -pdf *.pdf
filenames = os.listdir("./.unprocessedPapers/")
for filename in filenames:
    if filename.endswith(".pdf"):

        print(filename)
        # run kbib from command line
        try:
            bib = subprocess.check_output(
                ["kbib", "-pdf", "./.unprocessedPapers/"+filename])
            print(bib)
            processBib(bib)
        except:
            if input("Error with " + filename + "Manually add DOI? (y/n)") == "y":
                doi = input("DOI: ")
                try:
                    bib = subprocess.check_output(
                        ["kbib", "-bib", doi])
                    processBib(bib)
                except:
                    print("DOI Lookup failed for " + filename)
                    # add to output.log
                    output.write("DOI Lookup failed for " + filename + "\n")

                    bib = manualBib()
                    processBib(bib)

            else:
                print("Error with " + filename)
                # add to output.log
                output.write("Error with " + filename + "\n")
                continue


# close output.log and biblio.bib
output.close()

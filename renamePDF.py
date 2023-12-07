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
import requests


# import keyword args
import argparse

# %% functions

# crossref API call


def find_doi(name, title, year):
    """
    Search for a DOI given an author's name, publication title, and year.

    Parameters:
    name (str): Author's name.
    title (str): Title of the publication.
    year (str): Year of publication.

    Returns:
    str: DOI of the publication or a message if not found.
    """

    # Base URL for CrossRef API
    base_url = "https://api.crossref.org/works?"

    # Formulate the query
    # Here we use the query.bibliographic parameter to search by publication title
    query = "query.title=" + str(title.replace(" ", " ")) + \
        "&query.author=" + str(name.replace(" ", "+")) + \
        "&query.bibliographic="+str(year)
    try:
        # Send the request
        response = requests.get(base_url+query)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response
        data = response.json()
        items = data.get("message", {}).get("items", [])

        # Extract DOI if available
        if items:
            return items[0].get("DOI", "DOI not found.")
        else:
            return "No matching publication found."

    except requests.RequestException as e:
        return f"An error occurred: {e}"


def processBib(bib):
    """
    Process the output of kbib to rename the PDF and add the BibTeX entry to biblio.bib.

    Parameters:
    bib (str): Output of kbib.
    """
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
        raise Exception("File not renamed.\n")


def manualBib():
    """
    Error handling for failed pdf search. Most often will happen with old, poorly formatted pdfs.
    """
    citation_info = {
        "type": "article",
        "fields": {}
    }

    # Prompting user for necessary information
    citation_info["fields"]["title"] = input(
        "Enter a few words of the article title: ")
    citation_info["fields"]["author"] = input(
        "Enter the author(s) of the article: ")
    citation_info["fields"]["year"] = input("Enter the publication year: ")

    # Creating the BibTeX entry
    doi = find_doi(citation_info["fields"]["author"],
                   citation_info["fields"]["title"],
                   citation_info["fields"]["year"]
                   )

    # Returning the formatted BibTeX entry
    return subprocess.check_output(
        ["kbib", "-bib", doi])


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
            processBib(bib)
            print(bib)

        except:
            while True:
                if input("Error with " + filename + ".\nManually add bib? (y/n)") == "y":

                    try:
                        bib = manualBib()
                        processBib(bib)
                        break
                    except:
                        print("Error with " + filename+"\n")
                        # add to output.log
                        output.write("Error with " + filename + "\n")
                else:
                    break

            else:
                print("Error with " + filename+"\n")
                # add to output.log
                output.write("Error with " + filename + "\n")
                continue


# close output.log and biblio.bib
output.close()

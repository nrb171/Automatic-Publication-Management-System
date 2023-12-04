import pybtex
import pybtex.database
import argparse
import os

# parse arguments
parser = argparse.ArgumentParser(description='Rename PDFs')

parser.add_argument('-d', '--directory', type=str, default='.',
                    help='Directory storing the PDFs to be renamed.')

os.chdir(parser.parse_args().directory)


def format_label(entry):
    # Custom logic to generate a new citation key
    first_author = entry.persons['author'][0].last()[0]
    year = entry.fields.get('year', '')
    other_authors = ''.join(author.last()[0]
                            for author in entry.persons['author'][1:])
    new_key = first_author + year + other_authors
    return new_key


# load file
bibData = pybtex.database.parse_file(
    "biblio.bib", bib_format='bibtex')


# Format the labels
bibDataNew = pybtex.database.BibliographyData()
errorCount = 0
for entry in bibData.entries.values():
    newKey = format_label(entry)
    print(newKey)
    while 1:
        try:
            bibDataNew.add_entry(newKey, entry)
            errorCount = 0
            break
        except pybtex.database.BibliographyDataError:
            errorCount += 1
            # 97 is unicode for "a"
            bibDataNew.add_entry(newKey + chr(97 + errorCount), entry)
            break

# Write the new bibliography to a file
bibDataNew.to_file("biblio.bib", bib_format='bibtex')

# commit changes to git
os.system("git add biblio.bib")
os.system("git commit -m 'update biblio.bib'")

# Automatic-Publication-Management-System (APMS)
This script helps to keep large repositories of academic papers organized.

# Usage Instructions
## Create a virtual environment
you can install the virtual env. by loading the `requirements.txt` file and then running the following command:
`cd path/to/Papers/`
`pip install -r ./.APMS/requirements.txt`
## Format your Papers folder
Format your `Papers` folder as follows:

`Papers`
  Processed papers are stored here.
  
  `Papers/.bibliography`
    `biblio.bib` is stored here
    
  `/Papers/.APMS`
    The scripts from APMS go here.
    
  `/Papers/.unprocessedPapers`
    pdfs to be processed go here.


To run APMS, navigate to `Papers` and run `python ./.APMS/renamePDF.py`

# Manual Instructions
Older academic papers do not always have appropriate metadata stored in the pdf. So, you may have to add a paper manually. To do this, follow the instructions below:
1. Name the file `LastnameYYYY*# - **.pdf`
- `*`: If the author has produced more than one paper in the same year, add an "a" to the first, a "b" to the second, and so on.
- `#`:  Add the other authors after `YYYY*`.
- `**`: Put a brief description of the paper here or copy/paste a few words from the title.


	EXAMPLE - The paper titled:
> CHAU-LAM YU, ANTHONY C. DIDLAKE JR., FUQING ZHANG, AND ROBERT G. NYSTROM, "Asymmetric Rainband Processes Leading to Secondary Eyewall Formation in a Model Simulation of Hurricane Matthew (2016)", 2020,...

It would have the following name: `Yu2020Didlake - Asymmetric Rainband Processes.pdf`

3. Update the biblio.bib file `./.bibliography/biblio.bib`
	a. Use the "LastnameYYYY*# format for the reference ID.

# See Also:
[Automatic Publication Summarization](https://github.com/nrb171/Automatic-Publication-Summarization)

# CHANGELOG 

2023-06-07: Nicholas Barron
- Initial repository creation
 
2023-10-25: Nicholas Barron
- general updates
- Format change to APMS name from renamePDF.
- Integrate with [APS](https://github.com/nrb171/Automatic-Publication-Summarization)

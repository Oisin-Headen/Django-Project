# Breakdown of files:
views.py: contains functions that handle the processing of pages. It can read POST data from a form, or get data from a database to give to a html template

urls.py: tells the app what each url for our site is, and what method to call for it.

models.py: contains our models, used to create and interact with the database. It doesn't look like we need to use SQL, just call methods. We're mostly using CSV and JSON files to store data.

templates/paranoidApp: contains html files, which are processed in the views.py methods. The templates can contian code to be processed, such as a for loop to list database items.

static/paranoidApp: contains extra files, like css and js.

data/: This is the folder which stores our CSV/JSON files. The JSON files contain all the information needed for the survey, and the CSVs contain the survey responses.

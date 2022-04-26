### Scripts for populating db, converting data, and removing data from db

To populate the db with the data for the experiment, first remove all existing
data using the commands in the `delete_all_dbdata.txt` file. Then run the
commands in the `managementcommands.txt` file.

To remove only partcicipants' responses, simply run the commands in the
`delete_all_responses_dbdata.txt` file.

To generate the csv files, type `python3 manage.py shell` in the terminal, then
copy and paste the code in `convert_db2csv.py`.
Otherwise, type `./manage.py shell < utils/scripts/convert_db2csv.py`
in the console.

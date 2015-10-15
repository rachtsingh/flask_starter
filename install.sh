#!/usr/bin/env bash
# this is the install script that makes everything come alive

echo Setting up Python environment...

# create a virtual environment and activate it
virtualenv venv 
source venv/bin/activate

# install the python dependencies - feel free to uninstall if any of these are unnecessary
pip install -r requirements.txt

# set up the database
echo Setting up Postgres database \`flask_template\`

# start postgres
pg_ctl start -l logfile
sleep 2

# ask the user if they'd like to drop the database 'flask_template'
while [[ true ]]; do
    read -n1 -p "\nDo you want to recreate the 'flask_template' database? This will delete the current database, if any [y/n]: " answer
    case $answer in 
        y|Y) 
            break;;
        n|N) 
            exit;;
        *) continue ;;
    esac
done

dropdb flask_template
createdb flask_template
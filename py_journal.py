import os.path
import subprocess
from shutil import copyfile
from datetime import datetime, timedelta


# Finds monthly journal tex file in the journal directory.
def check_file(name):

    if not os.path.isfile(name):
        copyfile('template.tex', name)
    
def user_input(filename):
    
    date = input("Date: ") or get_day_for_entry()
    header = input("Header: ") 

    entry = []
    line = input("Entry: ")
    while line != 'end':
        entry.append(line + "\n")
        line = input("-----> ")
    # bike_info = input("Bike distance: ")

    if date == "yesterday":
        date = get_yesterday_date()

    add_entry(header, date, entry, filename)

# Add a new journal entry to the monthly journal
def add_entry(header, date, entry, filename):

    begin_env = "\\begin{entry}{" + date + "}{" + header + "}\n"
    end_env = "\n\\end{entry}\n\n\\end{document}"
    with open(filename, 'r+') as f:
        content = f.readlines()
        content[-1] = begin_env
        for l in entry:
            content.append(l)
        content.append(end_env)
        f.seek(0)
        
        for line in content:
            f.write("%s" % line)
        f.truncate()
        compile_tex(filename)


# Returns the name for the file 
def get_date_for_filename():
    time = datetime.now()
    return str(time.strftime("%B%Y"))

# Returns the date for the header
def get_day_for_entry():
    time = datetime.now()
    return str(time.strftime("%A, %B %-d"))

# Returns yesterdays date, this is a pretty common one so it gets a special case
def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return str(yesterday.strftime("%A, %B %-d"))

# Compiles the journal
def compile_tex(name):
    subprocess.check_call(['pdflatex', name])

if __name__ == "__main__":

    filename = get_date_for_filename() + ".tex"
    check_file(filename)
    user_input(filename)
    

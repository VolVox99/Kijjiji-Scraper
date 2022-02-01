# Kijjiji-Scraper

![](https://i.ibb.co/GQ6mp5T/2022-01-31-17-25-33.gif)

# Instructions

All terminal commands are highlighted.
Make sure you first have python 3 installed.
You can check this by running "python -V" in the terminal.
If the version it writes is not 3, download python3 and for the instructions, usepython
everywhere instead ofpython.

## Steps for the very first time

1. unzip the downloaded folder
2. Open the terminal
3. Type in "cd" and space 
4. open the terminal and drag (click, hold down andmove mouse) the unzipped folder onto
the terminal
5. It should have pasted the folders path after cdonto the terminal. Press enter
6. type python -m pip install -r requirements.txt and press enter

Every other time you would like to run the script,you need to redo steps 2-4 from the first
time, so your terminal is running in the folder ofthe script.

Now that your terminal is in the folder of the code,you can run the script. You can type
python frontendyinto the terminal and press enterto start the GUI.

This will launch the GUI. You can navigate the pagesof filters through the arrow buttons in
the top right corner, or by pressing on the page name.Once you have entered all the filters
you would like, you can press on the start buttonto take you to the start page. The start
button is displayed below. Then press on the buttonto apply the filters and the script will
start. Information about it’s status will be displayedin the terminal. The filter validation on
the GUI is not very lackluster. If a filter is inthe wrong format, it will write an error message
in the console and the GUI will close. Make sure theinputs are in the correct format. The
format for all the dates is MM/DD/YYYY. In Canadayou may use the format of
DD/MM/YYYY but the GUI uses the format I mentioned.For the city, enter in only the city
name, such as ‘Burnaby’, and press submit. And forthe price simply enter in numbers.


## Output while running

While the script is running, it will output certaininformation about what it is doing. For every
location, it will output “starting on location” wherelocation is the starting link of that location.

After that, the script will output “listings found:number” where number is the amount of listings
found for that city.
If the option to continue the file from the optionspage is used, there is a slight difference in that
for every city it will instead output “new listings(non duplicates) found: number” where number
is the number of new listings that were found. Theinformation is actually the same for the flag or
not: the number of listings found. But with the flagit is more useful as you can know which cities
have had new posting, since many may not have if thescript has been run recently again. If it
outputs 0 as the number, that means all the listingswere already contained in the output file and
nothing new has been posted. The way listings aredifferentiated is through their unique ID on
the website.

Then it will continually output a number that keepsincreasing. Each number is one listing being
written to the file.


Every so often, it will continually output “sleeping”instead of a number. This means the script
has temporarily stopped making requests to the website'sserver because they block too many
requests. Do not worry, it will continue after 20-30seconds once the server allows it once more.

Finally it will output “FINISHED”. It is done runningand you can now open the output file to view
the results. You cannot have the file open in somethingsuch as excel while the script is running
or it will error as it will not be able to write toit.


If it ever displays something cryptic such as

### Traceback (most recent call last):

### File "C:\Users\\main.py", line 99, in <module>

### main()

### File "C:\Users\main.py", line 35, in main

### with open(outFile, 'r+' if continue_file else 'w',newline = '', encoding = 'utf-8') as


### csvfile:

### PermissionError: [Errno 13] Permission denied: 'output.csv'

and stops running, that means an error has occurred.It is unlikely for any unaccounted errors to
occur, since I addressed any that had the possibilityof occurring during my testing, but
something unexpected can always happen. To addressthis, copy paste the entire error
message, or take a screenshot, and contact me. I willfix it and get back to you.

The output does not need to be monitored, it is justauxiliary information while it is running.
Since there are many total listings for all the citiesinvolved, and each needs to be meticulously
scraped individually, it takes some time to finishrunning. It takes a second or two per listing, and
in my testing I found there to be around 1000 forall the cities, although this number will always
vary. So that would take about 30 minutes. I recommendsimply leaving the script running and
coming back when it's done.
If you run into any issues, or have any additionalquestions, feel free to reach out to me again.



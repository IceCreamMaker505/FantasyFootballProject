#Before starting, run the commands to activate virtual environments then create a .py file 
#source venv/Scripts/activate
#If the command doesn't work,try...
#source venv/bin/activate
#pip install beautifulsoup4 html5lib

import requests
#imports requests which we did in API

from bs4 import BeautifulSoup as BS 

#import new library called BS4, de facto web scraping library for Python.
#This will help parse through the html we give it from our request we make with "requests"

import pandas as pd
from sys import argv

#From sys module, we import object called argv

letter_url = 'https://www.pro-football-reference.com/players/{letter}/'
players_url = 'https://www.pro-football-reference.com/players/{letter}/{player_code}.htm'

#Basic URL format for our archive page and player page
#Unformatted for now as we'll be using the "format"string method later once we know te letter and player_code values

player_first_name = input("What is the player's first name? ")
player_last_name = input("What is the player's last name? ")

#input is a built in function in Python that allows command line input from a user
#Returns the user response as the return value of function

inputted_player_name = player_first_name + " " + player_last_name

#We build our players name by concatenating three strings-
#the strings are: player_first_name, an empty string with a space, and player_last_name
#Once we iterate therough the list of players on the archive page, we'll use this value to check if a player on the archive page is the player we are trying to get data about

#Archice page is organized by player last initial
letter_to_request = player_last_name[0].upper()

#This is the page we are requesting from to find the player codes
#We are getting our players last initial
#Stings are able to be indexed much like lists are in Python so we are able to grab the first character of a string using [0]
#string method still applies
#We use the string method upper to convert our last initial to a capital letter
#We then use that variable to format our archive page string, or "letter_url"
#Once we find the player codes, we can then make a request to the player page

letter_url = letter_url.format(letter=letter_to_request)

res = requests.get(letter_url)

#We make the request to our archive page for whatever player we are requesting

soup = BS(res.content, 'html.parser')

#We pass this response in to our BeautifulSoup class
#Remember we imported BeautifulSoup as BS, which is meant to help us parse our HTML file
#This is why we pass in res.content as our first arguemt to this class
#In the API chapter, we got back an JSON string, in this chapter, we are getting an HTML file
#So, when we access res.content, its in the form of HTML
#As our second content, we pass in 'html.parser' to tell bs to parse the first argument, our content, as an HTML file
                
                #Pause for lesson

#Before we move on, remember when I talked briefly about "a" tags and how they are just links?
#They way they link to other pages is through an attribute each "a" tag has, an href
#The href is what is going to contain our player code so we are going to need to access it in a minute
#Another thing about HTML you should know is that elements and tags in an HTML file can have id's
#These id's are normally meant for use in CSS and JavaScript to be able to identify elements in an HTML page.
#id's should alwasy be unique to a page, which make them extremely useful for our purposes as well
#Last thing is that you can view the HTML page you want by right clicking on a page and clicking "inspecting element"
#We'll be using inspect element to view the HTML of the page we want to scrape and then finding where our desired data lives and seeing if there's any unique id's that we can use to make the web scraping easier

        #Video
#Here's the process I go through here. 
# You can see that all of the values we need are enclosed in this giant section tag which has an id of all_players. 
# Within that section tag, we have a collection of p tags, one for each player. 
# Underneath each p tag, we have a corresponding a tag, and the information in the href of the a tag is what we really need.

#Using BS, we can grab our entire section by the id using soup's metod called find
#We give it a keyword argument of id to tell BS we want to find the HTML element with the id of "all_players"
#We now have another BS object we can manipulate and has it's own set of methods and attributes.

#Remember, underneath this section we have a collection of p tags that corresponds to each player.
#We use the BS method 'find_all" to find all those values
#This object we save to our p_tags variable is an iterable now, so we can now create a list comprehension to map a function across it.

section = soup.find(id="all_players")
p_tags = section.find_all('p')

#In line 22, we find all "a" tags in our collection of 'p' tages using the method find again
#We set the keyword argument "href=True" to tell BS to keep our href in there
#Our new variable "a_tags" is now a collection of "a" tags with their hrefs
a_tags = [p.find('a', href=True) for p in p_tags]

#We are almost done, just bare with me
#Now we have to iterate over our "a_tags" collection and get our player name for each "a" tag and href(which contains our player code)

for a in a_tags:
   
    #We grab the player name using 'a.content[0].
    #This is simply giving us the content within the "a" tag
    #An "a" tag in HTML is composed of more than a simple href
    #It also contains some content in between the opening and closing tag to give the link some text
    #This text is our player name
    #We will be using this variable in an if statement to check if it is equal to the player naem we gave our terminal through input
    #If it is, run the block

    player_name = a.contents[0]

    #We grab our player code
    #We grab the href using the get method BS comes with, which is different then other get methods
    #Here, 'get' gets our href, which is a string.
    #It looks like '/players/B/BradTo00.htm' 
    #We are only interest in the player code, which is the "BradT00"
    #So, we split our string by '/', take the last element of our list
    #Then, we split it one more time on'.' and take the first element of that list
    #We went through a similar process when we ran a function across our "Player" column in pandas to format our player names correctly
    #We set this value equal to a variable we call "player_code"
    #We will be using this value soon to build our player_url

    #if our player name we inputted to the terminal is equal to the player we are on when iterating through our anchor tags('a' tags)
    #then we want to run our if block
    
    player_code = a.get('href').split('/')[-1].split('.')[0]

    #We use the strip sting method and tack it on to remove any trailing white space
    #We also want to stop our loop dead in its tracks after we run the code in the if block, if the if block runs
    #Forwarding to the end, we use break to be able to do this
    #break stops a loop while return stops a function
            
            #Lets Recap
    
    #In order, we have build and format our player URL
    #We made a request to that URL
    #We follow the same process we did for the archive/letter page
    #We find the first table on our HTML response content
    #We "get" our id, much like we "got" our href for our anchor tag
    #We dont know what our table id is yet, it seems it could be either rushing_and_receiving, passing, or receiving_and_rushing
    #We convert this HTML object to a string, we'll be using read_html that allows us to convert this HTML table to DF
    
    if player_name.strip() == inputted_player_name:
        player_url = players_url.format(letter=letter_to_request, player_code=player_code)
        res = requests.get(player_url)
        soup = BS(res.content, 'html.parser')
        table = soup.find('table')
        table_id = table.get('id')
        table = str(table)
    #We use the function read_html to read our HTML and convert it to a DF
    #we have only table so we tack on a [0] to grab the first value in our list

        df = pd.read_html(table)[0]
    #We check how many levels our DF column index has
    #we want to get rid of our column indexes to avoid troublesome
        
        if df.columns.nlevels > 1:
    #We can access the amount of levels our column row has by accesing the attribute df.columns.nlevels
    #If their is more than one column, we want to remove it
            df.columns = df.columns.droplevel(level=0)
    #The general format in which we alter our columns is by settng the columns equal to itself
    #We set df.columns equal to df.columns but with a level dropped
    #We do this with the method droplevels
    #It takes an argument of a level, which we provide a value of 0
    #By providing 0, we are saying drop the top level or first level which has an index of 0
    #In python, everything you need to find an index starts with an index of 0
        
        df.fillna(0, inplace=True)
    #We are using a pandas DF method called fillna to fill all NA values in our DF with the value of 0

        df['Year'] = df['Year'].apply(lambda x: x.split('*')[0])

        #We format our 'year' column much like we did our 'player' column
        #If you examine our DF at this point, use print(df.head()), print must be used unlike in Google Colab
        #This line, like previous, is only removing special characters like *

        columns_to_drop = []

        print(table_id)
        
        #We start to use our variable we set to table_id to manimpulate our DF

        #if blocks refer to the id option that are being used mentioned earlier
        #passing, receiving_rushing, or rushing_receiving
        if table_id == 'passing':

            df.rename({
                'Yds': 'PassingYds',
                'Yds.1': 'YdsLostToSacks'
            }, axis=1, inplace=True)

            columns_to_drop = [
                'TD%', 'Int%', 'Y/A', 'AY/A', 'Y/C', 'Y/G', 'NY/A', 'ANY/A', 'Sk%', 'AV'
            ]

        #if blocks goes back to whatever id is being used
        #.iloc allows us to grab cross sections of a DF
        if table_id == 'receiving_and_rushing':
            df['ReceivingYds'] = df['Yds'].iloc[:,0]
            df['RushingYds'] = df['Yds'].iloc[:, 1]
            df['Receiving1D'] = df['1D'].iloc[:, 0]
            df['Rushing1D'] = df['1D'].iloc[:, 1]
            df['RecevingTD'] = df['TD'].iloc[:, 0]
            df['RushingTD'] = df['TD'].iloc[:, 1]

            columns_to_drop = [
            'Yds', 'Y/G', 'Y/A', 'R/G', 'Y/Tch', 'YScm', 'Ctch%', 'Y/Tgt', 'Y/R', 'A/G', '1D', 'RRTD', 'TD'
            ]

        if table_id == 'rushing_and_receiving':
            df['ReceivingYds'] = df['Yds'].iloc[:,1]
            df['RushingYds'] = df['Yds'].iloc[:, 0]
            df['Receiving1D'] = df['1D'].iloc[:, 1]
            df['Rushing1D'] = df['1D'].iloc[:, 0]
            df['RecevingTD'] = df['TD'].iloc[:, 1]
            df['RushingTD'] = df['TD'].iloc[:, 0]

            columns_to_drop = [
            'Yds', 'Y/G', 'Y/A', 'R/G', 'Y/Tch', 'YScm', 'Ctch%', 'Y/Tgt', 'Y/R', 'A/G', '1D', 'RRTD', 'TD'
            ]

        df.drop(columns_to_drop, axis=1, inplace=True)    

        #Lastly, we circle back to something we imported earlier called argv
        #argv is a shorthand for argument vector and vector is a fancy word for a list
        #The arguemnt vector is simply a list of the arguments you provide to the command line when you run a python script
        #if you were to run the command python webscraping.py, the argument vector would simply look like the following...
        #['webscraping.py'] a list with the length of 1
        #However, run a command to run a python script using...
        #python webscraping.py--save, the argv would look like this...
        #['webscraping.py','--save'] a list with the length of 2

        try:
            if argv[1] == '--save':
                filename = (player_first_name+player_last_name).upper() + '.csv'
                df.to_csv('data/{}'.format(filename)) # saves to a folder called data.
        
        #Here, we run an if block to check if the user would like to save this DF we got back from this whole scraping process to a new CSV file
        #We wrap this all in a try/except block and check if the second argument in our argv is equal to '--save'
        #if it is not, or if there is an IndexError(meaning the user only ran the command "pyton webscraping.py"), then we print out to our console df.tail()
        except IndexError:
            print(df.tail())

        break
        #We save a pandas DF to a CSV file using the pandas function df.to_csv
        #In line 87, we call our function and format a string with 'data/{}'.format(filename).
        # This means save the file with file name filename to a directory that already exists called data. 
        # If you have not already, create a new directory in the same level this file is located in called data to save your CSV files to this folder. 
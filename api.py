import sys #sys is built in library(the bread and butter)


try: #underneath the block try block, you "try" a piece of code that you think might give you an error
    #In my case, I didn't install request when running
    import requests
except ImportError:
    #Write specific error
    #We are looking for an ImportError. If there is an import error, we want to stop the script
    sys.exit("requests was not properly installed. Try again. Are you sure you are in venv?")
#exit() exit our script if the block of code underneath except is ran
#Stops script dead, much like an error and sends messaged typed
def get_fantasy_points(player,pos):
    #we write a little function to get a player fantasy points from JSON object
    #Our JSON is a list of dictionaries with dictionaries nested within
    if player.get("position")==pos:
        #check if our player has the correct position with the if block
        #pos is our new variable to be used instead of position
        return player.get("fantasy_points").get("ppr")
        #If they do, we chain two get methods to get back our desired result.
        #get. is pretty straightforward

pos="WR"
year="2019"
week= 1

res=requests.get('https://www.fantasyfootballdatapros.com/api/players/{0}/{1}'.format(year, week))
#We build our API endpoint using the built in method format
#The endpoint requires a season number and and week number which we set abouve
if res.ok:
    #Status code 200, true or ok(500 or 404 denied)
    #Pass URL into our request.get method
    #Requests module has a function called get which allows us to make an HTTP GET request
    #Remember, a GET request is what you do everyday when you request a resource form a webpage
    #Instead here, we are requesting a JSON object that we can use in our code
    print("Season {0}, week{1} VOR for {2}s".format(year, week, pos))
    print('-'*40)
    #Season{0} reference back to api url
    #We print out to the terminal some info about our script
    #numbers are matched to format() order
    #Strings can be multiplied just like integers
    #'-'*40 means give us '-' 40 times, please make sense later.

    data = res.json()
    #.json() to convert our response to JSON so we can use it in code

    wr_fantasy_points=[get_fantasy_points(player,pos) for player in data]
    #We use our little helper function to extract fantasy_points for each of our player objects
    #fantasy_points is how it looks on api
    #newly created json object is just a python list now
    wr_fantasy_points=list(filter(lambda x: x is not None, wr_fantasy_points))
    #filter out any values which have the value of None
    mean = lambda x: sum(x)/len(x)
    #we write a lambda and save it as a variable in order to calculate average of a list
    #when in doubt, always assume you can something to a variable
    #We can reference this function by using mean()


    replacement_value=mean(wr_fantasy_points)

    for player in data:
        if player.get("position")==pos:
            vor=player.get("fantasy_points").get("ppr")-replacement_value
            print(
                player.get("player_name"), "had a VOR of", vor
            )

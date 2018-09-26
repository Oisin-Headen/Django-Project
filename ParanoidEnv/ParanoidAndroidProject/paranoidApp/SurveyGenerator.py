# Author: Simon Jones
# Date Created: 23/09/2018
# Purpose: Generate random survey data for use in analytics.
# Version: 1.0
# Last Modified: 23/09/2018

from random import randint
import csv

def generateSurveyData():
    numSurveyResponses = 1000

    try:
        # Newline argument is required for later Python versions, otherwise a gap is inserted between each row
        with open('surveyData.csv', 'w', newline = '') as csvfile:

            csvline = csv.writer(csvfile, dialect = 'excel', delimiter = ',')

            # Get question header data for CSV file
            surveyQuestions = getSurveyQuestions()
            csvline.writerow(surveyQuestions)

            # Generate individual survey responses
            surveyCounter = 0
            while surveyCounter < numSurveyResponses:
                surveyAnswers = getSurveyResponse()
                csvline.writerow(surveyAnswers)
                surveyCounter += 1

    except FileNotFoundError:
        print('Cannot find the file specified.')

    except PermissionError:
        print('Permission denied to open the file. Please make sure it is not already open.') 

# Function to g
def getSurveyResponse():
    cinema = getCinema()
    regularCinema = getYesNo()
    day = getDay()
    sessionConvenience = getLikert("Convenience")
    travelTime = getVariableData("Travel Time")
    movieFrequency = getVariableData("Movie Frequency")
    goldClass = getGoldClass(cinema)
    overallCleanliness = getRating()
    screenSize = getRating()
    pictureQuality = getRating()
    soundQuality = getRating()
    seatQuality = getRating()
    temperatureQuality = getLikert("Temperature")
    staffLevel = getLikert()
    staffQuality = getRating()
    bathroomCleanliness = getRating()
    vrewardsMember = getYesNo()
    purchaseFoodDrinks = getYesNo()

    # Assign NA to these variables, as their content depends on other questions below
    foodSelection, foodQuality, foodPrice, username, email = ('NA',) * 5
    
    if purchaseFoodDrinks == "Yes":
        foodSelection = getRating()
        foodQuality = getRating()
        foodPrice = getRating()
    
    wouldRecommend = getRating()
    giftUser = getYesNo()

    receiveOffers = getYesNo()
    
    if receiveOffers == "Yes":
        username = getName()
        email = getEmail(username)

    return (cinema, regularCinema, day, sessionConvenience, travelTime, movieFrequency, goldClass, overallCleanliness, screenSize, pictureQuality, soundQuality, seatQuality, temperatureQuality, staffLevel, staffQuality, bathroomCleanliness, vrewardsMember, purchaseFoodDrinks, foodSelection, foodQuality, foodPrice, wouldRecommend, giftUser, receiveOffers,username, email)

def getSurveyQuestions():
    surveyQuestions = ('Which village cinema did you last visit to watch a movie?',
    'Is this the regular Village cinema which you attend?',
    'Which day of the week did you attend the Village cinema on your last visit?',
    'How convenient were the available session times for the movie you watched?',
    'Approximately how long did it take for you to reach the cinema from home on your last visit?',
    'Including your most recent visit, how frequently have you been to the movies in the past 3 months?',
    'Was the session you last attended a Gold Class screen?',
    'How would you rate the overall cleanliness of the cinema?',
    'How would you rate the size of the screen in your last movie session?',
    'How would you rate the picture quality of the screen in your last movie session?',
    'How would you rate the quality of the sound for the cinema you were in?',
    'How would you rate the comfort and size of your seat for the cinema you were in?',
    'How would you rate temperature in the cinema you were in?',
    'Staffing levels were adequate with reasonable wait times',
    'How would you rate the friendliness of our staff?',
    'How would you rate the cleanliness of the amenities, such as bathrooms?',
    'Are you a Vrewards member?',
    'Did you purchase any food or drinks from our Snack Bar or Gold Class menu?',
    'How would you rate the overall selection of our food?',
    'How would you rate the quality of our food?',
    'How would you rate the price of our food?',
    'Based on your last experience, how likely would you recommend the Village cinema you visited to a friend or colleague?',
    'Have you ever received or would you gift someone a movie experience?',
    'Would you like to receive news and special offers from Village?',
    'What is your name?',
    'What is your email address?'
    )
    # Future question for free text: 'Is there anything else you would like to share about your cinema experience?'
    return surveyQuestions

def getYesNo():
    answer =  "No" if randint(0,1) == 0 else "Yes"

    return answer

def getDay():
    daysOfWeek = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

    return daysOfWeek[randint(0, len(daysOfWeek) - 1)]

def getRating():
    return randint(0,10)

def getLikert(scaleType = "Traditional"):
    scaleDescriptions = ''

    if scaleType == "Convenience":
        scaleDescriptions = ('Very Inconvenient','Inconvient','Indifferent','Convenient','Very Convenient')
    elif scaleType == "Temperature":
        scaleDescriptions = ('Way too cold','A little cool','Just right','A little warm', 'Way too hot')
    else:
        scaleDescriptions = ('Strongly disagree','Disagree','Neither agree nor disagree','Agree','Strongly agree')

    return scaleDescriptions[randint(0,len(scaleDescriptions) - 1)]

def getVariableData(dataType = "Unknown"):
    variableDescriptions = ''

    if dataType == "Travel Time":
        variableDescriptions = ('Less than 10 minutes','Less than 30 minutes','Less than 1 hour','More than 1 hour')
    elif dataType == "Movie Frequency":
        variableDescriptions = ('Once', '2-3 times', '4-6 times','More than 6 times')
    else:
        return variableDescriptions

    return variableDescriptions[randint(0,len(variableDescriptions) - 1)]
        
def getCinema():
    cinemaLocations = ('Airport West','Albury','Bendigo','Century City','Coburg Drive-In','Crown','Doncaster','Eastlands','Fountain Gate','Geelong','Glenorchy','Hobart','Jam Factory','Karingal','Knox','Launceston','Morwell','Plenty Valley','Rivoli','Rosebud','Shepparton','Sorrento','Southland','Sunshine','Warragul','Warnambool','Werribee')
    
    return cinemaLocations[randint(0, len(cinemaLocations) - 1)]

def getGoldClass(cinema):
    goldClassLocations = ('Albury','Bendigo','Century City','Crown','Doncaster','Fountain Gate','Geelong','Hobart','Jam Factory','Karingal','Knox','Plenty Valley','Rivoli','Southland','Sunshine','Werribee')

    if cinema in goldClassLocations:
        return getYesNo()
    else:
        return "NA"

def getName():
   
   firstNames = ('Grace','Sarah','Amelia','Jayce','Penelope','Mateo','Isaiah','Henry','Ava','Aiden','Grayson','Ella','Paisley','Ethan','Jacob','Matthew','Jack','Cameron','Camilla','William','Jayden','Elijah','Carter','Samuel','Arianna','Caleb','Madelyn','Isaac','Luna','Isabelle','Chloe','Ellie','Liam','Luke','Nicholas','Kinsley','Owen','Aria','Olivia','Emily','Abigail','Mila','Harper','Elizabeth','Avery','Dylan','Hailey','Zoe','Hannah','Nora','Lucas','Kaylee','Leo','James','Michael','Sebastian','Lincoln','Jackson','Charlotte','Oliver','Scarlett','Addison','Ryan','Mason','David','Josiah','Noah','Daniel','Levi','Wyatt','Alexander','Caden','Adalyn','Eliana','Benjamin','Nathan','Evelyn','Brooklyn','John','Victoria','Maidson','Sophia','Muhammad','Adam','Mia','Leah','Layla','Logan','Aubrey','Lily','Aaliyah','Julian','Connor','Riley','Emma','Isabella','Gabriel','Mackenzie','Anna','Maya')
   lastNames = ('Adams','Allen','Anderson','Bailey','Baker','Barnes','Bell','Bennett','Brooks','Brown','Butler','Campbell','Carter','Chen','Clark','Collins','Cook','Cooper','Cox','Cruz','Davis','Diaz','Edwards','Evans','Fisher','Flores','Foster','Garcia','Gray','Green','Hall','Harris','Hill','Howard','Hughes','Jackson','James','Jenkins','Johnson','Jones','Kelly','King','Kumar','Lee','Lewis','Li','Long','Lopez','Martin','Miller','Mitchell','Moore','Morales','Morgan','Morris','Murphy','Myers','Nelson','Nguyen','Parker','Patel','Perez','Perry','Peterson','Phillips','Powell','Price','Reed','Reyes','Richardson','Roberts','Robinson','Rodriguez','Rogers','Ross','Russell','Ryan','Sanchez','Sanders','Scott','Singh','Smith','Stewart','Sullivan','Taylor','Thomas','Thompson','Torres','Turner','Walker','Wang','Ward','Watson','White','Williams','Wilson','Wood','Wright','Young','Zhang')
   
   fullName = firstNames[randint(0, len(firstNames) - 1)] + ' ' + lastNames[randint(0, len(lastNames) - 1)]

   return fullName
   
def getEmail(username):
    emailDomains = ('@gmail.com', '@yahoo.com.au','@hotmail.com', '@msn.com', '@live.com.au', '@outlook.com', '@bigpond.com', '@mail.com', '@optusnet.com.au', '@bigpond.net.au', '@mailinator.com')
    email = username.replace(' ','.') + emailDomains[randint(0, len(emailDomains) - 1)]

    return email

generateSurveyData()
from helper import *

DATE = "2020-09-07"
ODDS_DATE = DATE[:4] + DATE[5:7] + DATE[-2:]

# Get the page source from MoneyPuck
MP_url = "http://moneypuck.com/index.html?date="+DATE
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/noahrowe/Desktop/Other/chromedriver", options=options)
driver.get(MP_url)

# Loop to grab todays teams
games = driver.find_element_by_xpath('//*[@id="includedContent"]/table/tbody')
teams = games.find_elements_by_xpath('//img')
temp_team_list = [t.get_attribute('alt') for t in teams if t.get_attribute('alt')!=""]
team_list = []
for i in range(int(len(temp_team_list)/2)):
    team_list.append([temp_team_list[i*2], temp_team_list[i*2+1]])

games = driver.find_element_by_xpath('//*[@id="includedContent"]/table/tbody')
probs = games.find_elements_by_xpath('//h2')
probs = [p.text for p in probs ]

game_probs = []
temp_game_probs = []
for i in range(len(probs)):
    p = probs[i]
    if p[-1] == "%":
        temp_game_probs.append(round(float(p[:-1])/100, 4))
        if len(temp_game_probs) == 2:
            game_probs.append(temp_game_probs)
            temp_game_probs = []


# Create a dict object from all the data we now have
main = []
for i in range(len(team_list)):
    tempDict = {}
    teams = team_list[i]
    probs = game_probs[i]
    tempDict["team1"] = teams[0]
    tempDict["team2"] = teams[1]
    tempDict["p1"] = probs[0]
    tempDict['p2'] = probs[1]
    main.append(tempDict)
    

####################### GET TEAMS FROM ODDS SITE #######################
betting_url = "https://classic.sportsbookreview.com/betting-odds/money-line/?date="+ODDS_DATE

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/noahrowe/Desktop/Other/chromedriver", options=options)
driver.get(betting_url)

# Loop to grab basketball matchups
bball = driver.find_element_by_xpath('//*[@id="OddsGridModule_7"]')
bball = bball.find_element_by_xpath('//*[@id="sport-6"]/div/div/div/div[2]/div[4]')
teams = bball.find_elements_by_class_name("team-name")
team_list = []
print("Hockey Games to Bet On:")
for i in range(int(len(teams)/2)): # Betting odds grid container object
    team1, team2 = teams[i*2].text, teams[i*2+1].text
    print("{} vs {}".format(team1, team2))
    team_list.append([team1, team2])
    
AVAL_HOCKEY_GAMES = len(team_list)

####################### GET ODDS LISTS #######################
sites = []
## PAGE ONE
# Get the list of sites
bball = driver.find_element_by_xpath('//*[@id="OddsGridModule_7"]')
odds = bball.find_element_by_class_name("eventLine-book-value")
odds = odds.find_elements_by_xpath("//div[contains(@class, 'book')]")
sites.extend(odds[0].text.splitlines())

# Get the list of odds
active_games = driver.find_element_by_xpath('//*[@id="sport-6"]/div/div/div/div[2]/div[4]').text.splitlines()
space_indexs = np.where(np.array(active_games)=="")[0]
game_odds = []
for index in space_indexs:
    temp_odds = active_games[index+1:index+21]
    game_odds.append([[temp_odds[2*i], temp_odds[2*i+1]] for i in range(int(len(temp_odds)/2))])
    
odds_list = game_odds
# Change the page to the other sites
next_button = driver.find_element_by_xpath('//*[@id="feedHeaderCarousel"]/div[1]/a[2]/span')
next_button.click()
time.sleep(2)


## PAGE TWO
# Get the list of sites
bball = driver.find_element_by_xpath('//*[@id="OddsGridModule_7"]')
odds = bball.find_element_by_class_name("eventLine-book-value")
odds = odds.find_elements_by_xpath("//div[contains(@class, 'book')]")
sites.extend(odds[0].text.splitlines())

# Get the odds for this page
active_games = driver.find_element_by_xpath('//*[@id="sport-6"]/div/div/div/div[2]/div[4]').text.splitlines()
space_indexs = np.where(np.array(active_games)=="")[0]
game_odds = []
for index in space_indexs:
    temp_odds = active_games[index+1:index+21]
    game_odds.append([[temp_odds[2*i], temp_odds[2*i+1]] for i in range(int(len(temp_odds)/2))])
    
for i in range(len(game_odds)):
    odds_list[i].extend(game_odds[i])
    
# Change the page to the other sites
next_button = driver.find_element_by_xpath('//*[@id="feedHeaderCarousel"]/div[1]/a[2]/span')
next_button.click()
time.sleep(2)

## PAGE THREE
# Get the list of sites
bball = driver.find_element_by_xpath('//*[@id="OddsGridModule_7"]')
odds = bball.find_element_by_class_name("eventLine-book-value")
odds = odds.find_elements_by_xpath("//div[contains(@class, 'book')]")
sites.extend(odds[0].text.splitlines()[1:])

# Get the odds for this page
active_games = driver.find_element_by_xpath('//*[@id="sport-6"]/div/div/div/div[2]/div[4]').text.splitlines()
space_indexs = np.where(np.array(active_games)=="")[0]
game_odds = []
for index in space_indexs:
    temp_odds = active_games[index+3:index+21]
    game_odds.append([[temp_odds[2*i], temp_odds[2*i+1]] for i in range(int(len(temp_odds)/2))])
    
for i in range(len(game_odds)):
    odds_list[i].extend(game_odds[i])

if AVAL_HOCKEY_GAMES != 0:
    odds_list[0] = odds_list[0][:-1]


for i in range(len(odds_list)):
    for j in range(len(odds_list[i])):
        for k in range(len(odds_list[i][j])):
            odds_list[i][j][k] = round(convert(int(odds_list[i][j][k])), 2)


###### LOOP THROUGH EACH GAME AND DECIDE WHETER A BET SHOULD BE PLACED ######
mySiteIndex = np.where(np.array(sites)=="SportsInteraction")[0][0]
for i in range(len(odds_list)):
    
    myOdds1 = odds_list[i][mySiteIndex][0]
    myOdds2 = odds_list[i][mySiteIndex][1]
    myProb1, myProb2 = 1./myOdds1, 1./myOdds2
    #myProb1, myProb2 = myProb1/(myProb1+myProb2), myProb2/(myProb1+myProb2)
    
    game = main[i]
    MP1 = game["p1"]
    MP2 = game["p2"]

    print("\nMy {} odds and implied probability: {:.2f}, {:.2f}%".format(team_list[i][0], myOdds1, myProb1))
    print("MoneyPuck {} prob: {:.2f}%".format(team_list[i][0], MP1))
    print("")
    bet(team_list[i][0], team_list[i][1], MP1, MP2, myOdds1, myOdds2)
    print("")
            
         

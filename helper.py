import numpy as np
from selenium import webdriver
import time

CAP = 30
FRAC = 1./4

# Decide what to bet and how much
def kelly(capital, win_prob, bet_odds, moneyLine=False):
    if moneyLine:
        # Convert moneyline to bet odds
        if bet_odds > 0:
            bet_odds = bet_odds / 100. 
        else:
            bet_odds = -100. / bet_odds 
    else:
        # Subtract 1 from usual decimal odds
        bet_odds -= 1

    F = (win_prob * (bet_odds + 1) - 1)/bet_odds
    if F > 0:
        return capital * F  # Conservative Kelly
    else: 
        return 0
    
def bet(t1, t2, p1, p2, d1, d2):
    if (p1 + p2) - 1.> 0.01:
        print("Wrong probs")
    
    t1_kelly = kelly(CAP, p1, d1)
    t2_kelly = kelly(CAP, p2, d2)
    if t1_kelly>0: 
        print("Bet ${:.2f} on {}".format(FRAC*t1_kelly, t1))
    elif t2_kelly>0: 
        print("Bet ${:.2f} on {}".format(FRAC*t2_kelly, t2))
    else:
        print("Odds are good")
            
# Convert from moneyline to decimal
def convert(ml):
    return ml/100. + 1 if ml>0 else -100./ml + 1
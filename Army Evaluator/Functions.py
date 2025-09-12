#Get this up and working, then add the corner cases as they're mentioned

# calculate and store best at each range

# things to look at
# firepower at each range
# firepower into white saves -> red surging saves
# impact/crit
# total health
# effective health
# suppression outpot -need to factor gunslinger and maybe command cards, and demoralize for this. Raiding party leader too

#firepower at range could work on a chart. not sure about the rest

#DTs need to auto equip both

#special cases:
#arsenal
#overrun
#beam
#gunslinger
#extra health upgrades
#crit from maul saber and frags
#expend weapons? rockets and flamethrowers
# commando bubbles

#any gear weapons:
#boba things
#din things

#repair and restore

#double mini upgrades in riot and arf



import json

cards = {}
with open("Army Evaluator\\Data\\cards.json","r") as file:
    cards = json.load(file) 


def FirePower():
    pass


def WeaponsCheck():
    for card in cards:
        if cards[card]["cardType"] == "unit":
            try:
                weapons = cards[card]["weapons"]
                if len(weapons) == 0:
                    print(cards[card]["cardName"], card)
            except KeyError:
                print(cards[card]["cardName"], card)

def WeaponKeywordCheck():
    pass

def KeywordCheck():
    for card in cards:
        if cards[card]["cardType"] == "upgrade":
            if cards[card]["cardSubtype"] in ["heavy weapon", "personnel", "weapon", "ordnance", "armament", "hardpoint"]:
                if not "weapons" in cards[card]:
                    print(cards[card]["cardName"], card)

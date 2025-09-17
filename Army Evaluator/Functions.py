#Get this up and working, then add the corner cases as they're mentioned

# firepower into white saves -> red surging saves
# impact/crit

# suppression output -need to factor gunslinger and maybe command cards, and demoralize for this. Raiding party leader too

#firepower at range could work on a chart. not sure about the rest

#DTs need to auto equip both

#special cases:
#extra health upgrades
#other masteries as well

#repair and restore

#double mini upgrades in riot and arf

#what logic for clone commando bubbles?
#defense always
#offense like x/6? so that it's 50% of the time if you have 3 bubbles?

import json
import random

GROUP_WEAPONS = ["gear", "hardpoint", "armament", "generator", "ordnance", "pilot", "training", "crew"]
SINGLE_WEAPONS = ["personnel", "squad leader", "heavy weapon"]
EXTRA_MINI = ["personnel", "squad leader", "heavy weapon"]



CARDS = {}
with open("Army Evaluator\\Data\\cards.json","r") as file:
    CARDS = json.load(file) 

ttsUnitToCards = {}
ttsUpgradeToCards = {}
for card in CARDS: # don't need to create the whole thing for one list
    name = CARDS[card]["cardName"]
    if "title" in CARDS[card]:
        name = name + " " + CARDS[card]["title"]
    if "ttsName" in CARDS[card]:
        name = CARDS[card]["ttsName"]
    if CARDS[card]["cardType"] == "unit":
        ttsUnitToCards[name] = card
    elif CARDS[card]["cardType"] == "upgrade":
        ttsUpgradeToCards[name] = card


def GetListFromJSON():
    global SAMPLE_LIST
    for unit in SAMPLE_LIST["units"]:
        unitID = ttsUnitToCards[unit["name"]]
        print(CARDS[unitID]["cardName"])
        
        for upgrade in unit["upgrades"]:
            upgradeID = ttsUnitToCards[upgrade]
            print("--" + CARDS[upgradeID]["cardName"])    

##################### IMPLEMENTED #####################
#aims
#aim priority logic
#weapon choice per range band
#single thrower grenades
#surge tokens
#precise
#aims applied for: independent, steady, charge, relentless, tactical
#yoda (ataru)
#frag crit
#dark trooper double attacks
#gunslinger -- attacks again with one less aim. boom. done.

################### NOT IMPLEMENTED ###################
#any gear weapons: boba/din/gar
#arsenal
#Beam  -- how to choose between saber weapons and beam?
#saber throw
#steady/relentless (charge?) range increase
#should treat steady as 1 range band further it's kinda one range further OR one aim.... hmm....
#crit from maul saber
#expend weapons? rockets and flamethrowers
#overrun could call this range 0.5 or range 0 with melee

def FirePower(filePath):
    sampleList = {}
    with open(filePath,"r") as file:
        sampleList = json.load(file)

    allHitsAtRange = [0,0,0,0,0,0]
    for u in sampleList["units"]:
        unit = CARDS[ttsUnitToCards[u["name"]]]
        hitsAtRange = [0,0,0,0,0,0]
        upgrades = []
        print(unit["cardName"])
        for p in u["upgrades"]:
            upgrades.append(CARDS[ttsUpgradeToCards[p]])
    
        for r in range(0,len(hitsAtRange)):
            print("--" + str(r) + "--")
            surge = unit["stats"]["hitsurge"] != ""
            eligibleWeapons = []
            chosenWeapons = []
            miniCount = unit["stats"]["minicount"]
            for weapon in unit["weapons"]:
                if WeaponInRange(weapon, r):
                    eligibleWeapons.append(weapon)
            for upgrade in upgrades: #find all eligible equipped weapons
                if upgrade["cardSubtype"] in GROUP_WEAPONS and "weapons" in upgrade:
                    for weapon in upgrade["weapons"]:
                        if WeaponInRange(weapon, r):
                            eligibleWeapons.append(weapon)

            hitsPerEligible = []
            for weapon in eligibleWeapons:
                hitsPerEligible.append(WeaponExpectedHits(weapon, surge))
            if len(hitsPerEligible) == 0:
                hitsPerEligible.append(0)

            #need to have all weapons first to be able to choose
            for upgrade in upgrades: #choose if using heavy weapons (that are adding bodies as well)
                if upgrade["cardSubtype"] in SINGLE_WEAPONS:
                    if "weapons" in upgrade:
                        chosenWeapon = {}
                        for weapon in upgrade["weapons"]:
                            if WeaponInRange(weapon, r):
                                if "Sidearm" in weapon["keywords"]:
                                    chosenWeapon = weapon
                                elif WeaponExpectedHits(weapon, surge) > max(hitsPerEligible):
                                    if chosenWeapon:
                                        if WeaponExpectedHits(weapon, surge) > WeaponExpectedHits(chosenWeapon, surge):
                                            chosenWeapon = weapon
                                    else:
                                        chosenWeapon = weapon
                        if not chosenWeapon:
                            miniCount = miniCount + 1
                        else:
                            chosenWeapons.append(chosenWeapon)
                    else:
                        miniCount = miniCount + 1
            for upgrade in upgrades: #grenades can only be thrown once per attack
                if upgrade["cardSubtype"] == "grenades" and "weapons" in upgrade:
                    grenade = upgrade["weapons"][0]
                    if WeaponInRange(grenade, r) and WeaponExpectedHits(grenade, surge) >= max(hitsPerEligible): #not accounting for possibility of two weapons of grenades. oh well
                        chosenWeapons.append(grenade)
                        miniCount = miniCount - 1
            chosenWeapon = {}
            if len(eligibleWeapons) > 0: #the rest of the minis choose the best weapon they've got
                for i in range(len(eligibleWeapons)):
                    if WeaponExpectedHits(eligibleWeapons[i], surge) == max(hitsPerEligible):
                        chosenWeapon = eligibleWeapons[i]
                for i in range(miniCount):
                    chosenWeapons.append(chosenWeapon)

            #Count typical aims (independent = 1, tactical = 1, target no, steady = 1, charge = 1, relentless = 1) yes, these are all intended to stack
            aimCount = 0
            allKeywords = unit["keywords"]
            precise = 0
            surgeTokens = 0
            for upgrade in upgrades:
                if not "weapons" in upgrade:
                    allKeywords = allKeywords + upgrade["keywords"]
            for weapon in chosenWeapons:
                allKeywords = allKeywords + weapon["keywords"]
                if weapon["name"] == "Frag Grenade":
                    surge = True
            for k in allKeywords:
                # print(k)
                if k in ["Steady", "Charge", "Relentless", "Tactical"]: #tactical is poorly formatted in cards.json. fuck. same with precise
                    aimCount = aimCount + 1
                elif k == "Precise":
                    precise = precise + 1
                elif "name" in k:
                    if k["name"] == "Tactical": #doesnt account for 2x move steady shot with tac2+ but so far those are all one-time upgrade kinda things
                        aimCount += k["value"]
                    elif k["name"] == "Independent" and "Aim" in k["value"]: #only assumes and accounts for aim 1. I'm not parsing that shit
                        aimCount += 1
                    elif k["name"] == "Precise":
                        precise = precise + k["value"]
                    elif k["name"] == "Reliable":
                        surgeTokens = surgeTokens + k["value"]
            #special cases that i'm sick of
            for upgrade in upgrades:
                #heavy weapons that give precise
                if upgrade["cardName"] == "Crosshair":
                    precise = precise + 1
                elif upgrade["cardName"] == "Super Commando Marksman":
                    precise = precise + 1
                #problems arising when a heavy weapon also gives non-weapon keywords, or keywords that might be lsited under the weapon AND the upgrade itself. don't want to double a lethal
                elif upgrade["cardName"] == "Echo" and upgrade["title"] == "ARC Marksman":
                    surgeTokens = surgeTokens + 1
                elif upgrade["cardName"] == "Echo" and upgrade["title"] == "Clone Force 99":
                    surgeTokens = surgeTokens + 3
            #unit special cases
            if unit["cardName"] == "Yoda": #being treated as one large pool rather than 2 separate. fine for now since no aims
                tempWeapons = [w for w in chosenWeapons]
                for w in tempWeapons:
                    chosenWeapons.append(w)
                


            if len(chosenWeapons) > 0:
                expectedHits = WeaponExpectedHitsSim(chosenWeapons, aimCount, precise, surge, surgeTokens)
                print(aimCount, precise, surge, surgeTokens)
                print(expectedHits)
                hitsAtRange[r] = expectedHits

            #post-die roll unit exceptions
            if "Gunslinger" in unit["keywords"]:
                if len(chosenWeapons) > 0:
                    expectedHits = WeaponExpectedHitsSim(chosenWeapons, aimCount - 1, precise, surge, surgeTokens)
                    hitsAtRange[r] = hitsAtRange[r] + expectedHits

            for w in chosenWeapons:
                print(w)

        if unit["cardName"] == "Imperial Dark Troopers":
            hitsAtRange = [2*h for h in hitsAtRange]

        allHitsAtRange = [allHitsAtRange[i] + hitsAtRange[i] for i in range(len(hitsAtRange))]
    return allHitsAtRange

def WeaponInRange(weapon, r):
    if len(weapon["range"]) > 1:
        if weapon["range"][0] <= r and weapon["range"][1] >= r:
            return True
        else: return False
    else:
        if weapon["range"][0] == r:
            return True
        else: return False

def WeaponExpectedHits(weapon, surge):
    s = 0
    if (surge): s = 1

    print(weapon)
    for k in weapon["keywords"]:
        try:
            if k["name"] == "Critical": #kinda crude check, but should be correct
                s = 1
        except:
            pass

    hits = weapon["dice"]["r"] * (6 + s)/8 + weapon["dice"]["b"] * (4 + s)/8 + weapon["dice"]["w"] * (2 + s)/8
    return hits

def WeaponExpectedHitsSim(weapons, aims=0, precise=0, surge=False, surgeTokens=0, simCount=10000):
    #the surge-spending logic will handle spending surges on whites first, but if after re-rolling there's another white surge, it won't re-roll a black on the next in favor of spending the surge on the white 
    RED = 0
    BLACK = 0
    WHITE = 0
    AIM_VALUE = 2 + precise
    SURGE_COUNT = surgeTokens # need to also add crit x to this
    s = 0   
    if surge: s = 1
    for weapon in weapons:
        RED = RED + weapon["dice"]["r"]
        BLACK = BLACK + weapon["dice"]["b"]
        WHITE = WHITE + weapon["dice"]["w"]
    
    if aims > 0:
        hitDistribution = [0 for i in range(RED + BLACK + WHITE + 1)]
        for i in range(simCount): #all the stuff....
            #initial roll
            reds = RED
            blacks = BLACK
            whites = WHITE
            h = 0
            surgeCount = SURGE_COUNT
            
            remove = 0
            diceRoll = [random.uniform(0.0, 1.0) for x in range(reds)]
            for die in diceRoll:
                if die < (6+s)/8:
                    h = h + 1
                    remove = remove + 1
            reds = reds - remove

            remove = 0
            diceRoll = [random.uniform(0.0, 1.0) for x in range(blacks)]
            for die in diceRoll:
                if die < (4+s)/8:
                    h = h + 1
                    remove = remove + 1
            blacks = blacks - remove

            remove = 0
            diceRoll = [random.uniform(0.0, 1.0) for x in range(whites)]
            for die in diceRoll:
                if die < (2+s)/8:
                    h = h + 1
                    remove = remove + 1
            whites = whites - remove

            #spend surges
            if not surge:
                remove = 0
                diceRoll = [random.uniform(0.0, 1.0) for x in range(min(whites,surgeCount))]
                for die in diceRoll:
                    if die < 1/6:
                        h = h + 1
                        remove = remove + 1
                whites = whites - remove
                surgeCount = surgeCount - remove

                remove = 0
                diceRoll = [random.uniform(0.0, 1.0) for x in range(min(blacks,surgeCount))]
                for die in diceRoll:
                    if die < 1/4:
                        h = h + 1
                        remove = remove + 1
                blacks = blacks - remove
                surgeCount = surgeCount - remove
                
                remove = 0
                diceRoll = [random.uniform(0.0, 1.0) for x in range(min(reds,surgeCount))]
                for die in diceRoll:
                    if die < 1/2:
                        h = h + 1
                        remove = remove + 1
                reds = reds - remove
                surgeCount = surgeCount - remove

            #re-roll logic
            for j in range(aims):
                aimV = AIM_VALUE

                remove = 0
                diceRoll = [random.uniform(0.0, 1.0) for x in range(min(aimV,reds))]
                for die in diceRoll:
                    if die < (6+s)/8:
                        h = h + 1
                        remove = remove + 1
                aimV = aimV - reds
                reds = reds - remove

                if aimV > 0:
                    remove = 0
                    diceRoll = [random.uniform(0.0, 1.0) for x in range(min(aimV,blacks))]
                    for die in diceRoll:
                        if die < (4+s)/8:
                            h = h + 1
                            remove = remove + 1
                    aimV = aimV - blacks
                    blacks = blacks - remove

                if aimV > 0:
                    remove = 0
                    diceRoll = [random.uniform(0.0, 1.0) for x in range(min(aimV,whites))]
                    for die in diceRoll:
                        if die < (2+s)/8:
                            h = h + 1
                            remove = remove + 1
                    aimV = aimV - whites
                    whites = whites - remove

                #spend surges
                if not surge:
                    remove = 0
                    diceRoll = [random.uniform(0.0, 1.0) for x in range(min(whites,surgeCount))]
                    for die in diceRoll:
                        if die < 1/6:
                            h = h + 1
                            remove = remove + 1
                    whites = whites - remove
                    surgeCount = surgeCount - remove

                    remove = 0
                    diceRoll = [random.uniform(0.0, 1.0) for x in range(min(blacks,surgeCount))]
                    for die in diceRoll:
                        if die < 1/4:
                            h = h + 1
                            remove = remove + 1
                    blacks = blacks - remove
                    surgeCount = surgeCount - remove
                    
                    remove = 0
                    diceRoll = [random.uniform(0.0, 1.0) for x in range(min(reds,surgeCount))]
                    for die in diceRoll:
                        if die < 1/2:
                            h = h + 1
                            remove = remove + 1
                    reds = reds - remove
                    surgeCount = surgeCount - remove
            
            hitDistribution[h] = hitDistribution[h] + 1

        averageHits = 0
        for i in range(len(hitDistribution)):
            averageHits = hitDistribution[i]*i/simCount + averageHits
        return averageHits
    else:
        hits = RED*(6+s)/8 + BLACK*(4+s)/8 + WHITE*(2+s)/8
        hits = hits + min(SURGE_COUNT, (RED + BLACK + WHITE)/8)
        return hits 

# total health
# effective health
def Health():
    pass

#region Data Checks
def WeaponsCheck():
    for card in CARDS:
        if CARDS[card]["cardType"] == "unit":
            try:
                weapons = CARDS[card]["weapons"]
                if len(weapons) == 0:
                    print(CARDS[card]["cardName"], card)
            except KeyError:
                print(CARDS[card]["cardName"], card)

def WeaponKeywordCheck():
    pass

def KeywordCheck():
    for card in CARDS:
        if CARDS[card]["cardType"] == "upgrade":
            if CARDS[card]["cardSubtype"] in ["heavy weapon", "personnel", "weapon", "ordnance", "armament", "hardpoint"]:
                if not "weapons" in CARDS[card]:
                    print(CARDS[card]["cardName"], card)
#endregion


firePower2 = FirePower("Army Evaluator\\Data\\sample4.json")
print(firePower2)

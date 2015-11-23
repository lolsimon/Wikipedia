# -*- coding: utf-8 -*-
# Author Simon Bijl
# 2015, MIT-License
import wikipedia, userlib
import urllib, json, sys, datetime
from itertools import islice, count

def main():
    wikiString = "Onderstaande tabel geeft een indicatie van de activiteit van een moderator. De vermelde data, zijn de data dat de moderator geen moderator meer zou zijn, als hij geen bijdragen meer doet vanaf het moment dat deze pagina is geupdate. \n\n {| class=\"wikitable sortable\"\n|-\n!Gebruikersnaam || Deadline voor aantal bewerkingen\n"
    mods = getMods() #Get moderator list

    #Process for each moderator:
    for mod in mods:
        dateObj = str(deadlineOfModerator(mod))
        wikiString += "\n|-\n| [[Gebruiker:%(m)s|%(m)s]] || %(deadline)s" % { 'm':mod, 'deadline':dateObj }
    wikiString += "\n|}\n"

    wikipedia.Page(wikipedia.getSite(), "Gebruiker:Lolsimon/Activiteit_mods").put(wikiString, comment='Update') #Save page

#Returns the date a moderator would lose its moderator rights (=250 edits ago + 1 year)
def deadlineOfModerator(mod):
    modObj = userlib.User(wikipedia.getSite('nl', 'wikipedia'), mod)
    contributions = modObj.contributions(limit=251)
    edit250ago = str(nth(contributions, 250)[2])
    return datetime.datetime(int(edit250ago[0:4])+1, int(edit250ago[4:6]), int(edit250ago[6:8]), int(edit250ago[8:10]), int(edit250ago[10:12]), int(edit250ago[12:14]))

#Returns nth element of a generator
def nth(iterable, n, default=None):
    return next(islice(iterable, n, None), default)

#Returns list with all moderators active on nl.wp
def getMods():
    array = []
    response = urllib.urlopen ("https://nl.wikipedia.org/w/api.php?action=query&list=allusers&augroup=sysop&aulimit=200&format=json")
    mods = json.loads(response.read())
    for mod in mods['query']['allusers']:
        array.append(mod['name'])
    return array

if __name__ == '__main__':
    try:
        main()
    finally:
        wikipedia.stopme()


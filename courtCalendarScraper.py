import requests
import re
import datetime

initialToPage = {
    "A":"A", "B":"B", "C":"C", "D":"D", "E":"E", "F":"F", "G":"G", "H":"H", "I":"I-J", "J":"I-J", "K":"K", "L":"L", "M":"M", "N":"N", "O":"O", "P":"P", "Q":"Q-R", "R":"Q-R", "S":"S", "T":"T-V", "U":"T-V", "V":"T-V", "W":"W-Z", "X":"W-Z", "Y":"W-Z", "Z":"W-Z"
}

def datetimeparse(datestring:str):
    hour = int(datestring[14:16])
    if datestring[20:22] == 'PM':
        hour += 12
    return datetime.datetime(int(datestring[6:10]), int(datestring[0:2]), int(datestring[3:5]), hour, int(datestring[17:19]))

counties = ['Addison','Bennington','Caledonia','Chittenden','Essex','Franklin','Grand Isle','Lamoille','Orange','Orleans','Rutland','Washington','Windham','Windsor']
joinedcountyregex = '|'.join(counties)

def attnysection(attnyname:str, lastInitial:str):
    link = f"http://www.state.vt.us/courts/atty/{initialToPage[lastInitial]}_cal.htm"
    res = requests.get(link)
    res.raise_for_status()
    ctcalregex = re.compile(attnyname + '.*?HR NOSHADE',re.DOTALL)
    attnysection = ctcalregex.search(res.text).group()
    return(attnysection)

def events(section:str):
    events = []
    for x in range(len(section)):
        countymatch = re.match(joinedcountyregex, section[x:])
        timemattermatch = re.match('\d\d/\d\d/\d\d\d\d at \d\d:\d\d [AP]M +.+',section[x:])
        docketnomatch = re.match(r' \d+-\d+-\d+ .+',section[x:])
        if countymatch:
            location = countymatch.group()
        elif timemattermatch:
            time = datetimeparse(timemattermatch.group())
            matter = timemattermatch.group()[29:]
        elif docketnomatch:
            docketno = docketnomatch.group()
            event = {'location':location, 'time':time, 'docketno':docketno,'matter':matter}
            events += [event]
    return events

def attnyevents(attnyname:str, lastInitial:str):
    section = attnysection(attnyname, lastInitial)
    return events(section)
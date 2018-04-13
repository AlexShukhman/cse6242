'''

LinkedIn Scraping Algorithm for CSE6242 - Spr 2018
(Group 31: Evzonas and Shukhman)

-> External Downloaded Libraries Used:
    python3-linkedin
    
-> To Run:
    $ pip install python3-linkedin
    [or pip3 install python3-linkedin]
    $ python scrape.py
    [or python3 scrape.py]

-> Inputted values:
    none

-> Returned Values:
    runtime: debugging statements to stdout
    end: approx run time (seconds) in type float to stdout

-> Files Created:
    graph.csv

-> Other notes:
    This requires a file called token.txt which is not included in the final
    submission.

'''



# ***** Imports/Env *****

# Env Variables -- lowers safety of oauth locally, no harm will come of it
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

# Non-External Libraries
import re, csv, json, time, requests, socket
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

# External Libraries
import linkedin


# ***** Globals *****

# Read In Token
def readtoken(): # file is 3 lines: Client ID, Client Secret, Authorization Code
    with open('token.txt', 'r') as f:
        token = f.readlines() 
    return token

# O-Auth Access Token
global access_token
access_token = readtoken()

# List of Companies
global companies
companies = ['ionic-security', 'immunet', 'flashpoint-intel', 'phantom-cyber',
             'brightpoint-security-formerly-vorstack', 'endgame']



# ***** Helper Functions *****

# Writer
def writer(datalist):
    with open ('graph.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'target', 'qualifier'])
        for line in datalist:
            writer.writerow(line);
    return

# Scrape User
def scrapeUsers(uids):
    ids = 'List((id:{'+uids[0]+'})'
    uids.pop(0)
    for uid in uids:
        ids += 'id:{'+uid+'})'

# Get Links of a single user
def getLinksU(app, u):
    res = app
    return

# Get Links of a company
def getLinksC(app, c):
    res = app.get('http://api.linkedin.com/v1/people-search?company-name='+
                  c +'&current-company=true')
    return

# Get Links main
def getLinks(app, c):
    links = []
    cLinks = getLinksC(app, c)
    links += cLinks
    for link in cLinks:
        uLinks1 = getLinksU(app, link[1])
        links += uLinks1
        for link1 in uLinks1:
            uLinks2 = getLinksU(app, link1[1])
            links += uLinks2
            for link2 in uLinks2:
                links += getLinksU(app, link2[1])
    return links

# Compile Link List into CSV
def comp(l):
    links = []
    for i in l:
        links += i
    writer(links)
    print('Wrote ' + str(len(links)) + ' lines')
    return
        

# Create Session
def createApp():
    client_id    = access_token[0].strip()
    client_secret = access_token[1].strip()
    authorization_base_url = 'https://www.linkedin.com/uas/oauth2/authorization'
    token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    RETURN_URL = "https://smop.io"

    linkedin = OAuth2Session(client_id, redirect_uri='http://127.0.0.1')
    linkedin = linkedin_compliance_fix(linkedin)

    authorization_url, state = linkedin.authorization_url(
        authorization_base_url)
    print ('Please go here and authorize,', authorization_url)

    redirect_response = input('Paste the full redirect URL here:')

    linkedin.fetch_token(token_url, client_secret=client_secret,
                         authorization_response=redirect_response)
    return linkedin
    


# ***** Main Function and Runner *****

# Main
def main():
    app = createApp()
    res = []
    n = 0
    t = 0
    day = time.ctime().split(' ')[0]
    for i in companies:
        r, t0 = getLinks(app, i, T)
        res += r
        t += t0
        while True:
            if (t/500000-n) < 1:
                print("done with "+i+", boutta start another")
                break
            elif time.ctime().split(' ')[0] != day:
                day = time.ctime().split(' ')[0]
                print("done with "+i+", boutta start another")
                break
    print("all done, compiling into csv")
    comp(res)
    return

# Runner
if __name__ == "__main__":
    #main()
    print()

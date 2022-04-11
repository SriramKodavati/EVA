import Responce
import requests
#import speech
import display


from bs4 import BeautifulSoup

whatis = "What is"
warningString = "Warning"
seString = 'side effects'
iTakeString = 'take'

def userSelection(filterString, url):
    resp = requests.get(url)
    infoCount = 0
    print('made it')

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text, 'lxml')

        for data in soup.find_all('h2'):
            if whatis in data.text:
                for dat in data.find_all_next(['p', 'h2']):
                    if infoCount > 0:
                        break
                    if dat.name == 'h2':
                        break
                    infoCount = infoCount + 1

    else:
        print('couldnt open')

    if 'i take' in filterString or 'warnings' in filterString or 'side effects' in filterString or 'warning' in filterString:
        for data in soup.find_all('h2'):
            if filterString in data.text:
                for dat in data.find_all_next(['p', 'h2']):
                    if dat.name == 'h2':
                        break
                    print(dat.text)
                    Responce.justsay(dat.text)
                    return
    elif 'none' in filterString:
        print(filterString)
        speech.speak('alright, let me know if you need anything else')
        return
    else:
        Responce.justsay("error, try again")




def readSite(url, drugname):
    resp = requests.get(url)
    infoCount = 0

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text, 'lxml')

        for data in soup.find_all('h2'):
            if whatis in data.text:
                for dat in data.find_all_next(['p', 'h2']):
                    if infoCount > 0:
                        break
                    if dat.name == 'h2':
                        break
                    print(dat.text)
                    Responce.speechandsayDrugs(dat.text)
                    infoCount = infoCount + 1
        return soup
    else:
        print('couldnt open')



def metformin():
    url = 'https://www.drugs.com/metformin.html'
    selection = readSite(url, 'Metformin')
    return selection

def lisinopril():
    url = 'https://www.drugs.com/lisinopril.html'
    selection = readSite(url, 'Lisinopril')

def amlodipine():
    url = 'https://www.drugs.com/amlodipine.html'
    selection = readSite(url, 'Amlodipine')

def albuterol():
    url = 'https://www.drugs.com/albuterol.html'
    selection = readSite(url, 'Albuterol')

def atorvastatin():
    url = 'https://www.drugs.com/atorvastatin.html'
    selection = readSite(url, 'atorvastatin')

def levothyroxine():
    url = 'https://www.drugs.com/levothyroxine.html'
    selection = readSite(url, 'levothyroxine')

def metoprolol():
    url = 'https://www.drugs.com/metoprolol.html'
    selection = readSite(url, 'metoprolol')

def omeprazole():
    url = 'https://www.drugs.com/omeprazole.html'
    selection = readSite(url, 'omeprazole')

def losartan():
    url = 'https://www.drugs.com/losartan.html'
    selection = readSite(url, 'losartan')

def simvastatin():
    url = 'https://www.drugs.com/simvastatin.html'
    selection = readSite(url, 'simvastatin')

def rosuvastatin():
    url = 'https://www.drugs.com/rosuvastatin.html'
    selection = readSite(url, 'rosuvastatin')

def tamsulosin():
    url = 'https://www.drugs.com/tamsulosin.html'
    selection = readSite(url, 'tamsulosin')

def specificDruginfo(specificName):

    specificMedicine = specificName

    print(specificName)

    if specificMedicine == "Metformin" or specificMedicine == "metformin":
        retResult = metformin()
        return retResult
    elif specificMedicine == "Lisinopril" or specificMedicine == "lisinopril":
        lisinopril()
    elif specificMedicine == "Amlodipine" or specificMedicine == "amlodipine":
        amlodipine()
    elif specificMedicine == "Albuterol" or specificMedicine == "albuterol":
        albuterol()
    elif specificMedicine == "Atorvastatin" or specificMedicine == "atorvastatin":
        atorvastatin()
    elif specificMedicine == "Levothyroxine" or specificMedicine == "levothyroxine":
        levothyroxine()
    elif specificMedicine == "Metoprolol" or specificMedicine == "metoprolol":
        metoprolol()
    elif specificMedicine == "Omeprazole" or specificMedicine == "omeprazole":
        omeprazole()
    elif specificMedicine == "Losartan" or specificMedicine == "losartan":
        losartan()
    elif specificMedicine == "Simvastatin" or specificMedicine == "simvastatin":
        simvastatin()
    else:
        speech.speak("Medicine not in system.")
        return "none"


def getMedName():
    speech.speak("Sure. Can you say the name of the medicine you want information on?")
    display.putText("Sure. Can you say the name of the medicine you want information on?")
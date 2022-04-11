#import speech
import display

def justDisplay(str):
    display.putText(str)


def justsay(str):
    speech.speak(str)

def speechandsay(str):
    display.putText(str)
    #speech.speak(str)

def speechandsayDrugs(str):
    display.putText2(str)
    #speech.speak(str)
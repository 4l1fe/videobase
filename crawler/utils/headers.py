from crawler.constants import browser_strings, browser_freq
import random

def get_random_weighted_browser_string():

    num = random.randint(1,100)
    summarum = 0
    
    for key,val in browser_freq.items():
        summarum += val
        if num < summarum :
            break

    brfiltered = [ brs for brs in browser_strings if key in brs]
    if brfiltered:
        return random.choice(brfiltered)
    else:
        return random.choice(browser_strings)


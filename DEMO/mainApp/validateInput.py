import re


def isValidTwitterHandle(text):
    if(len(text) > 15 or len(text) == 0):
        return False
    regex = re.compile('[\s@!#$%^&*()<>?/\|}{~:]')
    if(regex.search(text) != None):
        return False
    return True

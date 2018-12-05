import re


def isValidTwitterHandle(text):
    if(len(text) > 15):
        return False
    regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
    if(regex.search(text) != None):
        return False
    return True

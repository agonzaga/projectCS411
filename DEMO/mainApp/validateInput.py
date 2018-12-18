import re


def isValidTwitterHandle(text):
    if(len(text) > 15 or len(text) == 0):
        return False
    regex = re.compile('[\s@!#$%^&*()<>?/\|}{~:]')
    if(regex.search(text) != None):
        return False
    return True


# Remove URL text from tweets
def prettyTweets(tweets):
    d = {"contentItems": []}
    tweetsAsString = ""
    for item in tweets:
        if ("https://" in item or "http://" in item):
            item = item[:item.find("http")]
        d["contentItems"].append({"content": item})
        tweetsAsString += item + " "
    return (d, tweetsAsString)

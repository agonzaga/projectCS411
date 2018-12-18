from watson_developer_cloud import PersonalityInsightsV3
from os.path import join, dirname
import json


# Connects to Watson
def watson(file):
    personality_insights = PersonalityInsightsV3(
        version='2018-08-01',
        iam_apikey='-nE47TPbkO4Y90I15b7-wFcodJzt7O6pITqJGeOgnE3N',
        url='https://gateway-wdc.watsonplatform.net/personality-insights/api'
    )

    with open(join(dirname(__file__), file)) as profile_json:
        profile = personality_insights.profile(
            profile_json.read(),
            content_type='application/json',
            consumption_preferences=True,
            raw_scores=True
        ).get_result()

    return(json.dumps(profile, indent=2))


# Calls Watson and returns the analysis
def getWatsonAnalysis():
    traits = []
    watson_text = watson("../profile.json")
    watson_text2 = json.loads(watson_text)
    for i in watson_text2.get("personality"):
        score = (i.get("name"), i.get("raw_score"))
        traits.append(score)
    return traits


def formatAnalysis(traits):
    traitPercentile = []

    # Converts personailty score to 100 percentile
    for trait in traits:
        traitPercentile.append((trait[0], "%.2f" % (trait[1]*100)))

    return traitPercentile

from watson_developer_cloud import PersonalityInsightsV3
from os.path import join, dirname
import json


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

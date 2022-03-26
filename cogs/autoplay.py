from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class AutoPlay(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    async def get_answer(self, question):
        check_question = db.questions_base.find_one({"question": question})
        if not check_question: return None
        answer = db.questions_base.find_one({"question": question}).get("answer")
        return answer

    async def add_question(self, question, answer):
        check_question = db.questions_base.find_one({"question": question})
        if not check_question:
            db.questions_base.insert_one({"question": question, "answer": answer})

    async def auto_play(self):
        try:
            offair_id = api.start_offair()['gameUuid']
        except ApiResponseError:
            offair_id = api.get_schedule()['offairTrivia']['games'][0]['gameUuid']
        while True:
            offair = api.offair_trivia(offair_id)
            print("Question {0}/{1}".format(offair['question']['questionNumber'], offair['questionCount']))
            print(offair['question']['question'])
            for answer in offair['question']['answers']:
                print('{0}. {1}'.format(answer['offairAnswerId'], answer['text']))
            select = int(input('Select answer [1-3] > '))
            answer = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            print('You got it right: ' + str(answer['youGotItRight']))
            if answer['gameSummary']:
                print('Game ended')
                print('Earned:')
                print('Coins: ' + str(answer['gameSummary']['coinsEarned']))
                print('Points: ' + str(answer['gameSummary']['pointsEarned']))
                break

def setup(client):
    client.add_cog(AutoPlay(client))
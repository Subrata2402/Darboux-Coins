from pymongo import MongoClient


data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/Darboux?retryWrites=true&w=majority')
db = data.get_database("Darboux")
token_base = db.token
login_token_base = db.login_token
q_base = db.questions
auto_base = db.auto_play

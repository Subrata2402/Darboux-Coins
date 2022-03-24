from pymongo import MongoClient

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/Darboux?retryWrites=true&w=majority')
db = data.get_database("Darboux")
profile_base = db.profile
questions_base = db.questions

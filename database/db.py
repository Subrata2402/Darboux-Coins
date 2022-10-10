import motor.motor_asyncio


url = "mongodb://Subrata2001:Subrata2001@cluster0-shard-00-00.ywnwn.mongodb.net:27017,cluster0-shard-00-01.ywnwn.mongodb.net:27017,cluster0-shard-00-02.ywnwn.mongodb.net:27017/?ssl=true&replicaSet=atlas-ibirzx-shard-0&authSource=admin&retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = client.Darboux
profile_base = db.profile
questions_base = db.hq_questions
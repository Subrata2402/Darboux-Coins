import motor.motor_asyncio
url = "mongodb://chingari:tweet99@ac-ckzkoia-shard-00-00.p3hxmwx.mongodb.net:27017,ac-ckzkoia-shard-00-01.p3hxmwx.mongodb.net:27017,ac-ckzkoia-shard-00-02.p3hxmwx.mongodb.net:27017/?ssl=true&replicaSet=atlas-gjiwte-shard-0&authSource=admin&retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = client.Darboux
profile_base = db.profile
questions_base = db.hq_questions
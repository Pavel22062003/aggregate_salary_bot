import motor.motor_asyncio
from environs import Env

env = Env()
env.read_env()

client = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)
db = client['sampleDB']

BOT_TOKEN = env.str('BOT_TOKEN')

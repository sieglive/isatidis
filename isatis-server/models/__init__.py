from pymongo import MongoClient
from config import CFG as config

M_CLIENT = MongoClient(config.mongodb).isatis

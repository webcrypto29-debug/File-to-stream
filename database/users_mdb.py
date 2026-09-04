import motor.motor_asyncio
import re
from config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["AutoFilterBot"]
files_col = db["files"]

# फ़ाइल डेटाबेस में सेव करना
async def save_file(file_id, file_name, file_size):
    # नाम से विशेष कैरेक्टर हटाना ताकि सर्च आसान हो
    clean_name = re.sub(r'[_.-]', ' ', file_name)
    
    file_doc = {
        "file_id": file_id,
        "file_name": file_name,
        "clean_name": clean_name,
        "file_size": file_size
    }
    
    # अगर फ़ाइल पहले से है तो अपडेट करें, नहीं तो नई जोड़ें
    await files_col.update_one(
        {"file_id": file_id},
        {"$set": file_doc},
        upsert=True
    )

# फ़ाइल खोजना (Case-insensitive Regex Search)
async def get_search_results(query):
    clean_query = re.sub(r'[_.-]', ' ', query)
    regex = re.compile(clean_query, re.IGNORECASE)
    
    cursor = files_col.find({
        "$or": [
            {"file_name": {"$regex": regex}},
            {"clean_name": {"$regex": regex}}
        ]
    })
    
    results = await cursor.to_list(length=20)
    return results

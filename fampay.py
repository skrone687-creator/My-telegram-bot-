import aiohttp
import json

async def make_request(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}) as response:
            return await response.json()
 async def prepare_payment(chosen_amount):
    payload = {
        "amount": chosen_amount,
        "txn_id": "TXN123456789",
        "description": "Payment for bot services",
    }
    return payload
         

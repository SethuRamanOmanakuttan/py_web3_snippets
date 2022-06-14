import asyncio #for async code
import websockets
import json

#setting the wsss endpoint
CHAINSTACK_WSS_ENDPOINT = "<wss://chainstack-node-endpoint>"

#function to 
# -> establish connection
# -> send the required rpc object
# -> receive and process the corresponding the response
# returns result
async def send_receive_data(request_data):
    async with websockets.connect(CHAINSTACK_WSS_ENDPOINT) as websocket:
        await websocket.send(json.dumps(request_data))
        resp = await websocket.recv()    
        return json.loads(resp)["result"]

#function to fetch the filter id
async def get_filter_id():
    request_data = {
        "jsonrpc": "2.0",
        "method": "eth_newPendingTransactionFilter",
        "params": [],
        "id": 1
    }
    filter_id = await send_receive_data(request_data)
    return filter_id

#function to display transaction details
async def get_transaction_detail(hash_list):
    #check if list is empty
    if(len(hash_list) == 0):
        print("")
    else:
        #for each hash value in the list
        for hash in hash_list:
            #prepare a eth_getTransactionByHash request using the hash value
            request_data = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": [hash],
                "id": 1
            }
            #get the transaction details
            transaction_detail = await send_receive_data(request_data)
            print(transaction_detail)
            print("="*80)
    



async def get_pending_transaction():
    #get the filter id
    filter_id = await get_filter_id()
    #prepare request using filter id
    request_data = {
    "jsonrpc": "2.0",
    "method": "eth_getFilterChanges",
    "params": [filter_id],
    "id": 0
    }
    while True:
        pending_hash_list = await send_receive_data(request_data)
        #pass the hash value list to get_transaction_detail
        await get_transaction_detail(pending_hash_list)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_pending_transaction())
    loop.close()



# use ctrl + z to break the loop

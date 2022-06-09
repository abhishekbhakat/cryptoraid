import json
# 3paddle strategy
class Wallet():

    def __init__(self):
        self.target_balance = {}
        self.source_balance = {}
        
        self.paddle_1 = {}
        self.paddle_2 = {}
        self.paddle_3 = {}
    
    def __str__(self) -> str:
        status = {}
        status['Target_balance'] = self.target_balance
        status['Source_balance'] = self.source_balance
        status['Paddle-1'] = self.paddle_1
        status['Paddle-2'] = self.paddle_2
        status['Paddle-3'] = self.paddle_3
        return json.dumps(status)
    
    def get(self) -> str:
        status = {}
        status['Target_balance'] = self.target_balance
        status['Source_balance'] = self.source_balance
        status['Paddle-1'] = self.paddle_1
        status['Paddle-2'] = self.paddle_2
        status['Paddle-3'] = self.paddle_3
        return status
    
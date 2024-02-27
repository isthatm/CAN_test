import cantools
from typing import List


class CAN_database:
    def __init__(self, db_path) -> None:
            self.db = cantools.db.load_file(filename=db_path, database_format='dbc')
    
    def list_nodes(self):
        return self.db.nodes
    
    def list_messages(self):
        return self.db.messages   

    def list_sending_msg(self, node_name: str): 
        sending_msg = []
        for msg in self.list_messages():
            if msg.senders[0] == node_name:
                sending_msg.append(msg)
        return sending_msg    
    
    def list_receiving_msg(self, node_name: str) -> List[cantools.db.Message]:
        receiving_msg = [msg for msg in self.list_messages() 
                            if node_name in msg.receivers]
        return receiving_msg

                
if __name__ == '__main__':
    db = CAN_database("./Example.dbc")
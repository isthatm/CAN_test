import cantools

class CAN_database:
    def __init__(self, db_path) -> None:
            self.db = cantools.db.load_file(filename=db_path, database_format='dbc')
    
    def list_nodes(self):
        return self.db.nodes
    
    def list_messages(self):
        return self.db.messages   

    def list_node_msg(self, node_name: str): 
        node_msg = []
        for msg in self.list_messages():
            if msg.senders[0] == node_name:
                node_msg.append(msg)
                
        return node_msg     
                 
if __name__ == '__main__':
    DB = CAN_database("./Example.dbc")
    DB.list_node_msg()
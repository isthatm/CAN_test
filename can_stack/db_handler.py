import cantools

class CAN_database:
    def __init__(self, db_path) -> None:
            self.db = cantools.db.load_file(filename=db_path, database_format='dbc')
    
    def list_nodes(self):
        return self.db.nodes
    
    def list_messages(self):
        return self.db.messages    
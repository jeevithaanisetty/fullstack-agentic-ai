
# employee-project entity
class Project:
    def __init__(self, project_id, name,status):
        self.project_id = project_id 
        self.name = name
        self.status = status
        
    # converting json data to dictionary
    def to_dict(self):
        return {
            "project_id":self.project_id, 
            "name":self.name,
            "status":self.status
        }
    
    # converting dictionary to data object
    def from_dict(data):
        return[
            data["project_id"],
            data["name"],
            data["status"]
        ]

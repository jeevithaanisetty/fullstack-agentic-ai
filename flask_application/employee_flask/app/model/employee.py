from app.model.project import Project
from datetime import datetime

# employee entity
class Employee:
    def __init__(self, emp_id, name, department,salary,designation, location,dob, projects):
        self.emp_id =  emp_id
        self.name = name 
        self.department = department
        self.salary = salary
        self.designation =  designation
        self.location = location
        self.dob = dob
        self.projects = [ Project(**p) for p in projects]
    
    #converting json data to dictionary
    def to_dict(self):
       return {
           "emp_id":self.emp_id, 
            "name":self.name, 
            "department":self.department,
            "salary":self.salary,
            "designation":self.designation, 
            "location":self.location,
            "dob":self.dob, 
            "projects":[p.to_dict() for p in self.projects]         # converting each project object to a dictionary
        }
    
    # converting dict to data object
    def from_dict(data):
        return [
                data["emp_id"],
                data["name"],
                data["department"],
                data["salary"],
                data["designation"],
                data["location"],
                data["dob"],
                data["projects"]
        ]
    
    # finding count of projects 
    def is_on_bench(self):
        return len(self.projects) == 0 
    
    # finding employee based on project status
    def has_project_with_status(self, status):
            return any (p.status == status for p in self.projects)
    
    # calculating age based on dob
    def get_age (self):
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (datetime.now() - birth_date).days // 365

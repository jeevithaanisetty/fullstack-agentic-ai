from utils.helper_methods import save_to_json,load_from_json
import os

#ROLES_JSON="roles.json"
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
ROLES_JSON=os.path.join(BASE_DIR,"roles.json")
    
class Role:         
    def __init__(self, role_id,role_name):
        self.role_id=role_id
        self.role_name=role_name
    def to_dict(self):
        return vars(self) 
    def __str__(self):
        return f"Department {self.role_id} - {self.role_name}"
    
    @classmethod
    def add_role(cls):
        role_id=input("enter role_id:")
        role_name=input("enter role_name:")
        
        roles=load_from_json(ROLES_JSON)
        role=Role(role_id,role_name).to_dict()
        roles.append(role)
        save_to_json(roles,ROLES_JSON)
    
    def list_roles():          
        roles=load_from_json(ROLES_JSON)
        print("\033[92m\nAvailable roles")
        for r in roles:
            print(f"{r['role_id']} : {r['role_name']}")
        print("\033[0m")
    
    def delete_role():
        role_id=input("enter role_id:")
        roles=load_from_json(ROLES_JSON)
        new_list=list(filter(lambda r:r['role_id']!=role_id, roles))
        save_to_json(new_list,ROLES_JSON)
        print(f"employee with {role_id} as role_id is deleted")


    
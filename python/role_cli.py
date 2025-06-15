import json
import os

ROLES_JSON="roles.json"

def save_to_json(data,file):
    with open(file,"w") as f:
        json.dump(data,f,indent=4)
def load_from_json(file):
    if not os.path.exists(file):
        return []
    with open(file,"r") as f:
       return json.load(f)


class Role:
    def __init__(self,role_id,role_name):
        self.role_id=role_id
        self.role_name=role_name
    def to_dict(self):
        return vars(self)          
    def __str__(self):
        return f"roles {self.role_id} -{self.role_name}"
    @staticmethod
    def list_roles():        
        roles=load_from_json(ROLES_JSON)
        print("\033[92m\nAvailable roles")
        for r in roles:
            print(f"{r['role_id']} : {r['role_name']}")
        print("\033[0m")

    @classmethod
    def add_roles(cls):
        role_id=input("enter role_id:")
        role_name=input("enter role_name:")
        
        roles=load_from_json(ROLES_JSON)
        role=cls(role_id,role_name).to_dict()
        roles.append(role)
        save_to_json(roles,ROLES_JSON)

def menu():
    while True:
        print("\n===========EMPLOYEE SYSTEM========")
        print("1.add_roles")
        print("2.list_roles")
        print("0.Exit")
        choice=input("choose an option:")
        if choice=="1": Role.add_roles()
        elif choice=="2": Role.list_roles()
        elif choice=="0": print("\033[92m\nexiting........\033[0m") ;break  
        else: print("\033[91minvalid choice\033[0m")

if __name__=='__main__':
    menu()

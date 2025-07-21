import logging
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory employee storage
employees = []
id_counter = 1

logging.basicConfig (
    filename = 'employee.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logging = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

# CREATE employee
@app.route('/employees', methods=['POST'])
def create_employee():
    global id_counter
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')

    if not name or not position:
        return jsonify({'error': 'Name and position are required'}), 400

    employee = {'id': id_counter, 'name': name, 'position': position}
    employees.append(employee)
    id_counter += 1

    return jsonify(employee), 201

# READ all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# READ single employee
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify(employee)

# UPDATE employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    employee['name'] = data.get('name', employee['name'])
    employee['position'] = data.get('position', employee['position'])

    return jsonify(employee)

# DELETE employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    global employees
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    employees = [emp for emp in employees if emp['id'] != employee_id]
    return jsonify({'message': 'Employee deleted', 'employee': employee})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
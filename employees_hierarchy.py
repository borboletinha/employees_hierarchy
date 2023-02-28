import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

# Get environmental variables
load_dotenv()


def print_hierarchy(employee, indentation=0):
    """Recursively prints a full employees hierarchy with indentation"""
    print(f'{" " * indentation}{employee["name"]}, {employee["position"]}')
    for subordinate in employee['subordinates']:
        print_hierarchy(subordinate, indentation=indentation + 4)


def build_hierarchy(employees):
    """Constructs a full employees hierarchy with every employee as an independent row"""
    employees_dict = {}
    for employee in employees:
        employee_id = employee[1]
        if employee_id not in employees_dict:
            employees_dict[employee_id] = {'name': employee[2], 'position': employee[3],
                                           'level': employee[-1], 'subordinates': []}
        else:
            employees_dict[employee_id]['name'] = employee[2]
            employees_dict[employee_id]['position'] = employee[3]
            employees_dict[employee_id]['level'] = employee[-1]
        boss_id = employee[0]
        if boss_id != 0:
            if boss_id not in employees_dict:
                employees_dict[boss_id] = {'name': None, 'position': None, 'level': None, 'subordinates': []}
            employees_dict[boss_id]['subordinates'].append(employees_dict[employee_id])
    return [employee for employee in employees_dict.values()]


# Connect to the database
connection = mysql.connector.connect(host='localhost',
                                     user=os.getenv('DB_USER'),
                                     passwd=os.environ.get('DB_PASSWORD'),
                                     database='EmployeeStructure')
cursor = connection.cursor()

try:
    # Make a MySQL queryset
    cursor.execute('WITH RECURSIVE CTE(BossId, Id, Name, Position, subordination_level) AS ('
                   'SELECT parent.BossId, parent.Id, parent.Name, parent.Position, 0 AS subordination_level '
                   'FROM Employees parent '
                   'WHERE parent.BossId = 0 '
                   'UNION ALL '
                   'SELECT child.BossId, child.Id, child.Name, child.Position, subordination_level + 1 '
                   'FROM Employees child '
                   'INNER JOIN CTE AS cte ON child.BossId = cte.Id) '
                   'SELECT BossId, CTE.Id, Name, Positions.Position, subordination_level '
                   'FROM CTE '
                   'JOIN Positions ON CTE.Position = Positions.Id '
                   'ORDER BY subordination_level;')
    result = cursor.fetchall()

    # Make a nested dict
    employees_hierarchy = build_hierarchy(result)

    for employee in employees_hierarchy:
        if employee['level'] == 0:  # print only the top tier of hierarchy with all subordinates
            print_hierarchy(employee)

except Error as e:
    print(f'The following error has occurred: "{e}"')
    connection.rollback()
connection.close()

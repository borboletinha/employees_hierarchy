# Employees Hierarchy Script

## TOC
1. [Description](#description)
   - [Principle of operation](#principle-of-operation)
   - [Project structure](#project-structure)
   - [Tests absence](#tests-absence)
2.  [Running](#running)

## Description

A small script that prints the hierarchy of employees in a tree form in the console.

### Principle of operation

1. The data on the subordination of employees to each other and their positions is taken by means of an SQL query to the ```Employees``` and ```Positions``` tables in the ```EmployeeStructure``` MySQL database.

   The tables have the following organization:

**EMPLOYEES**

| Id  |   Name   | Position | BossId |
|-----|:--------:|---------:|-------:|
| 1   | Jane Doe |        1 |      0 |
| 2   | John Doe |        2 |      1 |
| 3   | Kate Doe |        3 |      2 |


**POSITIONS**

| Id  | Position  |
|-----|:---------:|
| 1   |    CEO    |
| 2   |    CTO    |
| 3   | Developer |


2.  Using the ```build_hierarchy``` function, from the list of tuples returned by the database query, a nested dictionary is created indicating the subordinate employees for each employee;


3. Using the ```print_hierarchy``` function, a tree-like hierarchy of employees is displayed in the console. To avoid duplication of employees, subordinates are displayed only for the highest level of management. Tree view is created using indentation.

* The example output:
```
Jane Doe, CEO
    John Doe, CTO
        Kate Doe, Developer
```

### Project structure
```
├── employees_hierarchy
│ ├── EmployeeStructure            # prepopulated database
│ │ ├── Employees.ibd
│ │ └── Positions.ibd
├── .env 
├── .gitignore 
├── employees_hierarchy.py         # the main script file  
├── README.md  
└── requirements.txt
```

### Tests absence

Please note that there are no tests in this project, since their writing was not included in the Scope of Work.

## Running

1. From the directory where the ```employees_hierarchy.py``` file is located, run the following command in a terminal:
```bash
python employees_hierarchy.py
```

**N.B.** Please note that this section does not describe the process of creating a virtual environment and installing dependencies.
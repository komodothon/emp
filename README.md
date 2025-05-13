# Employee Management System (ERP)

## Overview
The **Employee Management System** is a comprehensive web application designed to manage employee-related information within an organization. This system is part of a larger ERP (Enterprise Resource Planning) framework, providing features such as managing employees, departments, roles, and more.

## Features

### 1. **Employee Management**
   - Add, view, update, and delete employee records.
   - Track essential employee details like name, contact information, department, and role.
   - Assign employees to specific departments and roles within the organization.

### 2. **Department Management**
   - Create, update, and delete departments.
   - Manage hierarchical relationships between departments (e.g., sub-departments and parent departments).
   - View departments along with their employees.

### 3. **Role Management**
   - Create, update, and delete roles.
   - Assign roles to employees for structured organizational management.
   - RBAC (Role Based Access Control) control access based on user roles.


### 4. **Department Hierarchy**
   - Implement department structure with parent-child relationships.
   - Manage multiple levels of department hierarchy to represent organizational divisions.

### 5. **Data Integrity and Validation**
   - Ensure employee records and department data are consistently validated.
   - Include form validation to ensure that all data entered is accurate and follows business rules.

### 6. **Database Migrations**
   - Utilize Flask-Migrate to handle database schema

### 7. Payroll Module
   - Manage employee payroll records, including salaries, bonuses, deductions, and tax information.
   - Generate payslips based on the employee’s salary structure, contract type, and any other applicable deductions.
   - Calculate and update employee compensation automatically according to their position and contractual details.
   - Integrates the payroll records with the employee management system to ensure smooth payroll processing for each employee.

### 8. Responsive Design
   - The app is built with Bootstrap to ensure it is fully responsive and works well across desktops, tablets, and mobile devices.
   - Integrates JavaScript with AJAX to dynamically update UI based on real-time backend responses without full page reloads.


## Technologies Used
### 1. Flask: 
   - Web framework for Python.

### 2. SQLAlchemy: 
   - ORM (Object-Relational Mapper) for database operations + sqlite databse.

### 3. Bootstrap, HTML, CSS: 
   - Front-end framework for responsive design.

### 4. Flask-WTF: 
   - For handling forms and validation.

### 5. Flask-Migrate: 
   - Database migration support.
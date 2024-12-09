# Warehouse Management System

This is a simple warehouse management system built using **Flask**, **SQLAlchemy**, and **HTML/CSS/JavaScript**. It allows users to manage an inventory of products, track inbound and outbound products, and manage users with different roles.

## Features

- **Inventory Management**: Add, view, update, and delete products in the inventory.
- **Inbound Management**: Track incoming products, supplier information, and update the inventory.
- **Outbound Management**: Track outgoing products, customer information, and update the inventory.
- **User Management**: Assign roles (Admin, Operator) for different levels of access.
- **Responsive UI**: The app is mobile-friendly and responsive on all screen sizes.

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/warehouse-management.git
   cd warehouse-management

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
5. Run the application:
   ```bash
   flask run
6. Open the app in your browser at http://127.0.0.1:5000
   

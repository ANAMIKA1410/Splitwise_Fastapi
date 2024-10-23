# Expense Sharing App

### Overview
An application to manage shared expenses, allowing users to split costs equally, by exact amounts, or by percentage. Built with FastAPI and MySQL.

### Features

#### User Management: Add and manage users.
#### Expense Tracking: Record and track expenses.
#### Balance Calculation: Calculate user balances.
#### Flexible Splitting: Split expenses by equal, exact amounts, or percentages.

### Setup
#### Clone the repository:
git clone [https://github.com/ANAMIKA1410/Splitwise_Fastapi] <br>
cd /Splitwise_Fastapi
<br>Install dependencies:
pip install -r requirements.txt

#### Set up environment variables:
DATABASE_USER=<> <br>
DATABASE_PASSWORD=<> <br>
DATABASE_HOST=<> <br>
DATABASE_NAME=expense_sharing_app


#### Run the application: <br>
uvicorn main:app --reload <br>
Access the API docs at http://127.0.0.1:8000/docs for detailed API information.


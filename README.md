# 🏦 Maybank Credit Card Statement Generator (Backend)

This is a backend Python application that automatically generates PDF statements for Maybank credit card customers. It uses SQLite for storing user and transaction data and outputs professional-looking PDF statements.

---

## 📂 Project Structure

backend_maybank-main/ ├── main.py # Main script to run the statement generator ├── statement_generator.py # PDF generation logic ├── init_db.py # Initializes sample database records ├── database/ │ ├── credit_card.db # SQLite database file │ └── schema.sql # SQL schema (optional) ├── statements/ │ └── statement.pdf # Output PDF file └── README.md # You're reading it!
---

## ⚙️ Setup & Usage

1. 🔧 Install Python 3.10 or later

2. 💻 Clone this repository:
```bash
git clone https://github.com/your-username/backend_maybank-main.git
cd backend_maybank-main

Install required packages (if any):
pip install -r requirements.txt

Initialize the database:
python init_db.py

Generate a sample statement:
python main.py

Output Example
The generated PDF includes:
Cardholder information
Credit card number (partially masked)
Recent transactions
Total amount due


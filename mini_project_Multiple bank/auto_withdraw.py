import csv
import time
from datetime import datetime

CSV_FILE = "scheduled_transactions.csv"

# Function to add a scheduled payment
def schedule_payment(account_id, amount, due_date, description):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_id, amount, due_date, description, "pending"])
    print("✅ Payment Scheduled Successfully!")

# Function to process payments automatically
def process_payments():
    updated_transactions = []
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[2] == today and row[4] == "pending":
                    print(f"💰 ₹{row[1]} withdrawn for {row[3]}")
                    row[4] = "completed"
                updated_transactions.append(row)
    except FileNotFoundError:
        print("No scheduled transactions found.")

    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_transactions)

# Simple CLI Menu
def main():
    while True:
        print("\n1. Schedule Payment\n2. Process Payments\n3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            acc_id = input("Enter Account ID: ")
            amt = input("Enter Amount: ")
            date = input("Enter Due Date (YYYY-MM-DD): ")
            desc = input("Enter Description: ")
            schedule_payment(acc_id, amt, date, desc)

        elif choice == "2":
            process_payments()
            print("✅ Payment Processing Completed!")

        elif choice == "3":
            break

        else:
            print("❌ Invalid Choice!")

if __name__ == "__main__":
    main()

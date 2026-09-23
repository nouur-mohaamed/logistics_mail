import gspread 
import smtplib
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date , timedelta
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file
#------------------ prepare the connection to google sheet -----------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials=ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("log").sheet1
#-------------------------------------------------------
#------------------ check the date and send email -----------------------
stored_dates = sheet.col_values(18)

for idx, date_str in enumerate(stored_dates):
    # Skip empty cells and header row
    if idx<=5: continue
    if not date_str or date_str == "Stored Date":
        continue
    # print(f"Checking row {idx + 1}: {date_str}")
    try:
        # Parse M/D/YYYY date format
        parsed_date = datetime.strptime(date_str.strip(), "%m/%d/%Y").date()

        # Check if stored date matches tomorrow's date
        if parsed_date == date.today()+timedelta(days=1):
            # gspread is 1-indexed, so row index = idx + 1
            row_data = sheet.row_values(idx + 1)
            print(f"Match found at row {idx + 1}: {row_data}")
            # 1. Define email details
            sender_email = "nouurmohaamed6777@gmail.com"
            receiver_email = "Salwa.maher@acg-eg.com"
            password = os.getenv("app_password")  # Use an App Password, not your regular password

# 2. Create the body of the message
            body = f"""
Dear Salwa,
This is a reminder that the shipment of PO number "{row_data[0]}" with
- item description: {row_data[5]}
- supplier: {row_data[3]}   
- Quantity: {row_data[7]}
- Total Amount: {row_data[10]}
- shipping method: {row_data[12]}
matches tomorrow's date ({parsed_date.strftime('%m/%d/%Y')}).
"""

# 3. Initialize MIMEText with the body, subtype ('plain'), and charset ('utf-8')
            message = MIMEText(body, "plain", "utf-8")

# 4. Add headers
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Test Python MIME Text Email"

# 5. Send the email via an SMTP server
            try:
    # Example using Gmail's SMTP server
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()  # Upgrade the connection to secure (TLS)
                    server.login(sender_email, password)
                    server.send_message(message)
                    print("Email sent successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")

    except ValueError:
        # Skips non-date text or invalid formats without throwing an error
        continue
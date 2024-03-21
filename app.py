import pymysql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

def connect_to_mysql():
    try:
        # Load environment variables from .env file
        load_dotenv()

        # MySQL Connection Details
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")

        # Connect to MySQL
        connection = pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     database=database)
        return connection
    except Exception as e:
        raise e

def fetch_data(cursor):
    try:
        # Fetch data from MySQL table
        cursor.execute("SELECT * FROM dummy_table")  # Change 'your_table' to 'dummy_table'
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise e

def create_html_table(data):
    try:
        # Create HTML table with CSS styles
        html_table = """<html>
<head>
<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background-color: #f2f2f2;
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    tr:hover {
        background-color: #ddd;
    }
</style>
</head>
<body>
<table>
<tr>
    <th>ID</th>
    <th>Name</th>
    <th>Email</th>
    <th>Age</th>
</tr>"""

        for row in data:
            html_table += "<tr>"
            for col in row:
                html_table += "<td>{}</td>".format(col)
            html_table += "</tr>"
        html_table += "</table></body></html>"
        return html_table
    except Exception as e:
        raise e

def send_email(html_table):
    try:
        # Email Configuration
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        # Sending Email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Data from MySQL Table"
        msg.attach(MIMEText(html_table, 'html'))

        # Connect to SMTP server and send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Example for Gmail SMTP server
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except Exception as e:
        raise e

if __name__ == "__main__":
    try:
        # Connect to MySQL
        connection = connect_to_mysql()
        cursor = connection.cursor()

        # Fetch data from MySQL
        data = fetch_data(cursor)

        # Create HTML table
        html_table = create_html_table(data)

        # Send email
        send_email(html_table)

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

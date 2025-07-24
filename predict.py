import sys
sys.path.append('C:/Users/Ajay kumar/AppData/Local/Programs/Python/Python38/Lib/site-packages')
import pandas as pd
import joblib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MODEL LOADING
model = joblib.load("churn.joblib")

# COLUMNS ORDER CHECK
df = pd.read_csv("dataset.csv")
df = pd.get_dummies(df, drop_first=True)
feature_columns = df.drop('left', axis=1).columns

# INPUT
employee_data = {
    'satisfaction_level': 1.0,
    'last_evaluation': 0.7,
    'number_project': 3,
    'average_montly_hours': 560,
    'time_spend_company': 3,
    'Work_accident': 0,
    'promotion_last_5years': 2,
   
}

# CHECK ALL COLUMNS ARE PRESENT
for col in feature_columns:
    if col not in employee_data:
        employee_data[col] = 0

# PREDICTION FUNCTION
def interpret_and_recommend(employee_data):
    employee_df = pd.DataFrame([employee_data], columns=feature_columns)
    prediction = model.predict(employee_df)[0]
    if prediction == 1:
        return {
            "Risk": "High",
            "Action": "Assign Mentor, Reduce Workload, Monitor Engagement"
        }
    else:
        return {
            "Risk": "Low",
            "Action": "No immediate action needed"
        }

# Get recommendation
recommendation = interpret_and_recommend(employee_data)

# NOTIFICATION FUNCTION
def notify_hr(recommendation):
    return f"Notify HR: Employee is at {recommendation['Risk']} risk. Suggested Action: {recommendation['Action']}"

notification_msg = notify_hr(recommendation)

# Output results
print(f"Employee Risk: {recommendation['Risk']}")
print(f"Recommended Action: {recommendation['Action']}")
print(notification_msg)

# GENERATE REPORT
markdown_content = f"""
#        REPORT

## Sample Prediction and Recommendation
**Employee Risk:** {recommendation['Risk']}  
**Recommended Action:** {recommendation['Action']}

## Notification Simulation
{notification_msg}

"""

md_path = "Single_Employee_Risk_Report.md"
with open(md_path, "w") as f:
    f.write(markdown_content)

# EMAIL TO HR
# MAIL DETAILS
sender_email = "your_email@example.com"
receiver_email = "hr_email@example.com"
subject = "Employee Churn Risk Notification"
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "your_email@example.com"
smtp_password = "your_email_password"

# MAIL MESSAGE
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

body = f"""
Dear HR Team,

{notification_msg}

Regards,
AI Agent
"""
message.attach(MIMEText(body, "plain"))

# Send the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Notification email sent to HR.")
except Exception as e:
    print(f"Failed to send email: {e}")
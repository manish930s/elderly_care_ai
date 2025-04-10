from flask import Flask, render_template, request # type: ignore
from agents.health_agent import HealthAgent
from agents.safety_agent import SafetyAgent
from agents.reminder_agent import ReminderAgent
from agents.llm_agent import LLM_Agent
import pandas as pd
import os

app = Flask(__name__)

# Load agents
health_agent = HealthAgent("data/health_monitoring.csv")    
# safety_agent = SafetyAgent("data/safety_monitoring.csv")
reminder_agent = ReminderAgent("data/daily_reminder.csv")
llm_agent = LLM_Agent()

@app.route("/")
def index():
    user_id = request.args.get("user_id")
    csv_path = "data/health_monitoring.csv"

    if not os.path.exists(csv_path):
        return "CSV file not found. Please make sure 'health_monitoring.csv' exists.", 500

    df = pd.read_csv(csv_path)

    if user_id:
        df = df[df["Device-ID/User-ID"] == user_id]

    heart_rate_labels = df["Timestamp"].tolist() if not df.empty else []
    heart_rate_values = df["Heart Rate"].tolist() if not df.empty else []

    reminder_agent = ReminderAgent("data/daily_reminder.csv")  # ✅ Correct usage
    reminders = reminder_agent.get_reminders(user_id) if user_id else reminder_agent.get_reminders()
    health_alerts = health_agent.get_alerts(user_id) if user_id else []
    safety_agent = SafetyAgent("data/safety_monitoring.csv")  # pass path if required
    # safety_alerts = safety_agent.get_alerts(user_id)
    df.columns = df.columns.str.strip()

    safety_alerts = safety_agent.get_alerts(user_id) if user_id else []
    llm_response = llm_agent.get_health_advice(user_id) if user_id else ""

    return render_template("index.html",
                           reminders=reminders,
                           health_alerts=health_alerts,
                           safety_alerts=safety_alerts,
                           llm_response=llm_response,
                           heart_rate_labels=heart_rate_labels or [],
                           heart_rate_values=heart_rate_values or [])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

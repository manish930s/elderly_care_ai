import pandas as pd

class HealthAgent:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df.columns = self.df.columns.str.strip()

    def get_alerts(self, user_id=None):
        df = self.df
        if user_id:
            df = df[df["Device-ID/User-ID"] == user_id]

        df = df[df["Alert Triggered (Yes/No)"] == "Yes"]

        grouped_alerts = {
            "Cardiovascular": [],
            "Metabolic": [],
            "Respiratory": []
        }

        for _, row in df.iterrows():
            timestamp = row["Timestamp"]
            user = row["Device-ID/User-ID"]

            if row["Heart Rate Below/Above Threshold (Yes/No)"] == "Yes":
                grouped_alerts["Cardiovascular"].append({
                    "user": user,
                    "issue": f"Heart Rate: {row['Heart Rate']} bpm",
                    "details": f"Timestamp: {timestamp}"
                })

            if row["Blood Pressure Below/Above Threshold (Yes/No)"] == "Yes":
                grouped_alerts["Cardiovascular"].append({
                    "user": user,
                    "issue": f"Blood Pressure: {row['Blood Pressure']}",
                    "details": f"Timestamp: {timestamp}"
                })

            if row["Glucose Levels Below/Above Threshold (Yes/No)"] == "Yes":
                grouped_alerts["Metabolic"].append({
                    "user": user,
                    "issue": f"Glucose Level: {row['Glucose Levels']} mg/dL",
                    "details": f"Timestamp: {timestamp}"
                })

            if row["SpO₂ Below Threshold (Yes/No)"] == "Yes":
                grouped_alerts["Respiratory"].append({
                    "user": user,
                    "issue": f"SpO₂: {row['Oxygen Saturation (SpO₂%)']}%",
                    "details": f"Timestamp: {timestamp}"
                })

        return grouped_alerts

# agents/comms_agent.py

class CommsAgent:
    def notify(self, alert):
        if isinstance(alert, dict):
            print(f"[ALERT] 🚨 Notifying for {alert.get('user', 'Unknown User')}: {alert.get('issue', 'Unknown Issue')}")
            print(f"Details: {alert.get('details', 'No details provided.')}")
        else:
            # Fallback if alert is passed as a string
            print(f"[ALERT] 🚨 {alert}")

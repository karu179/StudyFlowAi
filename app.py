import pandas as pd
import gradio as gr
import requests

def generate_schedule(subjects, days_left, hours_per_day):
    # Split subjects into a list
    subjects = [s.strip() for s in subjects.split(",")]
    n = len(subjects)
    slot_hours = round(hours_per_day / 3, 2)

    # Create empty schedule table
    schedule = pd.DataFrame(columns=["Day", "Session", "Subject", "Duration", "Time Slot"])

    # Define professional time slots
    time_slots = ["08:00 - 10:00", "11:00 - 13:00", "15:00 - 17:00"]

    # Fill timetable
    for day in range(1, days_left+1):
        sessions = [
            {"Session": "Morning", "Subject": subjects[(day*0) % n], "Duration": f"{slot_hours} hrs", "Time Slot": time_slots[0]},
            {"Session": "Afternoon", "Subject": subjects[(day*1) % n], "Duration": f"{slot_hours} hrs", "Time Slot": time_slots[1]},
            {"Session": "Evening", "Subject": subjects[(day*2) % n], "Duration": f"{slot_hours} hrs", "Time Slot": time_slots[2]},
        ]
        for s in sessions:
            s["Day"] = day
            schedule = pd.concat([schedule, pd.DataFrame([s])], ignore_index=True)

    # Convert timetable to HTML for email
    schedule_html = schedule.to_html(index=False)

    # Send timetable + message to n8n webhook
    try:
        requests.post(
            "https://yashthite.app.n8n.cloud/webhook-test/studyplan",  # replace with your webhook URL
            json={
                "timetable_html": schedule_html,
                "message": "📚 Smart Study Plan ✨ Stay consistent!"
            }
        )
    except Exception as e:
        print("Error sending to n8n:", e)

    # Always return DataFrame so Gradio displays it
    return schedule

# Gradio interface
iface = gr.Interface(
    fn=generate_schedule,
    inputs=[
        gr.Textbox(label="Enter subjects (comma separated)"),
        gr.Number(label="Days left until exam"),
        gr.Number(label="Study hours per day")
    ],
    outputs="dataframe",
    title="Smart Study Scheduler (Professional Timetable)"
)

iface.launch(share=True)

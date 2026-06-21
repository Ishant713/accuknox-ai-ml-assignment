import sqlite3
import requests
import matplotlib.pyplot as plt
from pathlib import Path


DB_PATH = Path(__file__).parent / "scores.db"


# fetching student data from the API
res = requests.get("http://127.0.0.1:5000/students")

if res.status_code != 200:
    print("API call failed. Is the Flask server running?")
    exit()

students = res.json()["students"]
scores = [s["score"] for s in students]
names = [s["name"] for s in students]


# printing out records and average fo students 
print("\nStudent Records:\n")
for s in students:
    print(f"  {s['name']} : {s['score']}")

avg = sum(scores) / len(scores)
print(f"\nAverage Score: {avg:.2f}")


# save to sqlite
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT,
        score INTEGER
    )
""")

# deleting old data so we don't get duplicate rows on every run
cur.execute("DELETE FROM students")

for s in students:
    cur.execute(
        "INSERT INTO students (name, score) VALUES (?, ?)",
        (s["name"], s["score"])
    )

conn.commit()
conn.close()
print("\nData saved to scores.db.")


#creating bar chart
plt.figure(figsize=(12, 6))
plt.bar(names, scores)
plt.title("Student Test Scores")
plt.xlabel("Student")
plt.ylabel("Score")
plt.xticks(rotation=45)
plt.tight_layout()

chart_path = Path(__file__).parent / "student_scores_chart.png"
plt.savefig(chart_path)
plt.show()

print("Chart saved as student_scores_chart.png")


# Question 2: Data Processing and Visualization

## Objective

Retrieve student test score data using API, calculate the average score, store the data in a SQLite database and then plot a bar chart of the scores.

## Technologies Used

* Python
* Flask
* Requests
* SQLite3
* Matplotlib
* JSON

## Project Overview
For the Question 1, I used a public API (Open Library API) to fetch the book data.

For this question, instead of using any other public API, I have created my own API with the help of Flask. The student data is saved locally in a JSON file called students.json and the data can be fetched from an API through the Flask server.

## API Endpoint

```text
http://127.0.0.1:5000/students
```

## Features

1. Created a own API using Flask.
2. Stored student records in a JSON file.
3. Fetched students data using HTTP requests.
4. Calculated the average score of all students.
5. Then Stored the fetched records in a SQLite database ‘scores.db’.
6. Generate a bar chart to visualize student scores.
7. Saved the chart as `student_scores_chart.png`.

## Project Structure

![Folder Structure](screenshots/folder_struc.png)

## How to Run

### 1. Install Dependencies

```bash
pip install flask requests matplotlib
```

### 2. Start the API Server

```bash
python api_server.py
```

### 3. Run the Visualization Script

```bash
python student_scores_visualization.py
```

## Data Flow

```text
students.json
      ↓
 Flask API Server
      ↓
 HTTP Request
      ↓
 Python Processing
      ↓
 SQLite Database
      ↓
 Bar Chart Visualization
```

## Database Schema

Table: students

| Column | Type    |
| ------ | ------- |
| id     | INTEGER |
| name   | TEXT    |
| score  | INTEGER |

## Average Score

The average score is calculated using:

```python
average_score = sum(scores) / len(scores)
```

Average Score:

```text
82.85
```

## Screenshots

### Terminal Output

![Terminal Output](screenshots/terminal_output.png)

### Student Score Chart

![Bar Chart](screenshots/Bar_chart.png)

### SQLite Database

![SQLite Database](screenshots/sqlite_database.png)

## Assumptions


* Flask server is running brfore running the main code file (student_scores_visualization.py)
* Student data is already stored in a local JSON file.
* Each student record contains a name and score.
* The API response is in valid JSON format.
* Also existing database records are cleared before inserting new records to avoid duplicates storing.

## Conclusion

The whole process of creating a custom API, getting data using HTTP request, processing, storing it in SQLite database and visualization is demonstrated in this project. Also, the use of public APIs (Question 1) and creation of custom API (Question 2) is demonstrated here.
import json
from project.models import Student, Alum, Post

def load_students_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

def load_alumni_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

def load_posts_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

# Load data
students_data = load_students_from_json("students.json")
alumni_data = load_alumni_from_json("alumni.json")
posts_data = load_posts_from_json("posts.json")
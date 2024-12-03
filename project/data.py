import json
from pkg_resources import resource_filename
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
    
# file paths
students_data_filepath = resource_filename('project', 'data/students.json')
alumni_data_filepath = resource_filename('project', 'data/alumni.json')
posts_data_filepath = resource_filename('project', 'data/posts.json')

# Load data
students_data = load_students_from_json(students_data_filepath)
alumni_data = load_alumni_from_json(alumni_data_filepath)
posts_data = load_posts_from_json(posts_data_filepath)

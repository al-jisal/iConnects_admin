import os
import openai
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
from project import db
from project.models import Student, Alum, Post

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

main_blueprint = Blueprint('index', __name__)

from sqlalchemy.sql import text

def generate_models_context():
    """
    Generate a summary of all SQLAlchemy models, their columns, relationships, and all rows of data.
    """
    models_context = "You are working with the following SQLAlchemy models and data:\n\n"

    for table_name, table in db.Model.metadata.tables.items():
        models_context += f"Model '{table_name}':\n"

        for column in table.columns:
            models_context += f" - {column.name} ({str(column.type)})\n"

        relationships = [rel.key for rel in getattr(db.Model._decl_class_registry.get(table_name, None), '__mapper__', {}).relationships]
        if relationships:
            models_context += "Relationships:\n"
            for relationship in relationships:
                models_context += f"   - {relationship}\n"

        query = text(f"SELECT * FROM {table_name}")
        result = db.session.execute(query)
        rows = result.fetchall()

        if rows:
            models_context += "All rows:\n"
            for row in rows:
                models_context += f"   {dict(row)}\n"
        else:
            models_context += "No data available.\n"

        models_context += "\n"

    return models_context


@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@main_blueprint.route('/submit_query', methods=['POST'])
def submit_query():
    user_query = request.form.get('query')
    if not user_query or user_query.strip() == "":
        return jsonify({"error": "No query provided. Please provide a valid natural language query."})

    models_context = generate_models_context()

    prompt = f"""
    {models_context}\n
    Convert the following natural language query into a SQLAlchemy operation:
    '{user_query}'
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in SQLAlchemy and database operations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0
        )

        sqlalchemy_command = response['choices'][0]['message']['content'].strip()

        if not sqlalchemy_command or "cannot" in sqlalchemy_command.lower():
            return jsonify({"error": "The AI could not generate a valid SQLAlchemy command.", "response": sqlalchemy_command})

        try:
            exec(sqlalchemy_command)
            db.session.commit()
            return jsonify({"message": "Query executed successfully.", "command": sqlalchemy_command})
        except Exception as db_error:
            db.session.rollback()
            return jsonify({"error": str(db_error), "command": sqlalchemy_command})

    except Exception as api_error:
        return jsonify({"error": "Failed to generate SQLAlchemy command.", "details": str(api_error)})
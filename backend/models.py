from datetime import datetime
from database import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    learning_objectives = db.Column(db.Text, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship("Question", backref="project", cascade="all, delete-orphan")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    selected_objectives = db.Column(db.Text, nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    generated_question = db.Column(db.Text, nullable=False)
    scenario = db.Column(db.Integer)
    alignment = db.Column(db.Integer)
    complexity = db.Column(db.Integer)
    clarity = db.Column(db.Integer)
    feasibility = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
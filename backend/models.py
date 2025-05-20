from datetime import datetime, timezone
from database import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    learning_objectives = db.Column(db.Text, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    problems = db.relationship("Problem", backref="project", cascade="all, delete-orphan")

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    type = db.Column(db.Text, nullable=False)
    target_objectives = db.Column(db.Text, nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    generated_problem = db.Column(db.Text, nullable=False)
    sample_answer = db.Column(db.Text)
    scenario = db.Column(db.Integer)
    alignment = db.Column(db.Integer)
    complexity = db.Column(db.Integer)
    clarity = db.Column(db.Integer)
    feasibility = db.Column(db.Integer)
    evaluation_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
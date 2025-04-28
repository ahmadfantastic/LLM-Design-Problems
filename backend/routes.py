from flask import Blueprint, request, jsonify, abort
from database import db
from models import Project, Question
from openai_client import generate_question

api = Blueprint("api", __name__)

# ---- Projects ----
@api.route("/projects", methods=["GET"])
def list_projects():
    return jsonify([p_to_dict(p) for p in Project.query.order_by(Project.created_at.desc())])

@api.route("/projects", methods=["POST"])
def create_project():
    data = request.json or {}
    p = Project(name=data.get("name"),
                learning_objectives=data.get("learning_objectives"),
                task_description=data.get("task_description"),
                technologies=data.get("technologies"))
    db.session.add(p)
    db.session.commit()
    return jsonify(p_to_dict(p)), 201

@api.route("/projects/<int:pid>", methods=["PATCH"])
def update_project(pid):
    p = Project.query.get_or_404(pid)
    data = request.json or {}
    if "name" in data:
        p.name = data["name"]
    if "learning_objectives" in data:
        p.learning_objectives = data["learning_objectives"]
    if "task_description" in data:
        p.task_description = data["task_description"]
    if "technologies" in data:
        p.technologies = data["technologies"]
    db.session.commit()
    return jsonify(p_to_dict(p))

@api.route("/projects/<int:pid>")
def get_project(pid):
    p = Project.query.get_or_404(pid)
    return jsonify(p_to_dict(p, with_questions=True))


# ---- Questions ----
@api.route("/projects/<int:pid>/questions", methods=["POST"])
def create_question(pid):
    project = Project.query.get_or_404(pid)
    target_objs: str = request.json.get("selected_objectives", "")
    prompt, q_text = generate_question(project.learning_objectives,
                                       project.task_description,
                                       project.technologies,
                                       target_objs)
    q = Question(project_id=pid,
                 selected_objectives=target_objs,
                 prompt=prompt,
                 generated_question=q_text)
    db.session.add(q)
    db.session.commit()
    return jsonify(q_to_dict(q, full=True)), 201


@api.route("/questions/<int:qid>")

def get_question(qid):
    q = Question.query.get_or_404(qid)
    return jsonify(q_to_dict(q, full=True))

@api.route("/questions/<int:qid>", methods=["DELETE"])
def delete_question(qid):
    q = Question.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return '', 204  # No content

@api.route("/questions/<int:qid>/evaluate", methods=["POST"])

def evaluate_question(qid):
    q = Question.query.get_or_404(qid)
    data = request.json or {}
    for k in ["scenario", "alignment", "complexity", "clarity", "feasibility"]:
        if k in data:
            setattr(q, k, int(data[k]))
    db.session.commit()
    return jsonify(q_to_dict(q, full=True))

# ---- Helpers ----

def p_to_dict(p: Project, with_questions=False):
    d = {
        "id": p.id,
        "name": p.name,
        "learning_objectives": p.learning_objectives,
        "task_description": p.task_description,
        "technologies": p.technologies,
        "created_at": p.created_at.isoformat(),
    }
    if with_questions:
        d["questions"] = [q_to_dict(q) for q in p.questions]
    return d

def q_to_dict(q: Question, full=False):
    d = {
        "id": q.id,
        "project_id": q.project_id,
        "selected_objectives": q.selected_objectives,
        "generated_question": q.generated_question,
        "scenario": q.scenario,
        "alignment": q.alignment,
        "complexity": q.complexity,
        "clarity": q.clarity,
        "feasibility": q.feasibility,
        "created_at": q.created_at.isoformat(),
    }
    if full:
        d["prompt"] = q.prompt
    return d
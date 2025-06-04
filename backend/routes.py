from flask import Blueprint, request, jsonify, abort
from database import db
from models import Project, Problem
from openai_client import generate_problem, generate_answer

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
    return jsonify(p_to_dict(p, with_problems=True))


# ---- Problems ----
@api.route("/projects/<int:pid>/problems", methods=["POST"])
def create_problem(pid):
    project = Project.query.get_or_404(pid)
    target_objs: str = request.json.get("target_objectives", "")
    type: str = request.json.get("type", "open")
    count: int = request.json.get("count")

    VALID_TYPES = {"open", "multiple_choice"}
    if type not in VALID_TYPES:
        return jsonify({"error": f"Invalid problem type: '{type}'"}), 400
    count = request.json.get("count")
    if count is None:
        return jsonify({"error": "Missing 'count' in request"}), 400
    try:
        count = int(count)
    except (ValueError, TypeError):
        return jsonify({"error": f"Invalid count: '{count}' (must be an integer)"}), 400
    if count < 1 or count > 10:
        return jsonify({"error": f"Invalid count: '{count}' (must be between 1 and 10)"}), 400

    for i in range(count):
        prompt, q_text = generate_problem(project.learning_objectives,
                                        project.task_description,
                                        project.technologies,
                                        target_objs, type)
        q = Problem(project_id=pid,
                    type=type,
                    target_objectives=target_objs,
                    prompt=prompt,
                    generated_problem=q_text)
        db.session.add(q)
        db.session.commit()
    return jsonify(q_to_dict(q, full=True)), 201


@api.route("/problems/<int:qid>")
def get_problem(qid):
    q = Problem.query.get_or_404(qid)
    return jsonify(q_to_dict(q, full=True))


@api.route("/problems/<int:qid>", methods=["DELETE"])
def delete_problem(qid):
    q = Problem.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return '', 204  # No content


@api.route("/problems/<int:qid>/evaluate", methods=["POST"])
def evaluate_problem(qid):
    problem = Problem.query.get_or_404(qid)
    data = request.json or {}
    for k in ["scenario", "alignment", "complexity", "clarity", "feasibility"]:
        if k in data:
            score = int(data[k])
            if score < 0 or score > 2:
                return jsonify({"error": f"Invalid score for {k}: {score}"}), 400
            setattr(problem, k, score)
    problem.evaluation_note = data.get("evaluation_note")
    db.session.commit()
    return jsonify(q_to_dict(problem, full=True))


@api.route("/problems/<int:qid>/answer", methods=["POST"])
def answer_problem(qid):
    problem = Problem.query.get_or_404(qid)
    problem.sample_answer = generate_answer(problem.generated_problem, problem.type)
    db.session.commit()
    return jsonify(q_to_dict(problem, full=True))

# ---- Helpers ----

def p_to_dict(p: Project, with_problems=False):
    d = {
        "id": p.id,
        "name": p.name,
        "learning_objectives": p.learning_objectives,
        "task_description": p.task_description,
        "technologies": p.technologies,
        "problem_count": len(p.problems),
        "created_at": p.created_at.isoformat(),
    }
    if with_problems:
        d["problems"] = [q_to_dict(q) for q in p.problems]
    return d

def q_to_dict(q: Problem, full=False):
    d = {
        "id": q.id,
        "project_id": q.project_id,
        "type": q.type,
        "target_objectives": q.target_objectives,
        "generated_problem": q.generated_problem,
        "sample_answer": q.sample_answer,
        "scenario": q.scenario,
        "alignment": q.alignment,
        "complexity": q.complexity,
        "clarity": q.clarity,
        "feasibility": q.feasibility,
        "evaluation_note": q.evaluation_note,
        "created_at": q.created_at.isoformat(),
    }
    if full:
        d["prompt"] = q.prompt
    return d
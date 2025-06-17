from flask import Blueprint, request, jsonify, abort, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import Project, Problem, User, Evaluation
from openai_client import generate_problem, generate_answer

api = Blueprint("api", __name__)


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user():
            abort(401)
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or not user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper


# ---- Authentication ----

@api.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    user = User.query.filter_by(username=data.get("username")).first()
    if not user:
        abort(401)

    password = data.get("password")
    # If the user has no password set yet, require them to set one
    if user.password_hash is None:
        if not password:
            return jsonify({"set_password_required": True}), 400
        user.password_hash = generate_password_hash(password)
        db.session.commit()

    if not check_password_hash(user.password_hash, password or ""):
        abort(401)

    session["user_id"] = user.id
    return jsonify({"username": user.username, "is_admin": user.is_admin})


@api.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return "", 204


@api.route("/current_user")
def get_current_user_route():
    user = current_user()
    if not user:
        return jsonify(None)
    return jsonify({"id": user.id, "username": user.username, "is_admin": user.is_admin})


@api.route("/register", methods=["POST"])
@admin_required
def register_user():
    data = request.json or {}
    if not data.get("username"):
        abort(400)
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    user = User(
        username=data["username"],
        password_hash=None,
        is_admin=bool(data.get("is_admin")),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username, "is_admin": user.is_admin}), 201


@api.route("/users/<int:uid>/reset_password", methods=["POST"])
@admin_required
def reset_password(uid):
    user = User.query.get_or_404(uid)
    user.password_hash = None
    db.session.commit()
    return "", 204

# ---- Projects ----
@api.route("/projects", methods=["GET"])
def list_projects():
    return jsonify([p_to_dict(p) for p in Project.query.order_by(Project.created_at.desc())])

@api.route("/projects", methods=["POST"])
@login_required
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
    user = current_user()
    return jsonify(p_to_dict(p, user=user, with_problems=True))


@api.route("/projects/<int:pid>/stats")
@login_required
def project_stats(pid):
    project = Project.query.get_or_404(pid)
    user = current_user()
    metrics = ["scenario", "alignment", "complexity", "clarity", "feasibility"]

    user_evals = Evaluation.query.join(Problem).filter(
        Evaluation.user_id == user.id,
        Problem.project_id == pid
    ).all()

    def avg_for(evals, field):
        vals = [getattr(e, field) for e in evals if getattr(e, field) is not None]
        return sum(vals) / len(vals) if vals else None

    user_avg = {m: avg_for(user_evals, m) for m in metrics}

    overall_avg = None
    kappa = None
    if user.is_admin:
        all_evals = Evaluation.query.join(Problem).filter(Problem.project_id == pid).all()
        overall_avg = {m: avg_for(all_evals, m) for m in metrics}

        # build evaluations by user and problem
        evaluations_by_user = {}
        for ev in all_evals:
            evaluations_by_user.setdefault(ev.user_id, {})[ev.problem_id] = ev

        def cohen_kappa(r1, r2):
            n = len(r1)
            if n == 0:
                return None
            categories = [0, 1, 2]
            po = sum(1 for a, b in zip(r1, r2) if a == b) / n
            p1 = {c: r1.count(c) / n for c in categories}
            p2 = {c: r2.count(c) / n for c in categories}
            pe = sum(p1[c] * p2[c] for c in categories)
            return 1.0 if pe == 1 else (po - pe) / (1 - pe)

        from itertools import combinations
        kappa_vals = {m: [] for m in metrics}
        users = list(evaluations_by_user.keys())
        for u1, u2 in combinations(users, 2):
            probs = set(evaluations_by_user[u1].keys()) & set(evaluations_by_user[u2].keys())
            if not probs:
                continue
            for m in metrics:
                r1 = [getattr(evaluations_by_user[u1][pid], m) for pid in probs if getattr(evaluations_by_user[u1][pid], m) is not None and getattr(evaluations_by_user[u2][pid], m) is not None]
                r2 = [getattr(evaluations_by_user[u2][pid], m) for pid in probs if getattr(evaluations_by_user[u1][pid], m) is not None and getattr(evaluations_by_user[u2][pid], m) is not None]
                if len(r1):
                    score = cohen_kappa(r1, r2)
                    if score is not None:
                        kappa_vals[m].append(score)
        kappa = {m: (sum(v)/len(v) if v else None) for m, v in kappa_vals.items()}

    return jsonify({"user_avg": user_avg, "overall_avg": overall_avg, "kappa": kappa})


# ---- Problems ----
@api.route("/projects/<int:pid>/problems", methods=["POST"])
@login_required
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
@login_required
def get_problem(qid):
    q = Problem.query.get_or_404(qid)
    user = current_user()
    return jsonify(q_to_dict(q, user=user, full=True))


@api.route("/problems/<int:qid>", methods=["DELETE"])
def delete_problem(qid):
    q = Problem.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return '', 204  # No content


@api.route("/problems/<int:qid>/evaluate", methods=["POST"])
@login_required
def evaluate_problem(qid):
    problem = Problem.query.get_or_404(qid)
    user = current_user()
    data = request.json or {}
    evaluation = Evaluation.query.filter_by(problem_id=qid, user_id=user.id).first()
    if not evaluation:
        evaluation = Evaluation(problem_id=qid, user_id=user.id)
    for k in ["scenario", "alignment", "complexity", "clarity", "feasibility"]:
        if k in data:
            score = int(data[k])
            if score < 0 or score > 2:
                return jsonify({"error": f"Invalid score for {k}: {score}"}), 400
            setattr(evaluation, k, score)
    evaluation.evaluation_note = data.get("evaluation_note")
    db.session.add(evaluation)
    db.session.commit()
    return jsonify(q_to_dict(problem, user=user, full=True))


@api.route("/problems/<int:qid>/answer", methods=["POST"])
@login_required
def answer_problem(qid):
    problem = Problem.query.get_or_404(qid)
    problem.sample_answer = generate_answer(problem.generated_problem, problem.type)
    db.session.commit()
    return jsonify(q_to_dict(problem, full=True))

# ---- Helpers ----

def p_to_dict(p: Project, user=None, with_problems=False):
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
        d["problems"] = [q_to_dict(q, user=user) for q in p.problems]
    return d


def q_to_dict(q: Problem, user=None, full=False):
    d = {
        "id": q.id,
        "project_id": q.project_id,
        "type": q.type,
        "target_objectives": q.target_objectives,
        "generated_problem": q.generated_problem,
        "sample_answer": q.sample_answer,
        "created_at": q.created_at.isoformat(),
    }

    metrics = ["scenario", "alignment", "complexity", "clarity", "feasibility", "evaluation_note"]
    if user:
        ev = Evaluation.query.filter_by(problem_id=q.id, user_id=user.id).first()
        if ev:
            for m in metrics:
                d[m] = getattr(ev, m)
        else:
            for m in metrics:
                d[m] = None
        if user.is_admin:
            d["all_evaluations"] = [
                {
                    "user_id": e.user_id,
                    **{m: getattr(e, m) for m in metrics}
                }
                for e in q.evaluations
            ]
    if full:
        d["prompt"] = q.prompt
    return d

import os
from google import genai
from config import Config

# Configure Gemini client
client = genai.Client(api_key=Config.GEMINI_API_KEY)

def generate_problem(full_objs: str, task_desc: str, technologies: str, target_objs: str, type: str, model: str | None = None):
    prompt_template = load_prompt_template(type)

    prompt = prompt_template.format(
        full_learning_objectives=full_objs,
        task_description=task_desc,
        technologies=technologies,
        target_objectives=target_objs,
    )
    response = client.models.generate_content(
        model= model or Config.GEMINI_DEFAULT_MODEL,
        config={"temperature": 0.7},
        contents=prompt
    )
    return prompt, response.text


def generate_answer(problem: str, type: str, model: str | None = None):
    if type == "open":
        template = """ In one paragraph answer this problem: {problem}"""
    elif type == "multiple_choice":
        template = """ Briefly, what is the answer to this problem: {problem}"""
    else:
        template = """ In few sentences answer this problem: {problem}"""

    prompt = template.format(problem=problem)
    response = client.models.generate_content(
        model= model or Config.GEMINI_DEFAULT_MODEL,
        config={"temperature": 0},
        contents=prompt
    )
    return response.text


def evaluate_problem_llm(full_objs: str, task_desc: str, technologies: str, target_objs: str, problem: str, model: str | None = None):
    """Ask the LLM to evaluate a problem and return the raw JSON string."""
    prompt_template = load_prompt_template("evaluate")

    prompt = prompt_template.format(
        full_learning_objectives=full_objs,
        task_description=task_desc,
        technologies=technologies,
        target_learning_objectives=target_objs,
        problem=problem,
    )
    response = client.models.generate_content(
        model= model or Config.GEMINI_DEFAULT_MODEL,
        config={"temperature": 0, "response_mime_type": "application/json",},
        contents=prompt
    )
    return response.text


def load_prompt_template(type: str):
    filename = f"prompt_{type}.txt"
    filepath = os.path.join("prompts", filename)
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

import os
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_problem(full_objs: str, task_desc: str, technologies: str, target_objs: str, type: str):
    prompt_template = load_prompt_template(type)

    prompt = prompt_template.format(
        full_learning_objectives=full_objs,
        task_description=task_desc,
        technologies=technologies,
        target_objectives=target_objs,
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user", 
            "content": prompt
            }],
        temperature=0.7,
    )
    return prompt, response.choices[0].message.content.strip()


def generate_answer(problem: str, type: str):
    if type == "open":
        template = """ In one paragraph answer this problem: {problem}"""
    elif type == "multiple_choice":
        template = """ Briefly, what is the answer to this problem: {problem}"""
    else:
        template = """ In few sentences answer this problem: {problem}"""

    prompt = template.format(
        problem=problem,
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def evaluate_problem_llm(full_objs: str, task_desc: str, technologies: str, target_objs: str, problem: str):
    """Ask the LLM to evaluate a problem and return the raw JSON string."""
    prompt_template = load_prompt_template("evaluate")

    prompt = prompt_template.format(
        full_learning_objectives=full_objs,
        task_description=task_desc,
        technologies=technologies,
        target_learning_objectives=target_objs,
        problem=problem,
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content.strip()

def load_prompt_template(type: str):
    filename = f"prompt_{type}.txt"
    filepath = os.path.join("prompts", filename)
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


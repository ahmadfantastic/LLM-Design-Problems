import os
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

PROMPT_TEMPLATE = """
You are an expert computing education assistant. 
You will generate a short exam problem-solving question for students to solve.

Format Requirements:
- The question should begin with a short, realistic scenario.
- The question should test higher-order thinking skills
- The question should be in a different context from the project.
- The expected answer length is a few sentences to one paragraph.
- Students should be able to answer in 30 minutes.
- Ensure to adequately explain concepts in the domain problem that are potentially unfamiliar to students.

Generate a distinct question that aligns with these requirements based on the following course and project details:

1. Course Overview & Learning Objectives:  
{full_learning_objectives}

2. Project and Tasks Description Completed by Students:
{task_description}

3. Key Technologies, Techniques, and Tools used in the Project:
{technologies} 

4. Target Learning Objectives of the Question
{target_objectives}

Output format:
Scenario: <Brief context description>
Question: <Specific problem-solving question posed to students>
"""

def generate_question(full_objs: str, task_desc: str, technologies: str, target_objs: str):
    prompt = PROMPT_TEMPLATE.format(
        full_learning_objectives=full_objs,
        task_description=task_desc,
        technologies=technologies,
        target_objectives=target_objs,
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # swap easily
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return prompt, response.choices[0].message.content.strip()
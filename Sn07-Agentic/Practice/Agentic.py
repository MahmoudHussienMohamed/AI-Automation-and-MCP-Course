from OpenAIAgent import OpenAIAgent
import json

analyzer_agent = OpenAIAgent(
    system_prompt="""
You're an Agent that analyze the user query, and povide detailed observations of the user input.
""",
    prompt_template="""
    Concisely, Analyze the following user query to create a software app. The Analysis should be clear to start implementing the system.
    User Query: \"\"\"{query}\"\"\"
"""
)

# query = input('Query: ')
query = 'develop a system that organize the assets of IT department in a company using python.'
# for chunk in analyzer_agent.stream_chat(query=query):
#     print(chunk, end='', flush=True)
analysis = analyzer_agent.nonstream_chat(query=query)
# analysis = "analyzer_agent.nonstream_chat(query=query)"
print(f'{analysis=}', end=f"\n{'-' * 100}\n")

planner_system_prompt = """
You're an Agent that plan the user request into small tasks, and povide detailed descriptions of the inquirey to accomplish the task.
"""
planner_prompt_temp = """
    Provid a detailed plan of the following user query: \"\"\"{query}\"\"\"
    and here is a detailed analysis of it: \"\"\"{analysis}\"\"\"
    ## Instructions:
    - You should provide an execution plan of the software (max 3 planning milestone).
    - Respond *ONLY* with list of the plan as json object list with each object has "task" and "description" keys such as:
    [
        {{ "task": <title>, "description": <description> }},
        ...
    ]
    no side talking just the json list without formatting
"""
planner_prompt_temp = planner_prompt_temp.format(query=query, analysis=analysis)
print(planner_prompt_temp)
planner_agent = OpenAIAgent(
    system_prompt=planner_system_prompt,
    prompt_template=planner_prompt_temp
)


plan = planner_agent.nonstream_chat(query=query)
plan = json.loads(plan)
print(f'{plan=}', end=f"\n{'-' * 100}\n")

exec_agent = OpenAIAgent(
    system_prompt="""
""",
    prompt_template="""
"""
)

for milestone in plan:
    sub_analysis = analyzer_agent.nonstream_chat(query=milestone)
    planner_milestones = planner_agent.nonstream_chat(query=query, analysis=sub_analysis)
    exec_agent.execute(planner_milestones)
    
for chunk in planner_agent.stream_chat(query=query):
    print(chunk, end='', flush=True)


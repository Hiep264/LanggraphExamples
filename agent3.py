from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: float
    skills: List[str]
    result: str

def greeting(state: AgentState):
    """"""
    state['result'] = f"Hi {state['name']}, welcome!!!"
    return state

def describe_age(state: AgentState):
    """"""
    state['result'] = state['result'] + f" You are {state['age']} years old."
    return state

def show_skills(state: AgentState):
    """"""
    skills = state['skills']
    skills_list = skills[0] if len(skills) == 1 else f"{', '.join(skills[0:-1])} and {skills[-1]}."
    state['result'] += f" You have skills in {skills_list}"
    return state

workflow = StateGraph(AgentState)
workflow.add_node("greeting user", greeting)
workflow.add_node("describe user's age", describe_age)
workflow.add_node("show user's skills", show_skills)
workflow.set_entry_point("greeting user")
workflow.add_edge("greeting user", "describe user's age")
workflow.add_edge("describe user's age", "show user's skills")
workflow.set_finish_point("show user's skills")
agent = workflow.compile()

with open("img/agent3.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

answer = agent.invoke({
    "age": 21,
    "name": 21,
    "skills": ["Python", "ML", "AI", "FastAPI"]
})

print(answer["result"])
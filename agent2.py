from typing import TypedDict, List
from langgraph.graph import StateGraph
from math import prod

class AgentState(TypedDict):
    num: List[int]
    name: str
    operator: str
    result: str

def calculate_tool(state: AgentState) -> AgentState:
    """Simple function to calculate value from state"""
    if state['operator'] == '+':
        state['result'] = f"Hi {state['name']}, Your answer is {sum(state['num'])}"
    elif state['operator'] == '*':
        state['result'] = f"Hi {state['name']}, Your answer is {prod(state['num'])}"
    else:
        state['result'] = "Something wrong!"

    return state

workflow = StateGraph(AgentState)
workflow.add_node("cal", calculate_tool)
workflow.set_entry_point("cal")
workflow.set_finish_point("cal")
agent = workflow.compile()

with open("img/agent2.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

answer  = agent.invoke({
    "name": "H",
    "num": [1,2,3,4,5],
    "operator": "-",
})

print(answer["result"])
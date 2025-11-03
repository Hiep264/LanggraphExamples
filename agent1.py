from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str

def compliment_tool(state: AgentState) -> AgentState:
    """Simple function that give a person a compliment"""
    state['name'] = "Good job " + state['name'] + ", you're doing well!"
    return state

workflow = StateGraph(AgentState)
workflow.add_node("compliment node", compliment_tool)
workflow.set_entry_point("compliment node")
workflow.set_finish_point("compliment node")

agent = workflow.compile()

with open("img/agent1.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

print("Agent run: ")
print(agent.invoke({
    "name": "Hiep"
})["name"])
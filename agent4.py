from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    num1: int
    num2: int
    num3: int
    num4: int
    op1: str
    op2: str
    ans1: int
    ans2: int

def add1(state: AgentState) -> AgentState:
    """This node will add 2 numbers"""
    state['ans1'] = state['num1'] + state['num2']
    return state

def add2(state: AgentState) -> AgentState:
    """This node will add 2 numbers"""
    state['ans2'] = state['num3'] + state['num4']
    return state

def sub1(state: AgentState) -> AgentState:
    """This node will subtracts 2 numbers"""
    state['ans1'] = state['num1'] - state['num2']
    return state

def sub2(state: AgentState) -> AgentState:
    """This node will subtracts 2 numbers"""
    state['ans2'] = state['num3'] - state['num4']
    return state

def router1(state: AgentState):
    """This node will decide next node"""
    if state['op1'] == "+":
        return "add num1 and num2"
    elif state['op1'] == "-":
        return "sub num1 and num2"
    else:
        END

def router2(state: AgentState):
    """This node will decide next node"""
    if state['op2'] == "+":
        return "add num3 and num4"
    elif state['op2'] == "-":
        return "sub num3 and num4"
    else:
        END

workflow = StateGraph(AgentState)

# add nodes
workflow.add_node("add node 1", add1)
workflow.add_node("add node 2", add2)
workflow.add_node("sub node 1", sub1)
workflow.add_node("sub node 2", sub2)
workflow.add_node("router node 1", lambda state:state)
workflow.add_node("router node 2", lambda state:state)

# add edges
workflow.add_edge(START, "router node 1")
workflow.add_conditional_edges(
    "router node 1",
    router1,
    {
        # EDGE : NODE
        "add num1 and num2": "add node 1",
        "sub num1 and num2": "sub node 1"
    }
)
workflow.add_edge("add node 1", "router node 2")
workflow.add_edge("sub node 1", "router node 2")
workflow.add_conditional_edges(
    "router node 2",
    router2,
    {
        "add num3 and num4": "add node 2",
        "sub num3 and num4": "sub node 2"
    }
)
workflow.add_edge("add node 2", END)
workflow.add_edge("sub node 2", END)

agent = workflow.compile()

with open("img/agent4.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

initial_state = AgentState(num1=10, num2=5, num3=7, num4=2, op1="-", op2="+", ans1=0, ans2=0)
print(agent.invoke(initial_state)["ans1"])
print(agent.invoke(initial_state)["ans2"])


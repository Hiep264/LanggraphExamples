from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
import random

class AgentState(TypedDict):
    name: str
    target: int
    guesses: List[int]
    count: int
    hint: str
    lower_bound: int
    upper_bound: int

def setup_tool(state: AgentState) -> AgentState:
    """Initialize variables"""
    state['name'] = f"Welcome {state['name']} to the game!!!"
    state['target'] = random.randint(1,10)
    state['count'] = 0
    state['lower_bound'] = 1
    state['upper_bound'] = 10
    print("The Game is Started!!!")
    return state

def guess_tool(state: AgentState) -> AgentState:
    """Generate a new number"""
    num_available = [i for i in range(state['lower_bound'], state['upper_bound'] + 1) if i not in state['guesses']]
    num = random.choice(num_available)
    state['guesses'].append(num)
    state['count'] += 1
    print(f"Attempt {state['count']}: Guessing {num} and the current range is between {state['lower_bound']} - {state['upper_bound']}.")
    return state

def hint_tool(state: AgentState) -> AgentState:
    """Provide a hint base on the last guess"""
    last_guess = state['guesses'][-1]
    target = state['target']

    if last_guess < target:
        state['hint'] = f"The last guess {last_guess} is too low. Try a higher number."
        print(state['hint'])
        state["lower_bound"] = max(state["lower_bound"], last_guess + 1)
    elif last_guess > target:
        state['hint'] = f"The last guess {last_guess} is too high. Try a lower number."
        print(state['hint'])
        state['upper_bound'] = min(state['upper_bound'], last_guess - 1)
    else:
        state['hint'] = f"Correct number!! You found the target {target} in {state['count']} tries."
        print(state['hint'])
    return state

def loop_tool(state: AgentState) -> AgentState:
    """Determine if the game should continue or stop"""
    last_guess = state['guesses'][-1]

    if last_guess == state["target"]:
        print("Found Target!!")
        return "stop"
    elif state['count'] > 5:
        print(f"Reach max attempt! Can't find the target.")
        return "stop"
    else:
        print(f"Continue: {state['count']}/5!!")
        return "continue"
    
workflow = StateGraph(AgentState)

#add nodes
workflow.add_node("set up node", setup_tool)
workflow.add_node("guess node", guess_tool)
workflow.add_node("hint node", hint_tool)

# add edges
workflow.add_edge(START, "set up node")
workflow.add_edge("set up node", "guess node")
workflow.add_edge("guess node", "hint node")
workflow.add_conditional_edges(
    "hint node",
    loop_tool,
    {
        "stop": END,
        "continue": "guess node"
    }
)

agent = workflow.compile()

with open("img/agent5.png", 'wb') as f:
    f.write(agent.get_graph().draw_mermaid_png())
    
answer = agent.invoke({
    "name": "Me",
    "guesses": []
})
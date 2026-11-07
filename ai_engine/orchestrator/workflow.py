from langgraph.graph import StateGraph, START, END
from orchestrator.state import State
from orchestrator.nodes import requirement_node, architecture_node, testing_node, documentation_node
from human_review.review_handler import human_review_node
from langgraph.checkpoint.memory import MemorySaver

def route_after_review(state: State):
    stage = state['current_stage']
    decision = state['review_decision']

    if decision == 'revise':
        return {
            "requirements": "requirement",
            "architecture": "architecture",
            "test_plan": "testing",
            "documentation": "documentation"
        }[stage]
    
    if decision == "approve":
        return {
            "requirements": "architecture",
            "architecture": "testing",
            "test_plan": "documentation",
            "documentation": END
        }[stage]
    
    raise ValueError("Invalid review decision")

graph = StateGraph(State)

graph.add_node("requirement", requirement_node)
graph.add_node("architecture", architecture_node)
graph.add_node("testing", testing_node)
graph.add_node("documentation", documentation_node)
graph.add_node("human_review", human_review_node)

graph.add_edge(START, "requirement")
graph.add_edge("requirement", "human_review")
graph.add_edge("architecture", "human_review")
graph.add_edge("testing", "human_review")
graph.add_edge("documentation", "human_review")
graph.add_conditional_edges("human_review", route_after_review)

memory = MemorySaver()

workflow = graph.compile(checkpointer=memory)
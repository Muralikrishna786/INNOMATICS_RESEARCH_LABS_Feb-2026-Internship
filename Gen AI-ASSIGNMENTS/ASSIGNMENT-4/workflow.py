from langgraph.graph import StateGraph, END
from retriever import get_retriever, get_llm
from hitl import escalate_to_human
from typing import TypedDict

# Initialize
retriever = get_retriever()
llm = get_llm()

# -------------------------
# Safe State Wrapper
# -------------------------
def safe_state(state):
    return state if state else {}

# -------------------------
# Shared State
# -------------------------
class GraphState(TypedDict, total=False):
    query: str
    intent: str
    context: str
    response: str

# -------------------------
# 1. Intent Detection
# -------------------------
def detect_intent(state):
    state = safe_state(state)

    query = state.get("query", "").lower()

    if "refund" in query:
        state["intent"] = "billing"
    elif "delivery" in query:
        state["intent"] = "shipping"
    elif "problem" in query:
        state["intent"] = "technical"
    else:
        state["intent"] = "general"

    return state

# -------------------------
# 2. Retrieval
# -------------------------
def retrieve_docs(state):
    query = state.get("query", "")

    docs = retriever.invoke(query)

    # remove duplicates
    seen = set()
    unique_docs = []

    for d in docs:
        if d.page_content not in seen:
            unique_docs.append(d)
            seen.add(d.page_content)

    if not unique_docs:
        state["context"] = ""
        return state

    state["context"] = "\n\n".join(
        d.page_content for d in unique_docs[:3]
    )

    return state
# -------------------------
# 3. Generate Answer
# -------------------------
def generate_answer(state):
    state = safe_state(state)

    context = state.get("context", "").strip()
    query = state.get("query", "").lower()

    if not context:
        state["response"] = "No relevant information found."
        return state

    # ✅ RULE-BASED EXTRACTION (for definition questions)
    if "what is" in query or "define" in query:
        for line in context.split("\n"):
            if "called" in line.lower():
                state["response"] = line.strip()
                return state

    # ✅ FALLBACK TO LLM
    prompt = f"""
You are a customer support assistant.

Answer using ONLY the given context.
Give a clear and concise answer.

Context:
{context}

Question:
{state.get("query", "")}

Answer:
"""

    try:
        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            state["response"] = response.content.strip()
        else:
            state["response"] = str(response).strip()

    except Exception as e:
        print("LLM ERROR:", e)
        state["response"] = "⚠️ Error generating response. Please try again."

    return state

# -------------------------
# 4. Routing
# -------------------------
def route_decision(state):
    if state.get("intent") in ["billing", "technical"]:
        return "human"

    if not state.get("context"):
        return "human"

    return "generate"
# -------------------------
# Build Graph
# -------------------------
def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("intent", detect_intent)
    builder.add_node("retrieve", retrieve_docs)
    builder.add_node("generate", generate_answer)
    builder.add_node("human", escalate_to_human)

    builder.set_entry_point("intent")

    builder.add_edge("intent", "retrieve")

    builder.add_conditional_edges(
        "retrieve",
        route_decision,
        {
            "generate": "generate",
            "human": "human"
        }
    )

    builder.add_edge("generate", END)
    builder.add_edge("human", END)

    return builder.compile()
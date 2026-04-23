def escalate_to_human(state):
    if state is None:
        state = {}

    print("\n⚠️ Escalating to human support...\n")

    state["response"] = "Your query has been forwarded to a human agent."

    return state   # ✅ MUST RETURN
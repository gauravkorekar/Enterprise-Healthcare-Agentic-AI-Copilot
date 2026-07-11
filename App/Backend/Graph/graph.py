from Backend.Graph.router import route_question

from Backend.Agents.retriever_agent import retriever_agent
from Backend.Agents.mcp_agent import mcp_agent
from Backend.Agents.reasoning_agent import reasoning_agent
from Backend.Agents.prompt import NO_CONTEXT_RESPONSE

from Backend.Logs.logger import logger

# Evaluation is optional.
# If evaluation fails, answer will still be returned.
try:
    from Backend.Evaluation.evaluation_agent import evaluation_agent
except Exception:
    evaluation_agent = None


def run_mediassist_graph(question: str) -> dict:
    """
    Main Agentic Graph Flow:

    User Question
        ↓
    Planner Agent
        ↓
    Router
        ↓
    MCP Agent / Retriever Agent
        ↓
    Reasoning Agent
        ↓
    Evaluation Agent
        ↓
    Final Answer
    """

    state = {
        "question": question,
        "route": None,
        "context": "",
        "chunks": [],
        "sources": [],
        "answer": "",
        "is_valid": True,
        "reason": "",
        "evaluation": None
    }

    logger.info(f"[GRAPH] New Question : {question}")

    # =========================
    # 1. Planner + Input Guardrail
    # =========================
    planner_result = route_question(question)  #This decides whether the question should go to: RAg/MCP/Blocked

    #get= Give me the value of this key. If the key doesn't exist, return the default value
    #saving planner agent outpot in state
    
    state["is_valid"] = planner_result.get("is_valid", False)
    state["route"] = planner_result.get("route")
    state["reason"] = planner_result.get("reason", "")

    logger.info(f"[GRAPH] Planner Route : {state['route']}")
    logger.info(f"[GRAPH] Planner Reason : {state['reason']}")

    if not state["is_valid"]:
        logger.info("[GRAPH] Question blocked by planner")

        return {
            "answer": planner_result.get("answer", "Question blocked."),
            "sources": [],
            "evaluation": None
        }

    # =========================
    # 2. MCP Route
    # =========================
    if state["route"] == "mcp":
        logger.info("[GRAPH] Executing MCP Agent")

        mcp_result = mcp_agent.run(question)

        answer = mcp_result.get("answer", "")
        sources = mcp_result.get("sources", ["PostgreSQL Database"])

        logger.info("[GRAPH] MCP completed")

        return {
            "answer": answer,
            "sources": sources,
            "evaluation": None
        }

    # =========================
    # 3. RAG Route
    # =========================
    if state["route"] == "rag":
        logger.info("[GRAPH] Executing Retriever Agent")

        retrieval_result = retriever_agent.run(question)

        if not retrieval_result.get("found", False):
            logger.info("[GRAPH] No context found")

            return {
                "answer": NO_CONTEXT_RESPONSE,
                "sources": [],
                "evaluation": None
            }

        state["context"] = retrieval_result.get("context", "")
        state["chunks"] = retrieval_result.get("chunks", [])
        state["sources"] = retrieval_result.get("sources", [])

        logger.info(f"[GRAPH] Sources : {state['sources']}")
        logger.info(f"[GRAPH] Chunks Retrieved : {len(state['chunks'])}")

        logger.info("[GRAPH] Executing Reasoning Agent")

        reasoning_result = reasoning_agent.run(
            question=question,
            context=state["context"]
        )

        state["answer"] = reasoning_result.get("answer", NO_CONTEXT_RESPONSE)
        # =========================
        # Token Usage Logging
        # =========================
        logger.info(
            f"[TOKENS][REASONING] "
            f"Prompt={reasoning_result.get('prompt_tokens', 0)} "
            f"Completion={reasoning_result.get('completion_tokens', 0)} "
            f"Total={reasoning_result.get('total_tokens', 0)}"
        )
        logger.info("[GRAPH] Reasoning completed")

        # =========================
        # 4. Evaluation Route
        # =========================
        if evaluation_agent is not None:
            try:
                logger.info("[GRAPH] Executing Evaluation Agent")

                state["evaluation"] = evaluation_agent.run(
                    question=question,
                    context=state["context"],
                    answer=state["answer"]
                )

                logger.info(f"[GRAPH] Evaluation : {state['evaluation']}")

            except Exception as e:
                logger.info(f"[GRAPH] Evaluation failed : {str(e)}")
                state["evaluation"] = None

        logger.info("[GRAPH] Workflow completed")

        return {
            "answer": state["answer"],
            "sources": state["sources"],
            "evaluation": state["evaluation"]
        }

    # =========================
    # 5. Fallback
    # =========================
    logger.info("[GRAPH] Unknown route fallback")

    return {
        "answer": NO_CONTEXT_RESPONSE,
        "sources": [],
        "evaluation": None
    }
from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.agents.cv_parser import parse_cv
from app.agents.skill_analyst import analyze_skills
from app.agents.market_researcher import research_market
from app.agents.report_generator import generate_report
from app.core.llm import strict_llm, creative_llm
from functools import partial

def create_workflow():
    workflow = StateGraph(GraphState)

    parse_cv_node = partial(parse_cv, llm=strict_llm)
    analyze_skills_node = partial(analyze_skills, llm=strict_llm)
    research_market_node = partial(research_market, llm=strict_llm)
    
    generate_report_node = partial(generate_report, llm=creative_llm)

    workflow.add_node("cv_parser", parse_cv_node)
    workflow.add_node("skill_analyst", analyze_skills_node)
    workflow.add_node("market_researcher", research_market_node)
    workflow.add_node("report_generator", generate_report_node)

    workflow.set_entry_point("cv_parser")
    workflow.add_edge("cv_parser", "skill_analyst")
    workflow.add_edge("skill_analyst", "market_researcher")
    workflow.add_edge("market_researcher", "report_generator")
    workflow.add_edge("report_generator", END)

    return workflow.compile()

graph_app = create_workflow()
from langchain_tavily import TavilySearch
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.agents import AgentExecutor, create_tool_calling_agent
from app.prompts.prompts import market_researcher_prompt

def research_market(state: dict, llm: BaseChatModel):
    job_role = state["job_role"]

    search_tool = TavilySearch(max_results=5)
    tools = [search_tool]
    
    agent = create_tool_calling_agent(llm, tools, market_researcher_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools,)
    
    input_query = f"What are the current in-demand skills for a {job_role}?"
    response = agent_executor.invoke({"input": input_query})
    
    return {"market_analysis": response["output"]}
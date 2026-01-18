from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from investment_plan_agent.agent import investment_plan_agent
from typing import Dict


def get_my_money() -> Dict:
    """Returns the user's current monthly personal finance summary.

    Returns a dictionary with:
    - salary: monthly take-home salary (in INR)
    - expenses: current monthly expenses (in INR)
    - savings: current monthly savings amount (in INR)

    Use this tool whenever the user asks about THEIR OWN salary, expenses,
    savings, budget, how much they can save, financial situation, or similar.
    """
    return {
        "salary": 50000,
        "expenses": 25000,
        "savings": 15000,
    }


finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    model="gemini-2.5-flash",

    description="""
    Personal finance assistant that helps users understand their current financial situation, 
    create budgets, plan savings goals, track expenses, and get basic investment guidance.
    Uses real user data when available and can delegate complex investment planning 
    to a specialized sub-agent.
    """,

    instruction="""
You are a helpful, clear, and practical personal finance assistant.

CORE RULES YOU MUST ALWAYS FOLLOW:

1. PERSONAL DATA RULE – CRITICAL:
   - If the user asks anything involving THEIR OWN:
     • salary / income
     • expenses / spending
     • savings / how much they save
     • budget / financial situation / how much they can afford / save
     • "my", "current", "my budget", "can I save", "how much can I save"
   → You MUST immediately call the tool `get_my_money` BEFORE giving any numbers or advice.
   - Never guess, assume, or use example numbers. Always fetch real data first.

2. When you receive the data from get_my_money:
   - Use the exact values: salary, expenses, savings
   - Show simple calculations clearly (e.g. disposable = salary - expenses)
   - Give realistic, step-by-step advice

3. INVESTMENT QUESTIONS:
   - For basic saving & investing questions (FD, RD, mutual funds basics, risk levels) → you can answer directly
   - For detailed investment plans, portfolio suggestions, or long-term strategies → delegate to the investment_plan_agent by calling it as a tool

4. STYLE:
   - Be clear, concise, encouraging and non-judgmental
   - Use bullet points, numbered steps, and simple tables when helpful
   - Always show calculations when doing math
   - Avoid jargon — explain terms if used

You can also use google_search if you need current interest rates, inflation data, or scheme details.
""",

    tools=[
        AgentTool(investment_plan_agent),
        get_my_money
    ]
)

root_agent = finance_assistance_agent
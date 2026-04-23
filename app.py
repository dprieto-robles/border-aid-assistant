import gradio as gr
import os
from langchain_groq import ChatGroq
from langchain.tools import tool

# Get API key from Hugging Face Secrets
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0.7
)


@tool
def organization_info(query: str) -> str:
    """Use this tool to answer questions about humanitarian aid organizations
    operating on the U.S.-Mexico border including Kino Border Initiative,
    No More Deaths, Humane Borders, and Border Angels."""

    org_data = """
    KINO BORDER INITIATIVE (KBI):
    - Founded: 2009
    - Locations: Nogales, Arizona (USA) and Nogales, Sonora (Mexico)
    - Focus: Humanitarian aid and advocacy for migrants and deportees
    - Programs: Comedor (dining hall providing meals), shelter support,
      legal aid clinic, medical outreach, and specialized volunteering
      for students in social work, medicine, and law
    - Website: kinoborderinitiative.org
    NO MORE DEATHS (No Mas Muertes):
    - Founded: 2004
    - Location: Tucson, Arizona
    - Focus: Water drops, search and rescue, humanitarian aid in the desert
    - Notable work: Maintains a comprehensive database of migrant deaths
      along the entire southern U.S. border from 2002 to present
    - Documents 20 to 40 percent more migrant deaths than CBP official counts
    - Website: nomoredeaths.org
    HUMANE BORDERS:
    - Founded: 1999
    - Location: Tucson, Arizona
    - Focus: Maintaining water stations in the Sonoran Desert
    - Notable work: Partners with Pima County Medical Examiner to maintain
      the Arizona OpenGIS Initiative for Deceased Migrants, updated monthly
    - Since 1990 nearly 4500 undocumented migrants have died within
      Pima and Maricopa Counties
    - Website: humaneborders.org
    BORDER ANGELS:
    - Founded: 1986
    - Location: San Diego, California
    - Focus: Water drops, migrant support, and outreach along California border
    - Website: borderangels.org
    """

    response = llm.invoke(
        f"Using this information about border humanitarian organizations, "
        f"please answer the following question: {query}\n\n"
        f"Organization data: {org_data}"
    )
    return response.content


@tool
def corridor_risk_info(query: str) -> str:
    """Use this tool to answer questions about border crossing corridors,
    their risk levels, locations, and the dangers migrants face when
    crossing through each corridor."""

    corridor_data = """
    TUCSON CORRIDOR:
    - State: Arizona
    - Risk Level: Extreme
    - Description: One of the deadliest crossing corridors in the United States.
      Covers vast stretches of the Sonoran Desert where temperatures can exceed
      110 degrees Fahrenheit in summer.
    - Primary cause of death: Exposure, skeletal remains
    SONORAN DESERT CORRIDOR:
    - State: Arizona
    - Risk Level: Extreme
    - Description: Overlaps with the Tucson corridor and extends into remote
      desert areas. Extremely high death rates due to heat exposure.
    - Primary cause of death: Exposure, undetermined
    EL CENTRO CORRIDOR:
    - State: California
    - Risk Level: High
    - Description: Covers Imperial Valley in Southern California.
    - Primary cause of death: Exposure, drowning
    RIO GRANDE VALLEY CORRIDOR:
    - State: Texas
    - Risk Level: High
    - Description: One of the busiest crossing points on the southern border.
      Migrants frequently attempt to cross the Rio Grande river.
    - Primary cause of death: Drowning
    EL PASO CORRIDOR:
    - State: Texas
    - Risk Level: Moderate
    - Description: Urban crossing point with heavier enforcement presence.
    - Primary cause of death: Drowning, exposure
    SAN MIGUEL CORRIDOR:
    - State: Arizona
    - Risk Level: Extreme
    - Description: Located within the Tohono Oodham Nation territory.
    - Primary cause of death: Exposure, blunt force injury
    """

    response = llm.invoke(
        f"Using this information about border crossing corridors, "
        f"please answer the following question: {query}\n\n"
        f"Corridor data: {corridor_data}"
    )
    return response.content


@tool
def migrant_death_data(query: str) -> str:
    """Use this tool to answer questions about migrant death statistics
    and data along the U.S.-Mexico border including causes of death,
    identification rates, yearly trends, and body conditions."""

    death_data = """
    DATA SOURCE:
    The following statistics come from the Humane Borders Arizona OpenGIS
    Initiative for Deceased Migrants and the No More Deaths Border Death
    Database covering Pima County, Arizona and the broader southern border.
    2025 STATISTICS (January through April 2025):
    - Total recorded deaths: 28
    - Deaths involving skeletal remains: 14 (50 percent of all cases)
    - Deaths with undetermined cause: 12 (43 percent of all cases)
    - Deaths from exposure: 1
    - Deaths from other disease: 1
    - Unknown age: 26 out of 28 cases (93 percent)
    OVERALL TRENDS:
    - 2024 was the deadliest year on record globally for migrant deaths
    - Since 1990 nearly 4500 migrants have died within Pima and Maricopa Counties
    - No More Deaths documents 20 to 40 percent more deaths than CBP counts
    - As of February 2026, 1653 decedents remain unidentified in Arizona
    CAUSES OF DEATH:
    - Skeletal remains, Exposure, Undetermined, Drowning, Blunt force injury
    BODY CONDITIONS:
    - Fully fleshed, Decomposed, Skeletal remains
    """

    response = llm.invoke(
        f"Using this data about migrant deaths along the U.S.-Mexico border, "
        f"please answer the following question: {query}\n\n"
        f"Death statistics and data: {death_data}"
    )
    return response.content


tools = [organization_info, corridor_risk_info, migrant_death_data]
llm_with_tools = llm.bind_tools(tools)

system_prompt = """You are the Border Aid Assistant, a knowledgeable and
compassionate chatbot dedicated to raising awareness about the humanitarian
crisis at the U.S.-Mexico border. You have access to three tools:
1. organization_info — for humanitarian organizations
2. corridor_risk_info — for border crossing corridors
3. migrant_death_data — for migrant death statistics
Always be respectful and compassionate. These are real human lives."""


def run_agent(user_input):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = llm_with_tools.invoke(messages)

    tool_map = {
        "organization_info": organization_info,
        "corridor_risk_info": corridor_risk_info,
        "migrant_death_data": migrant_death_data
    }

    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        if tool_name in tool_map:
            return tool_map[tool_name].invoke(tool_args)

    return response.content


def chat_interface(message, history):
    return run_agent(message)


demo = gr.ChatInterface(
    fn=chat_interface,
    title="🌎 Border Aid Assistant",
    description=(
        "A compassionate chatbot dedicated to raising awareness about the "
        "humanitarian crisis at the U.S.-Mexico border. Ask me about aid "
        "organizations like the Kino Border Initiative, border crossing "
        "corridors and their risks, or migrant death statistics and trends."
    ),
    examples=[
        "What does the Kino Border Initiative do?",
        "How dangerous is the Tucson corridor?",
        "How many migrants died in 2025?",
        "Tell me about No More Deaths",
        "What are the main causes of migrant deaths?"
    ]
)

demo.launch()

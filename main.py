import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import SerperDevTool, ScrapeWebsiteTool
from crewai_tools import WebsiteSearchTool

# Initialize search tools (modern alternatives to DuckDuckGo)
# Option 1: Using SerperDev (requires SERPER_API_KEY)
# serper_tool = SerperDevTool()

# Option 2: Using CrewAI's WebsiteSearchTool (no API key needed for basic web search)
search_tool = WebsiteSearchTool()

# Option 3: For scraping websites
scrape_tool = ScrapeWebsiteTool()

# Note: You can also use these environment variables for API keys:
# os.environ["SERPER_API_KEY"] = "your_serper_api_key_here"
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

# Define your agents with modern configuration
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory="""You are an expert at a technology research group, 
    skilled in identifying trends and analyzing complex data.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool],
    # Modern CrewAI requires explicit LLM configuration
    # llm=ChatOpenAI(model_name="gpt-4", temperature=0.7),  # Uncomment and configure as needed
    max_iter=5,  # Limit iterations to prevent infinite loops
    memory=True  # Enable agent memory for better context retention
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a content strategist known for 
    making complex tech topics interesting and easy to understand.""",
    verbose=True,
    allow_delegation=True,
    # llm=ChatOpenAI(model_name="gpt-4", temperature=0.7),  # Uncomment and configure as needed
    max_iter=3,
    memory=True
)

# Create tasks with modern configuration (expected_output is now required)
task1 = Task(
    description="""Analyze the latest AI advancements from 2024 through 2025. 
    Find major trends, breakthrough technologies, and their real-world impacts. 
    Focus on the most recent developments and provide a comprehensive report with specific examples and data.""",
    agent=researcher,
    expected_output="""A comprehensive report containing:
    - Top 5 AI trends from 2024-2025
    - Latest breakthrough technologies with real examples
    - Market impact analysis and industry adoption
    - Current state of AI in October 2025
    - Future predictions for 2026 and beyond
    Format as structured markdown with clear sections and recent data."""
)

task2 = Task(
    description="""Create an engaging blog post about the latest AI advancements from 2024-2025 using your research insights. 
    Make it current, interesting, and suited for tech enthusiasts and industry professionals. 
    It should be comprehensive with engaging headlines and reflect the cutting-edge state of AI as of October 2025.""",
    agent=writer,
    expected_output="""A well-structured blog post containing:
    - Compelling title reflecting 2024-2025 AI developments
    - Engaging introduction highlighting recent breakthroughs
    - 4+ detailed paragraphs covering latest AI advancements
    - Real-world examples and current industry applications
    - Analysis of AI's impact through October 2025
    - Forward-looking conclusion with 2026+ predictions
    - SEO-friendly formatting with compelling subheadings"""
)

# Instantiate your crew with modern sequential process
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,  # Modern way to specify process
    verbose=True,  # Updated verbose syntax (boolean instead of integer)
    # Optional: Add memory and other modern features
    memory=True,
    embedder={
        "provider": "openai",  # or "cohere", "huggingface", etc.
        "config": {
            "model": "text-embedding-3-small"
        }
    }
)

# Enhanced execution with error handling
if __name__ == "__main__":
    try:
        print("🚀 Starting CrewAI execution...")
        result = crew.kickoff()
        
        print("\n" + "="*50)
        print("📋 FINAL RESULT")
        print("="*50)
        print(result)
        
        # Optional: Save result to file
        with open("ai_advancements_report.md", "w") as f:
            f.write(str(result))
        print("\n✅ Report saved to 'ai_advancements_report.md'")
        
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        print("💡 Make sure you have:")
        print("   - Set up your API keys (OPENAI_API_KEY, SERPER_API_KEY)")
        print("   - Installed required dependencies: pip install crewai crewai-tools")
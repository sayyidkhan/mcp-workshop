#!/usr/bin/env python3
"""
Proper MCP Implementation: AI discovers tools dynamically
Tools defined once on server, discovered by client.
In production systems like Claude Desktop, the Client and Model are separate. 
Claude Desktop is the client, Anthropic's servers run the model, and MCP servers provide tools.
In our workshop version, we've combined the Client and Model into one script for simplicity. In production MCP systems, these are often separate services.
"""

import os
import requests
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local", override=True)
load_dotenv(dotenv_path=".env", override=False)

base_url = os.getenv("BASE_API_URL")  # http://localhost:8000
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def discover_tools():
    """
    PROPER MCP: Dynamically discover what tools are available
    Get tools from the server.
    """
    try:
        response = requests.get(f"{base_url}/_mcp/tools")
        response.raise_for_status()
        tools = response.json()
        print(f"🔍 Discovered {len(tools)} tools from server:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        return tools
    except requests.RequestException as e:
        print(f"❌ Failed to discover tools: {e}")
        return []

def build_dynamic_prompt(question: str, available_tools: list) -> str:
    """
    Build prompt using DISCOVERED tools, not hardcoded ones!
    """
    # Convert discovered tools to prompt format
    tool_descriptions = []
    tool_definitions = {}
    
    for i, tool in enumerate(available_tools, 1):
        tool_descriptions.append(f"{i}. {tool['name']}: {tool['description']}")
        tool_definitions[tool['name']] = tool
    
    tools_list = "\n".join(tool_descriptions)
    tools_json = json.dumps(tool_definitions, indent=4)
    
    return f"""
You are a function router. Based on the user's query, decide whether to use a tool.

Available tools:
{tools_list}

Tool Definitions:
{tools_json}

Respond in valid JSON only, like:
{{
    "tool_use": true,
    "tool_name": "add",
    "parameters": {{
        "a": 4,
        "b": 5
    }}
}}

Query: "{question}"
"""

def call_tool(tool_name: str, parameters: dict):
    """Same as before"""
    url = f"{base_url}/{tool_name}"
    try:
        response = requests.post(url, json=parameters)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def chat_with_model(question: str):
    """
    PROPER MCP FLOW:
    1. Discover tools from server (not hardcoded!)
    2. Build prompt with discovered tools
    3. Let AI decide which tool to use
    4. Execute the tool
    """
    
    # Step 1: Discover available tools
    available_tools = discover_tools()
    if not available_tools:
        print("No tools available!")
        return
    
    # Step 2: Build prompt with discovered tools
    dynamic_prompt = build_dynamic_prompt(question, available_tools)
    
    # Step 3: Let AI decide
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": dynamic_prompt}],
        model="llama3-8b-8192",
    )
    
    model_reply = chat_completion.choices[0].message.content
    print("🤖 AI Decision:", model_reply)
    
    # Step 4: Execute chosen tool
    try:
        parsed = json.loads(model_reply)
        if parsed.get("tool_use") and parsed.get("tool_name") and parsed.get("parameters"):
            result = call_tool(parsed["tool_name"], parsed["parameters"])
            print("⚙️ Tool Result:", result)
            return result
        else:
            print("No tool needed.")
    except json.JSONDecodeError:
        print("Failed to parse AI response.")

if __name__ == "__main__":
    print("🚀 Proper MCP Client - Dynamic Tool Discovery")
    print("=" * 50)
    
    while True:
        user_input = input("\nEnter your question: ")
        chat_with_model(user_input)
        
        again = input("Ask another question? (y/n): ").strip().lower()
        if again != "y":
            print("👋 Goodbye!")
            break
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
    🎯 CORE MCP CONCEPT: Dynamically discover what tools are available
    This is what makes MCP powerful - clients don't hardcode tools!
    """
    
    # STEP 1: Make HTTP request to the server's tools endpoint
    # TODO: Use requests.get() to fetch tools from f"{base_url}/_mcp/tools"
    # HINT: response = requests.get(...)
    
    try:
        # TODO: Make the GET request here
        response = requests.get(f"{base_url}/_mcp/tools")
        
        # STEP 2: Check if request was successful
        # TODO: Call response.raise_for_status() to check for HTTP errors
        response.raise_for_status()
        
        # STEP 3: Parse the JSON response to get tools list
        # TODO: Convert response to JSON using response.json()
        # TODO: Store in a variable called 'tools'
        tools = response.json()
        
        # STEP 4: Show what we discovered (helpful for learning!)
        # TODO: Print how many tools were discovered
        # TODO: Loop through tools and print each tool's name and description
        # HINT: for tool in tools: print(f"  - {tool['name']}: {tool['description']}")
        print(f"Discovered {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
        # STEP 5: Return the discovered tools
        # TODO: Return the tools list
        return tools
        
    except requests.RequestException as e:
        print(f"❌ Failed to discover tools: {e}")
        return []

def build_dynamic_prompt(question: str, available_tools: list) -> str:
    """
    🎯 CORE MCP CONCEPT: Build AI prompts using DISCOVERED tools, not hardcoded ones!
    This shows how MCP enables truly dynamic AI capabilities.
    """
    
    # STEP 1: Initialize data structures for prompt building
    # TODO: Create empty list called 'tool_descriptions' 
    # TODO: Create empty dict called 'tool_definitions'
    
    
    # STEP 2: 🚀 THE MAGIC MOMENT - Convert discovered tools into prompt format
    # This is where MCP shines - we're using tools we just discovered!
    
    # TODO: Loop through available_tools with enumerate(available_tools, 1)
    # HINT: for i, tool in enumerate(available_tools, 1):
    
        # STEP 3: Build human-readable tool list for the prompt
        # TODO: Append to tool_descriptions: f"{i}. {tool['name']}: {tool['description']}"
        
        # STEP 4: Store full tool definition for detailed prompt
        # TODO: Add tool to tool_definitions dict: tool_definitions[tool['name']] = tool
    
    # STEP 5: Format the data for prompt inclusion
    # TODO: Join tool_descriptions with newlines: tools_list = "\n".join(tool_descriptions)
    # TODO: Convert tool_definitions to JSON: tools_json = json.dumps(tool_definitions, indent=4)
    
    # STEP 6: 🎯 THE DYNAMIC PROMPT - Built from discovered tools!
    # This prompt changes based on what tools the server offers
    
    # TODO: Return the formatted prompt string (see below for template)
    # Use f-string with: question, tools_list, and tools_json
    
    prompt_template = """
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
    
    # TODO: Return the formatted prompt using the template above
    # HINT: return prompt_template.format(tools_list=tools_list, tools_json=tools_json, question=question)


def call_tool(tool_name: str, parameters: dict):
    """Execute a tool on the server"""
    url = f"{base_url}/{tool_name}"
    try:
        response = requests.post(url, json=parameters)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def chat_with_model(question: str):
    """
    🎯 THE COMPLETE MCP FLOW:
    1. Discover tools from server (not hardcoded!)
    2. Build prompt with discovered tools
    3. Let AI decide which tool to use
    4. Execute the tool
    
    This demonstrates the full MCP cycle in action!
    """
    
    # Step 1: 🔍 DISCOVER - Don't hardcode, discover!
    print("🔍 Step 1: Discovering available tools...")
    available_tools = discover_tools()
    if not available_tools:
        print("No tools available!")
        return
    
    # Step 2: 🧠 BUILD - Create dynamic prompt with discovered tools
    print("🧠 Step 2: Building dynamic prompt...")
    dynamic_prompt = build_dynamic_prompt(question, available_tools)
    
    # Step 3: 🤖 DECIDE - Let AI choose which tool to use
    print("🤖 Step 3: AI choosing tool...")
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": dynamic_prompt}],
        model="llama3-8b-8192",
    )
    
    model_reply = chat_completion.choices[0].message.content
    print("🤖 AI Decision:", model_reply)
    
    # Step 4: ⚙️ EXECUTE - Run the chosen tool
    print("⚙️ Step 4: Executing tool...")
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
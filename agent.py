import os
from typing import List

from dotenv import load_dotenv
import google.generativeai as genai
from langchain.agents import AgentExecutor
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import list_files, read_file, write_file, rename_file


def load_api_key() -> None:
    """load the google api key"""
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    genai.configure(api_key=GOOGLE_API_KEY)


def create_llm() -> ChatGoogleGenerativeAI:
    """create the llm for agent"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0,
        convert_system_message_to_human=True,
        client_options=None,
        transport=None,
        client=None,
    )
    return llm


def create_tools() -> List[StructuredTool]:
    """define the available tools for the agent"""
    tools = [
        StructuredTool.from_function(
            func=list_files,
            name="list_files",
            description="""List files in a directory that satisfy the pattern.
            Input should be a directory path and a matching pattern.""",
        ),
        StructuredTool.from_function(
            func=read_file,
            name="read_file",
            description="Read content of a file. Input should be a file path.",
        ),
        StructuredTool.from_function(
            func=write_file,
            name="write_file",
            description="Write content to a file. Requires path and content arguments.",
        ),
        StructuredTool.from_function(
            func=rename_file,
            name="rename_file",
            description="Rename a file. Requires old_path and new_path arguments.",
        ),
    ]
    return tools


def create_agent_executor() -> AgentExecutor:
    """create the agent executor"""
    load_api_key()
    tools = create_tools()
    llm = create_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a file system operation agent and you can:
            1. List files in directories that satisfy a pattern
            2. Read file contents
            3. Write to files
            4. Rename files
            Aftere receiving the user's requirement, always think step by step and
            use the available tools to complete the tasks.
            When dealing with files that contain spaces in their names, make sure to handle them properly.
            If you encounter any errors, explain them clearly."""
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = StructuredChatAgent.from_llm_and_tools(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent_executor

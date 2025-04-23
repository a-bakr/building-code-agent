from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from core.text_extraction import text_extraction
from core.retriever import building_code_retriever

model = "google/gemini-2.5-pro-exp-03-25:free"
model = "gpt-4o-mini"
llm = ChatOpenAI(model=model)
# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

tools = [text_extraction, building_code_retriever]
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


class State(TypedDict):
    input_file: Optional[str]
    extracted_text: Optional[str]
    building_code: Optional[str]
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: State):
    
    image = state['input_file']
    
    massage = '\n'.join([
        "You are a helpful building code assistant.",
        "You can extract text from floorplan images.",
        "You can check if this text comply with the building code.",
        "you sould create short report."
        "You have access to the following tools:",
        "- text_extraction: Extract text from images",
        "- building_code_retriever: Get building code regulations for specific room, you can call me mulitple time to get all rooms data",
        "You should answer in the user language"
        f"Currently the loaded image is : {image}"
    ])
    sys_msg = SystemMessage(massage)
    
    messages = [sys_msg] + state['messages']
    res = llm_with_tools.invoke(messages)
    
    return {'messages': [res], "input_file": image}

def create_graph():
    
    builder = StateGraph(State)
    
    # Define nodes: these do the work
    builder.add_node('assistant', assistant)    
    builder.add_node('tools', ToolNode(tools))
    
    # Define edges: these determine how the control flow moves
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge('tools', "assistant")
    
    return builder.compile()

def run_agent(image_path: str, question: str):
    agent = create_graph()

    prompt = "\n".join([
        "Answer the user question without extra information.",
        f"User question: {question}",
        "You can extract text from images and retrieve building code information for any room as needed to answer the question.",
    ])
        # "The final answer should be in the user language"
    
    messages = [HumanMessage(prompt)]
    messages = agent.invoke({
        "input_file": image_path,
        "messages": prompt
    })
    
    # Process the result
    tool_outputs = {
        "text_extraction": "",
        "building_code_retriever": ""
    }
    for m in messages['messages']:
        if hasattr(m, 'name') and m.name in ['text_extraction', 'building_code_retriever']:
            tool_outputs[m.name] += m.content
    
    result = messages['messages'][-1].content
    res = {
        "tool_outputs": tool_outputs,
        "result": result
    }
    
    return res
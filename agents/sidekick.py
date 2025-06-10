import datetime
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, Dict, List, Any, Optional
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
import uuid


load_dotenv(override=True)

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool

class EvaluatorOutput(BaseModel):
    feedback: str = Field(description="Feedback on the assistant's response")
    success_criteria_met: bool = Field("Whether the success criteria have been met")
    user_input_needed: bool = Field("True if more input is needed from the user, or clarifications or the assistant is stuck ")
    
class Sidekick:
    def __init__(self):
        self.worker_llm_with_tools = None
        self.evaluator_llm_with_tool = None
        self.tools = None
        self.llm_with_tools = None
        self.graph = None
        self.sidekick_id = str(uuid.uuidv4())
        self.memory = MemorySaver()
        self.browser = None
        self.playwright = None
    
    def worker(self, state: State) -> Dict[str,Any]:
        system_message = f"""You are a helpful assistant that can use tools to complete tasks.
            You keep working on a task until either you have a question or clarification for the user, or the success criteria is met.
            You have many tools to help you, including tools to browse the internet, navigating and retrieving web pages.
            You have a tool to run python code, but note that you would need to include a print() statement if you wanted to receive output.
            The current date and time is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

            This is the success criteria:
            {state['success_criteria']}
            You should reply either with a question for the user about this assignment, or with your final response.
            If you have a question for the user, you need to reply by clearly stating your question. An example might be:

            Question: please clarify whether you want a summary or a detailed answer

            If you've finished, reply with the final answer, and don't ask a question; simply reply with the answer.
            """
        if state.get("feedback_on_work"):
            system_message += f"""
                Previously you thought you completed the assignment, but your reply was rejected because the success criteria was not met.
                Here is the feedback on why this was rejected:
                {state['feedback_on_work']}
                With this feedback, please continue the assignment, ensuring that you meet the success criteria or have a question for the user."""
        
        # Add in the system message
        found_system_message = False
        messages = state["messages"]
        for message in messages:
            if(isinstance(message, SystemMessage)):
               message.content = system_message
               found_system_message = True 
        if not found_system_message:
            messages = [SystemMessage(content=system_message)] + messages
        
        # Invoke the LLM with tools
        response = self.worker_llm_with_tools.invoke(messages)
    
    def format_conversation(self, messages: List[Any]) -> str:
        conversation = "Conversation history:\n\n"
        for message in messages:
            if isinstance(message, HumanMessage):
                conversation += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                text = message.content or "[Tools use]"
                conversation += f"Assistant: {text}\n"
        return conversation
              
        
        
        
        
        
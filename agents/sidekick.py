from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, List, Any, Optional
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
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
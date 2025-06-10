from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, List, Any, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

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
    
    
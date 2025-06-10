from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, List, Any, Optional
from langgraph.graph.message import add_messages


load_dotenv(override=True)

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool
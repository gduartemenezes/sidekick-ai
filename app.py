import gradio as gr
from agents.sidekick import Sidekick


async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick
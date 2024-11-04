import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import create_agent_executor

app = FastAPI()

agent_executor = create_agent_executor()


class AgentRequest(BaseModel):
    msg: str


class AgentResponse(BaseModel):
    msg: str


@app.post("/agent", response_model=AgentResponse)
async def process_agent_request(request: AgentRequest) -> AgentResponse:
    """Process agent requests asynchronously"""
    try:
        # Run agent in a thread pool to avoid blocking
        response = await asyncio.get_event_loop().run_in_executor(
            None, agent_executor.invoke, {"input": request.msg}
        )
        return AgentResponse(msg=response["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

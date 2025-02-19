
from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from autogen_agentchat.base._task import TaskResult

@dataclass
class LocalModelCapabilities:
    json_output: Optional[bool] = False
    vision: Optional[bool] = False
    function_calling: Optional[bool] = False

@dataclass
class ModelConfig:
    model: str
    model_type: Literal["OpenAIChatCompletionClient", "OllamaProxyClient"]
    api_key: Optional[str] = "NotRequiredSinceWeAreLocal"
    base_url: Optional[str] = "http://0.0.0.0:4000"
    model_capabilities: Optional[LocalModelCapabilities] = None

@dataclass
class ToolConfig:
    name: str
    description: str
    content: str

@dataclass
class AgentConfig:
    name: str
    agent_type: Literal["AssistantAgent", "CodingAssistantAgent"]
    system_message: Optional[str] = None
    model_client: Optional[ModelConfig] = None    
    tools: Optional[List[ToolConfig]] = None
    description: Optional[str] = None

@dataclass
class TerminationConfig:
    termination_type: Literal["MaxMessageTermination",
                              "StopMessageTermination", "TextMentionTermination"]
    max_messages: Optional[int] = None
    text: Optional[str] = None

@dataclass
class TeamConfig:
    name: str
    participants: List[AgentConfig]
    team_type: Literal["RoundRobinGroupChat", "SelectorGroupChat"]
    model_client: Optional[ModelConfig] = None
    termination_condition: Optional[TerminationConfig] = None

class TeamResult(BaseModel):
    task_result: TaskResult
    usage: str
    duration: float

@dataclass
class AgentFlowSpec:
    name: Optional[str] = None
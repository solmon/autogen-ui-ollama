
from typing import Any, List, Literal, Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from autogen_agentchat.base._task import TaskResult


@dataclass
class ModelConfig:
    model: str
    model_type: Literal["OpenAIChatCompletionClient","OllamaProxyClient"]


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
class LocalModelConfig:
    model: Optional[str] = "NotRequired"
    ap_key: Optional[str] = "NotRequired"
    base_url: Optional[str] = "http://0.0.0.0:4000"
    price: Optional[List[int]] = [0,0]

@dataclass
class LocalConfig:
    config_list: List[LocalModelConfig]
    cache_seed: Optional[str] = None

from .datamodel import AgentConfig, ModelConfig, ToolConfig, TerminationConfig, TeamConfig, LocalConfig, LocalModelConfig
# from autogen_agentchat.agents import AssistantAgent, CodingAssistantAgent, ConversableAgent
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
# from autogen import UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import MaxMessageTermination, StopMessageTermination, TextMentionTermination
# from autogen_core.components.tools import FunctionTool
from autogen_ext.tools.code_execution import PythonCodeExecutionTool


AgentTypes = AssistantAgent | CodeExecutorAgent
TeamTypes = RoundRobinGroupChat | SelectorGroupChat
ModelTypes = OpenAIChatCompletionClient | None | LocalConfig
TerminationTypes = MaxMessageTermination | StopMessageTermination | TextMentionTermination


class Provider():
    def __init__(self):
        pass

    def load_model(self, model_config: ModelConfig | dict) -> ModelTypes:
        if isinstance(model_config, dict):
            try:
                model_config = ModelConfig(**model_config)
            except:
                raise ValueError("Invalid model config")
        model = None
        if model_config.model_type == "OpenAIChatCompletionClient":
            model = OpenAIChatCompletionClient(model=model_config.model)
        elif model_config.model_type == "OllamaProxyClient":
            model = OpenAIChatCompletionClient(model=model_config.model)
        return model

    def load_local_model(self) -> ModelTypes:
        model_config = None
        model_config = LocalConfig()
        return model_config

    def _func_from_string(self, content: str) -> callable:
        """
        Convert a string containing function code into a callable function object.

        Args:
            content (str): String containing the function code, with proper indentation

        Returns:
            Callable: The compiled function object
        """
        # Create a namespace for the function
        namespace = {}

        # Ensure content is properly dedented if it contains indentation
        lines = content.split('\n')
        if len(lines) > 1:
            # Find the minimum indentation (excluding empty lines)
            indents = [len(line) - len(line.lstrip())
                       for line in lines if line.strip()]
            min_indent = min(indents) if indents else 0
            # Remove the minimum indentation from each line
            lines = [line[min_indent:]
                     if line.strip() else line for line in lines]
            content = '\n'.join(lines)

        try:
            # Execute the function definition in the namespace
            exec(content, namespace)

            # Find and return the function object
            # Get the first callable object from the namespace
            for item in namespace.values():
                if callable(item) and not isinstance(item, type):
                    return item

            raise ValueError("No function found in the provided code")
        except Exception as e:
            raise ValueError(
                f"Failed to create function from string: {str(e)}")

    def load_tool(self, tool_config: ToolConfig | dict) -> PythonCodeExecutionTool:
        if isinstance(tool_config, dict):
            try:
                tool_config = ToolConfig(**tool_config)
            except:
                raise ValueError("Invalid tool config")
        tool = PythonCodeExecutionTool(name=tool_config.name, description=tool_config.description,
                            func=self._func_from_string(tool_config.content))
        return tool

    def load_agent(self, agent_config: AgentConfig | dict) -> AgentTypes:
        if isinstance(agent_config, dict):
            try:
                agent_config = AgentConfig(**agent_config)
            except:
                raise ValueError("Invalid agent config")
        agent = None
        if agent_config.agent_type == "AssistantAgent":
            model_client = self.load_model(agent_config.model_client)
            system_message = agent_config.system_message if agent_config.system_message else "You are a helpful AI assistant. Solve tasks using your tools. Reply with 'TERMINATE' when the task has been completed."
            tools = [self.load_tool(tool) for tool in agent_config.tools]
            agent = AssistantAgent(
                name=agent_config.name, model_client=model_client, tools=tools, system_message=system_message)

        return agent

    def load_termination(self, termination_config: TerminationConfig | dict) -> TerminationTypes:
        if isinstance(termination_config, dict):
            try:
                termination_config = TerminationConfig(**termination_config)
            except:
                raise ValueError("Invalid termination config")
        termination = None
        if termination_config.termination_type == "MaxMessageTermination":
            termination = MaxMessageTermination(
                max_messages=termination_config.max_messages)
        elif termination_config.termination_type == "StopMessageTermination":
            termination = StopMessageTermination()
        elif termination_config.termination_type == "TextMentionTermination":
            termination = TextMentionTermination(text=termination_config.text)
        return termination

    def load_team(self, team_config: TeamConfig | dict) -> TeamTypes:
        if isinstance(team_config, dict):
            try:
                team_config = TeamConfig(**team_config)
            except:
                raise ValueError("Invalid team config")
        team = None
        agents = []
        termination = self.load_termination(team_config.termination_condition)
        # tbd on termination condition
        for agent_config in team_config.participants:
            agent = self.load_agent(agent_config)
            agents.append(agent)
        if team_config.team_type == "RoundRobinGroupChat":
            team = RoundRobinGroupChat(
                agents, termination_condition=termination)
        elif team_config.team_type == "SelectorGroupChat":
            team = SelectorGroupChat(agents, termination_condition=termination)

        return team
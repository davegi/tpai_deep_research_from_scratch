from typing import Protocol, Any, Dict, List, Optional
from pydantic import BaseModel, Field

# --- Config Protocol ---
class LLMConfigProtocol(Protocol):
    api_key: str
    model: str
    temperature: float
    top_p: float
    top_k: Optional[int]
    max_tokens: int
    timeout: int
    stop_sequences: Optional[List[str]]
    stream: bool
    system_prompt: Optional[str]
    user: Optional[str]
    logprobs: Optional[int]
    metadata: Optional[Dict[str, Any]]
    extra: Optional[Dict[str, Any]]

# --- Base Config ---
class LLMConfig(BaseModel):
    api_key: str = Field(default="")
    model: str = Field(default="")
    temperature: float = Field(default=0.7, ge=0, le=2)
    top_p: float = Field(default=1.0, ge=0, le=1)
    top_k: Optional[int] = Field(default=None, ge=0)
    max_tokens: int = Field(default=256, ge=1)
    timeout: int = Field(default=30, ge=1)
    stop_sequences: Optional[List[str]] = Field(default=None)
    stream: bool = Field(default=False)
    system_prompt: Optional[str] = Field(default=None)
    user: Optional[str] = Field(default=None)
    logprobs: Optional[int] = Field(default=None, ge=0)
    metadata: Optional[Dict[str, Any]] = Field(default=None)
    extra: Optional[Dict[str, Any]] = Field(default=None)

class OpenAIConfig(LLMConfig):
    organization: Optional[str] = Field(default=None)

class AnthropicConfig(LLMConfig):
    anthropic_version: Optional[str] = Field(default=None)

# Stubs for other providers
class GeminiConfig(LLMConfig):
    pass
class CohereConfig(LLMConfig):
    pass
class MistralConfig(LLMConfig):
    pass
class CopilotConfig(LLMConfig):
    token: str = Field(default="")
class HuggingFaceConfig(LLMConfig):
    pass
class AzureOpenAIConfig(LLMConfig):
    deployment_id: Optional[str] = Field(default=None)
    api_version: Optional[str] = Field(default=None)
    resource_name: Optional[str] = Field(default=None)

# --- Client Protocol ---
class LLMClient(Protocol):
    async def generate(self, prompt: str, **kwargs) -> str:
        ...

# --- Client Implementations ---
class OpenAIClient:
    def __init__(self, config: OpenAIConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        # TODO: Implement OpenAI API call
        return "openai response"

class AnthropicClient:
    def __init__(self, config: AnthropicConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        # TODO: Implement Anthropic API call
        return "anthropic response"

class MockLLM:
    def __init__(self, config: LLMConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        return f"mock response for: {prompt}"

# Stubs for other providers
class GeminiClient:
    def __init__(self, config: GeminiConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("GeminiClient not implemented yet.")

class CohereClient:
    def __init__(self, config: CohereConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("CohereClient not implemented yet.")

class MistralClient:
    def __init__(self, config: MistralConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("MistralClient not implemented yet.")

class CopilotClient:
    def __init__(self, config: CopilotConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("CopilotClient not implemented yet.")

class HuggingFaceClient:
    def __init__(self, config: HuggingFaceConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("HuggingFaceClient not implemented yet.")

class AzureOpenAIClient:
    def __init__(self, config: AzureOpenAIConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("AzureOpenAIClient not implemented yet.")

# --- Factory ---
def llm_factory(provider: str, config: LLMConfig) -> LLMClient:
    dump = config.model_dump()
    if provider == "openai":
        return OpenAIClient(OpenAIConfig(**dump))
    elif provider == "anthropic":
        return AnthropicClient(AnthropicConfig(**dump))
    elif provider == "mock":
        return MockLLM(config)
    elif provider == "gemini":
        return GeminiClient(GeminiConfig(**dump))
    elif provider == "cohere":
        return CohereClient(CohereConfig(**dump))
    elif provider == "mistral":
        return MistralClient(MistralConfig(**dump))
    elif provider == "copilot":
        return CopilotClient(CopilotConfig(**dump))
    elif provider == "huggingface":
        return HuggingFaceClient(HuggingFaceConfig(**dump))
    elif provider == "azure-openai":
        return AzureOpenAIClient(AzureOpenAIConfig(**dump))
    else:
        raise ValueError(f"Unknown provider: {provider}")

from typing import Protocol, Any, Dict, List, Optional, Type
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

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        """Model-in / model-out generation.

        Default contract: take a Pydantic input model and produce a Pydantic output
        model instance. Implementations should provide this for deterministic
        model-driven tools; fallback to string-based `generate` where needed.
        """
        ...

# --- Client Implementations ---
class OpenAIClient:
    def __init__(self, config: OpenAIConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        # TODO: Implement OpenAI API call
        return "openai response"

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class AnthropicClient:
    def __init__(self, config: AnthropicConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        # TODO: Implement Anthropic API call
        return "anthropic response"

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class MockLLM:
    def __init__(self, config: LLMConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        return f"mock response for: {prompt}"

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        # Simple deterministic mapping for testing: when asked to produce an
        # EvalResult from a ResearchTask-like input, create a constructed
        # EvalResult with feedback containing a mock response.
        try:
            # Best-effort extraction if input_model has `id` and `query` fields
            task_id = getattr(input_model, "id", None)
            prompt = getattr(input_model, "query", str(input_model))
        except Exception:
            task_id = None
            prompt = str(input_model)

        feedback = f"mock response for: {prompt}"

        # If the desired output model is EvalResult, construct it directly to
        # preserve types used across the codebase.
        from research_agent_framework.models import EvalResult

        if output_model is EvalResult or getattr(output_model, "__name__", "") == "EvalResult":
            return EvalResult(task_id=task_id or "unknown", success=True, score=min(1.0, len(feedback) / 100.0), feedback=feedback, details={})

        # Generic fallback: try to parse a dict into the requested Pydantic model
        data = {"feedback": feedback}
        if task_id is not None:
            data.setdefault("task_id", task_id)
        return output_model.model_validate(data)

# Stubs for other providers
class GeminiClient:
    def __init__(self, config: GeminiConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("GeminiClient not implemented yet.")

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class CohereClient:
    def __init__(self, config: CohereConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("CohereClient not implemented yet.")

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class MistralClient:
    def __init__(self, config: MistralConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("MistralClient not implemented yet.")

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class CopilotClient:
    def __init__(self, config: CopilotConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("CopilotClient not implemented yet.")

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class HuggingFaceClient:
    def __init__(self, config: HuggingFaceConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("HuggingFaceClient not implemented yet.")

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

class AzureOpenAIClient:
    def __init__(self, config: AzureOpenAIConfig):
        self.config = config
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("AzureOpenAIClient not implemented yet.")

    async def generate_model(self, input_model: BaseModel, output_model: Type[BaseModel], **kwargs) -> BaseModel:
        prompt = getattr(input_model, "query", str(input_model))
        text = await self.generate(prompt, **kwargs)
        data = {"feedback": text, "task_id": getattr(input_model, "id", None)}
        return output_model.model_validate(data)

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

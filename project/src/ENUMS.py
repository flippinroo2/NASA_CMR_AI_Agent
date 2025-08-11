from enum import Enum, StrEnum


class CMR_ENDPOINTS(StrEnum):
    AUTOCOMPLETE = "autocomplete"
    COLLECTIONS = "collections"
    GRANULES = "granules"

    @staticmethod
    def get_item_from_index(index) -> str | None:
        try:
            return list(CMR_ENDPOINTS)[index - 1]
        except IndexError as e:
            print(f"CMR_ENDPOINTS.get_item_from_index() - IndexError: {e}")

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class CMR_QUERY_INTENTION(Enum):
    EXPLORATORY = 1
    ANALYTICAL = 2
    SPECIFIC_DATA = 3

    def __str__(self):
        return f"CMR_QUERY_INTENTION_ENUM.{self.name}"

    def __repr__(self):
        return f"CMR_QUERY_INTENTION_ENUM.{self.name}"


class LLM_PROVIDER(Enum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    BEDROCK_CONVERSE = "bedrock_converse"
    DEEPSEEK = "deepseek"
    GOOGLE = "google"
    GROQ = "groq"
    HUGGING_FACE = "huggingface"
    LM_STUDIO = "lmstudio"
    MISTRAL = "mistralai"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"
    OPEN_AI = "openai"
    PERPLEXITY = "perplexity"
    XAI = "xai"

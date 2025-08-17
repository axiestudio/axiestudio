"""Axie Studio Components module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from axiestudio.components._importing import import_mod

if TYPE_CHECKING:
    from axiestudio.components import (
        Notion,
        agentql,
        agents,
        aiml,
        amazon,
        anthropic,
        apify,
        arxiv,
        assemblyai,
        azure,
        baidu,
        bing,
        cleanlab,
        cloudflare,
        cohere,
        composio,
        confluence,
        crewai,
        custom_component,
        data,
        datastax,
        deepseek,
        docling,
        duckduckgo,
        embeddings,
        exa,
        firecrawl,
        git,
        glean,
        google,
        groq,
        helpers,
        homeassistant,
        huggingface,
        ibm,
        icosacomputing,
        input_output,
        langchain_utilities,
        langwatch,
        lmstudio,
        logic,
        maritalk,
        mem0,
        mistral,
        models,
        needle,
        notdiamond,
        novita,
        nvidia,
        olivya,
        ollama,
        openai,
        openrouter,
        perplexity,
        processing,
        prototypes,
        redis,
        sambanova,
        scrapegraph,
        searchapi,
        serpapi,
        tavily,
        tools,
        twelvelabs,
        unstructured,
        vectorstores,
        vertexai,
        wikipedia,
        wolframalpha,
        xai,
        yahoosearch,
        youtube,
        zep,
    )

_dynamic_imports = {
    "agents": "axiestudio.components.agents",
    "data": "axiestudio.components.data",
    "processing": "axiestudio.components.processing",
    "vectorstores": "axiestudio.components.vectorstores",
    "tools": "axiestudio.components.tools",
    "models": "axiestudio.components.models",
    "embeddings": "axiestudio.components.embeddings",
    "helpers": "axiestudio.components.helpers",
    "input_output": "axiestudio.components.input_output",
    "logic": "axiestudio.components.logic",
    "custom_component": "axiestudio.components.custom_component",
    "prototypes": "axiestudio.components.prototypes",
    "openai": "axiestudio.components.openai",
    "anthropic": "axiestudio.components.anthropic",
    "google": "axiestudio.components.google",
    "azure": "axiestudio.components.azure",
    "huggingface": "axiestudio.components.huggingface",
    "ollama": "axiestudio.components.ollama",
    "groq": "axiestudio.components.groq",
    "cohere": "axiestudio.components.cohere",
    "mistral": "axiestudio.components.mistral",
    "deepseek": "axiestudio.components.deepseek",
    "nvidia": "axiestudio.components.nvidia",
    "amazon": "axiestudio.components.amazon",
    "vertexai": "axiestudio.components.vertexai",
    "xai": "axiestudio.components.xai",
    "perplexity": "axiestudio.components.perplexity",
    "openrouter": "axiestudio.components.openrouter",
    "lmstudio": "axiestudio.components.lmstudio",
    "sambanova": "axiestudio.components.sambanova",
    "maritalk": "axiestudio.components.maritalk",
    "novita": "axiestudio.components.novita",
    "olivya": "axiestudio.components.olivya",
    "notdiamond": "axiestudio.components.notdiamond",
    "needle": "axiestudio.components.needle",
    "cloudflare": "axiestudio.components.cloudflare",
    "baidu": "axiestudio.components.baidu",
    "aiml": "axiestudio.components.aiml",
    "ibm": "axiestudio.components.ibm",
    "langchain_utilities": "axiestudio.components.langchain_utilities",
    "crewai": "axiestudio.components.crewai",
    "composio": "axiestudio.components.composio",
    "mem0": "axiestudio.components.mem0",
    "datastax": "axiestudio.components.datastax",
    "cleanlab": "axiestudio.components.cleanlab",
    "langwatch": "axiestudio.components.langwatch",
    "icosacomputing": "axiestudio.components.icosacomputing",
    "homeassistant": "axiestudio.components.homeassistant",
    "agentql": "axiestudio.components.agentql",
    "assemblyai": "axiestudio.components.assemblyai",
    "twelvelabs": "axiestudio.components.twelvelabs",
    "docling": "axiestudio.components.docling",
    "unstructured": "axiestudio.components.unstructured",
    "redis": "axiestudio.components.redis",
    "zep": "axiestudio.components.zep",
    "bing": "axiestudio.components.bing",
    "duckduckgo": "axiestudio.components.duckduckgo",
    "serpapi": "axiestudio.components.serpapi",
    "searchapi": "axiestudio.components.searchapi",
    "tavily": "axiestudio.components.tavily",
    "exa": "axiestudio.components.exa",
    "glean": "axiestudio.components.glean",
    "yahoosearch": "axiestudio.components.yahoosearch",
    "apify": "axiestudio.components.apify",
    "arxiv": "axiestudio.components.arxiv",
    "confluence": "axiestudio.components.confluence",
    "firecrawl": "axiestudio.components.firecrawl",
    "git": "axiestudio.components.git",
    "wikipedia": "axiestudio.components.wikipedia",
    "youtube": "axiestudio.components.youtube",
    "scrapegraph": "axiestudio.components.scrapegraph",
    "Notion": "axiestudio.components.Notion",
    "wolframalpha": "axiestudio.components.wolframalpha",
}

__all__: list[str] = [
    "Notion",
    "agentql",
    "agents",
    "aiml",
    "amazon",
    "anthropic",
    "apify",
    "arxiv",
    "assemblyai",
    "azure",
    "baidu",
    "bing",
    "cleanlab",
    "cloudflare",
    "cohere",
    "composio",
    "confluence",
    "crewai",
    "custom_component",
    "data",
    "datastax",
    "deepseek",
    "docling",
    "duckduckgo",
    "embeddings",
    "exa",
    "firecrawl",
    "git",
    "glean",
    "google",
    "groq",
    "helpers",
    "homeassistant",
    "huggingface",
    "ibm",
    "icosacomputing",
    "input_output",
    "langchain_utilities",
    "langwatch",
    "lmstudio",
    "logic",
    "maritalk",
    "mem0",
    "mistral",
    "models",
    "needle",
    "notdiamond",
    "novita",
    "nvidia",
    "olivya",
    "ollama",
    "openai",
    "openrouter",
    "perplexity",
    "processing",
    "prototypes",
    "redis",
    "sambanova",
    "scrapegraph",
    "searchapi",
    "serpapi",
    "tavily",
    "tools",
    "twelvelabs",
    "unstructured",
    "vectorstores",
    "vertexai",
    "wikipedia",
    "wolframalpha",
    "xai",
    "yahoosearch",
    "youtube",
    "zep",
]


def __getattr__(attr_name: str) -> Any:
    """Lazily import component modules on attribute access.

    Args:
        attr_name (str): The attribute/module name to import.

    Returns:
        Any: The imported module or attribute.

    Raises:
        AttributeError: If the attribute is not a known component or cannot be imported.
    """
    if attr_name not in _dynamic_imports:
        msg = f"module '{__name__}' has no attribute '{attr_name}'"
        raise AttributeError(msg)
    try:
        # Use import_mod as in LangChain, passing the module name and package
        result = import_mod(attr_name, "__module__", __spec__.parent)
    except (ModuleNotFoundError, ImportError, AttributeError) as e:
        msg = f"Could not import '{attr_name}' from '{__name__}': {e}"
        raise AttributeError(msg) from e
    globals()[attr_name] = result  # Cache for future access
    return result


def __dir__() -> list[str]:
    """Return list of available attributes for tab-completion and dir()."""
    return list(__all__)


# Optional: Consistency check (can be removed in production)
_missing = set(__all__) - set(_dynamic_imports)
if _missing:
    msg = f"Missing dynamic import mapping for: {', '.join(_missing)}"
    raise ImportError(msg)
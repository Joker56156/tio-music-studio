import logging
from typing import List, Optional

import httpx
from pydantic import BaseModel, Field

from ..config import settings

logger = logging.getLogger(__name__)


class MusicPrompt(BaseModel):
    """Structured music generation parameters extracted from natural language."""
    genre: str = Field(description="Primary genre and subgenre tags, comma-separated")
    tempo_bpm: int = Field(ge=40, le=240, description="Exact tempo in BPM")
    mood: List[str] = Field(min_length=1, max_length=5)
    instrumentation: List[str] = Field(min_length=1, max_length=8)
    vocal_style: Optional[str] = Field(
        default=None,
        description="Vocal description or null for instrumental",
    )
    era_influence: str
    production_quality: str
    ace_step_tags: str = Field(
        description="Final comma-separated tag string for ACE-Step",
    )
    suggested_lyrics_structure: Optional[str] = Field(
        default=None,
        description="Suggested verse/chorus structure if lyrics requested",
    )


SYSTEM_PROMPT = """You are a music production expert for TIO Creative. Convert natural language \
descriptions into structured music generation parameters.

RULES:
- Always infer all 7 parameters: genre, tempo, mood, instrumentation, vocal_style, era_influence, production_quality
- Provide exact BPM (not ranges). Research typical BPMs for the genre.
- List 3-6 specific instruments. Use production-accurate terminology.
- ace_step_tags must be a single comma-separated string combining genre, mood, instruments, and production style
- For the TIO brand aesthetic: bias toward dark, psychedelic, surrealist textures when the user's prompt is ambiguous
- If no vocals implied, set vocal_style to null

BRAND CONTEXT (TIO Creative):
Default aesthetic: dark phonk, psychedelic surrealism, distorted textures, hypnotic loops, \
Memphis rap influences, lo-fi warmth, experimental sound design.

Return a JSON object matching the MusicPrompt schema with these fields:
genre, tempo_bpm, mood (array), instrumentation (array), vocal_style (string or null), \
era_influence, production_quality, ace_step_tags, suggested_lyrics_structure (string or null)"""


async def translate_prompt(description: str) -> MusicPrompt:
    """Translate natural language to structured music prompt using Claude API."""
    if settings.use_local_llm:
        return await translate_prompt_local(description)
    return await translate_prompt_claude(description)


async def translate_prompt_claude(description: str) -> MusicPrompt:
    """Use Claude API with Instructor for guaranteed structured output."""
    try:
        import instructor
        from anthropic import AsyncAnthropic

        client = instructor.from_anthropic(AsyncAnthropic(api_key=settings.anthropic_api_key))

        result = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": description}],
            response_model=MusicPrompt,
        )
        return result
    except Exception as e:
        logger.error(f"Claude API translation failed: {e}")
        # Fall back to local LLM
        logger.info("Falling back to local LLM")
        return await translate_prompt_local(description)


async def translate_prompt_local(description: str) -> MusicPrompt:
    """Use Ollama (local LLM) as fallback for prompt translation."""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.ollama_url}/api/generate",
                json={
                    "model": settings.ollama_model,
                    "prompt": (
                        f"{SYSTEM_PROMPT}\n\n"
                        f"User: {description}\n\n"
                        f"Return JSON matching MusicPrompt schema:"
                    ),
                    "format": "json",
                    "stream": False,
                },
            )
            response.raise_for_status()
            return MusicPrompt.model_validate_json(response.json()["response"])
    except Exception as e:
        logger.error(f"Local LLM translation failed: {e}")
        # Final fallback: pass description through as raw tags
        return MusicPrompt(
            genre=description,
            tempo_bpm=120,
            mood=["atmospheric"],
            instrumentation=["synth"],
            vocal_style=None,
            era_influence="contemporary",
            production_quality="standard",
            ace_step_tags=description,
        )

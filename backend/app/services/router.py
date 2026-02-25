from ..schemas.generation import GenerateRequest


def select_model(request: GenerateRequest) -> str:
    """Select the best model based on request parameters."""
    # Explicit model override
    if request.model:
        return request.model

    # Premium vocals with lyrics -> YuE
    if request.vocal_priority == "premium" and request.lyrics:
        return "yue"

    # Instrumental-only -> DiffRhythm for fast variations
    if request.instrumental:
        return "diffrhythm"

    # Default: ACE-Step 1.5 (fast + versatile)
    return "ace-step"

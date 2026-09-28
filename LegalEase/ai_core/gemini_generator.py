import google.generativeai as genai

from config import settings


class GeminiConfigurationError(RuntimeError):
    pass


class GeminiDocumentGenerator:
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            self.model = None
            return

        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: list[str],
        effective_date: object,
        additional_instructions: str = "",
    ) -> str:
        if self.model is None:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured. Add it to the .env file."
            )

        prompt = f"""Draft a professional {document_type}.

Parties:
{parties}

Effective date: {effective_date}

Required terms:
{chr(10).join(f"- {term}" for term in terms)}

Additional instructions:
{additional_instructions or "None"}

Return only the document text. Use clear numbered sections and include a
brief signature section. This is a draft for review by a qualified lawyer."""

        response = self.model.generate_content(prompt)
        content = getattr(response, "text", "").strip()
        if not content:
            raise RuntimeError("The Gemini response did not contain document text.")
        return content
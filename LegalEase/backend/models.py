from datetime import date

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=1)
    parties: str = Field(min_length=1)
    terms: list[str] = Field(min_length=1)
    effective_date: date
    additional_instructions: str = ""


class DocumentResponse(BaseModel):
    document_type: str
    content: str


class ExportRequest(BaseModel):
    document_type: str = "Legal Document"
    content: str = Field(min_length=1)
    terms: list[str] = Field(default_factory=list)
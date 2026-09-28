from io import BytesIO

from fastapi import APIRouter, HTTPException

from fastapi.responses import StreamingResponse

from ai_core.gemini_generator import (
    GeminiDocumentGenerator,
    GeminiConfigurationError
)

from backend.models import (
    DocumentRequest,
    DocumentResponse,
    ExportRequest
)

from utils.document_formats import (
    format_docx,
    format_pdf,
    format_txt
)


router = APIRouter()


generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        generated_content = (
            generator.generate_document(

                document_type=request.document_type,

                parties=request.parties,

                terms=request.terms,

                effective_date=request.effective_date,

                additional_instructions=(
                    request.additional_instructions
                    or ""
                )
            )
        )


        return DocumentResponse(

            document_type=request.document_type,

            content=generated_content
        )


    except GeminiConfigurationError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )


    except Exception as error:

        raise HTTPException(

            status_code=502,

            detail=(
                f"Document generation failed: {error}"
            )
        )


@router.post("/export/txt")
def export_txt(
    request: ExportRequest
):

    data = format_txt(
        request.content
    )


    return StreamingResponse(

        BytesIO(data),

        media_type="text/plain; charset=utf-8",

        headers={
            "Content-Disposition":
            "attachment; filename=legalease_document.txt"
        }
    )


@router.post("/export/docx")
def export_docx(
    request: ExportRequest
):

    data = format_docx(

        request.content,

        request.document_type,

        request.terms
    )


    return StreamingResponse(

        BytesIO(data),

        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),

        headers={
            "Content-Disposition":
            "attachment; filename=legalease_document.docx"
        }
    )


@router.post("/export/pdf")
def export_pdf(
    request: ExportRequest
):

    data = format_pdf(

        request.content,

        request.document_type,

        request.terms
    )


    return StreamingResponse(

        BytesIO(data),

        media_type="application/pdf",

        headers={
            "Content-Disposition":
            "attachment; filename=legalease_document.pdf"
        }
    )
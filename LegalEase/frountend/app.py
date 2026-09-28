import requests

from datetime import date

import streamlit as st


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


DEFAULT_BACKEND = (
    "http://127.0.0.1:8000"
)


if "backend_url" not in st.session_state:

    st.session_state.backend_url = (
        DEFAULT_BACKEND
    )


if "generated_document" not in st.session_state:

    st.session_state.generated_document = ""


if "document_type" not in st.session_state:

    st.session_state.document_type = (
        "Non-Disclosure Agreement"
    )


st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 2.6rem;

        font-weight: 800;

        margin-bottom: 0;
    }


    .subtitle {

        text-align: center;

        color: #777;

        margin-bottom: 2rem;
    }


    .notice {

        padding: 1rem;

        border-radius: 0.6rem;

        background: #fff4d6;

        border: 1px solid #e5c76b;
    }

    </style>
    """,

    unsafe_allow_html=True
)


st.markdown(

    '<div class="main-title">'
    '⚖️ LegalEase'
    '</div>',

    unsafe_allow_html=True
)


st.markdown(

    '<div class="subtitle">'
    'AI-powered legal document draft generator'
    '</div>',

    unsafe_allow_html=True
)


with st.sidebar:

    st.header("Settings")


    backend_url = st.text_input(

        "FastAPI backend URL",

        value=(
            st.session_state.backend_url
        )
    ).rstrip("/")


    st.session_state.backend_url = (
        backend_url
    )


    st.markdown(

        '<div class="notice">'
        'Generated documents are drafts. '
        'Review them with a qualified legal '
        'professional before signing or relying '
        'on them.'
        '</div>',

        unsafe_allow_html=True
    )


left, right = st.columns(
    [1, 1]
)


with left:

    st.subheader(
        "1. Document Details"
    )


    document_options = [

        "Employment Contract",

        "Non-Disclosure Agreement",

        "Lease Agreement",

        "Employment Offer Letter",

        "Freelance Work Contract",

        "Service Agreement",

        "Other"
    ]


    selected_type = st.selectbox(

        "Document Type",

        document_options
    )


    if selected_type == "Other":

        document_type = st.text_input(

            "Enter document type",

            value=(
                st.session_state.document_type
            )
        )

    else:

        document_type = selected_type


    parties = st.text_area(

        "Parties Involved",

        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=120
    )


    terms_text = st.text_area(

        "Terms & Conditions",

        placeholder=(

            "Payment to be made within 30 days "
            "of invoice; Confidentiality must be "
            "maintained; Either party may terminate "
            "with 15 days notice"
        ),

        height=160,

        help=(
            "Separate each term using a semicolon (;)."
        )
    )


    effective_date = st.date_input(

        "Effective Date",

        value=date.today()
    )


    additional_instructions = st.text_area(

        "Additional Instructions",

        placeholder=(

            "Example: Keep the agreement concise "
            "and use numbered sections."
        ),

        height=100
    )


    logo = st.file_uploader(

        "Optional Logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    generate_button = st.button(

        "✨ Generate Document",

        type="primary",

        use_container_width=True
    )


with right:

    st.subheader(
        "2. Preview & Edit"
    )


    if generate_button:

        terms = [

            term.strip()

            for term in terms_text.split(";")

            if term.strip()
        ]


        if not document_type.strip():

            st.error(
                "Please enter a document type."
            )


        elif not parties.strip():

            st.error(
                "Please enter the parties involved."
            )


        elif not terms:

            st.error(
                "Please enter at least one term."
            )


        else:

            payload = {

                "document_type":
                    document_type.strip(),

                "parties":
                    parties.strip(),

                "terms":
                    terms,

                "effective_date":
                    effective_date.isoformat(),

                "additional_instructions":
                    additional_instructions.strip()
            }


            with st.spinner(
                "Generating your legal document..."
            ):

                try:

                    response = requests.post(

                        f"{backend_url}/generate",

                        json=payload,

                        timeout=120
                    )


                    if response.ok:

                        data = response.json()


                        st.session_state.generated_document = (
                            data["content"]
                        )


                        st.session_state.document_type = (
                            document_type
                        )


                        st.success(
                            "Document generated successfully!"
                        )


                    else:

                        try:

                            error_detail = (
                                response.json()
                                .get(
                                    "detail",
                                    response.text
                                )
                            )

                        except ValueError:

                            error_detail = (
                                response.text
                            )


                        st.error(
                            f"Backend error: "
                            f"{error_detail}"
                        )


                except requests.RequestException as error:

                    st.error(

                        "Could not connect to FastAPI. "
                        "Make sure the backend is running.\n\n"
                        f"Details: {error}"
                    )


    if st.session_state.generated_document:

        edited_document = st.text_area(

            "Editable Document",

            value=(
                st.session_state.generated_document
            ),

            height=650
        )


        st.session_state.generated_document = (
            edited_document
        )


        terms = [

            term.strip()

            for term in terms_text.split(";")

            if term.strip()
        ]


        st.subheader(
            "3. Download"
        )


        col1, col2, col3 = st.columns(3)


        def export_document(
            endpoint: str
        ):

            return requests.post(

                f"{backend_url}{endpoint}",

                json={

                    "document_type":
                        st.session_state.document_type,

                    "content":
                        st.session_state.generated_document,

                    "terms":
                        terms
                },

                timeout=60
            )


        with col1:

            if st.button(
                "Prepare TXT",
                use_container_width=True
            ):

                try:

                    response = export_document(
                        "/export/txt"
                    )


                    response.raise_for_status()


                    st.download_button(

                        "⬇️ Download TXT",

                        data=response.content,

                        file_name=(
                            "legalease_document.txt"
                        ),

                        mime="text/plain",

                        use_container_width=True
                    )


                except requests.RequestException as error:

                    st.error(
                        f"TXT export failed: {error}"
                    )


        with col2:

            if st.button(
                "Prepare DOCX",
                use_container_width=True
            ):

                try:

                    response = export_document(
                        "/export/docx"
                    )


                    response.raise_for_status()


                    st.download_button(

                        "⬇️ Download DOCX",

                        data=response.content,

                        file_name=(
                            "legalease_document.docx"
                        ),

                        mime=(
                            "application/"
                            "vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        ),

                        use_container_width=True
                    )


                except requests.RequestException as error:

                    st.error(
                        f"DOCX export failed: {error}"
                    )


        with col3:

            if st.button(
                "Prepare PDF",
                use_container_width=True
            ):

                try:

                    response = export_document(
                        "/export/pdf"
                    )


                    response.raise_for_status()


                    st.download_button(

                        "⬇️ Download PDF",

                        data=response.content,

                        file_name=(
                            "legalease_document.pdf"
                        ),

                        mime="application/pdf",

                        use_container_width=True
                    )


                except requests.RequestException as error:

                    st.error(
                        f"PDF export failed: {error}"
                    )


        with st.expander(
            "Preview Document"
        ):

            safe_text = (

                st.session_state
                .generated_document

                .replace("&", "&amp;")

                .replace("<", "&lt;")

                .replace(">", "&gt;")

                .replace("\n", "<br>")
            )


            st.markdown(

                f"""
                <div
                    style="
                    padding:20px;
                    border:1px solid #555;
                    border-radius:8px;
                    max-height:500px;
                    overflow:auto;
                    "
                >
                    {safe_text}
                </div>
                """,

                unsafe_allow_html=True
            )


    else:

        st.info(
            "Your generated document will appear here."
        )


if logo:

    st.caption(
        f"Logo uploaded: {logo.name}"
    )
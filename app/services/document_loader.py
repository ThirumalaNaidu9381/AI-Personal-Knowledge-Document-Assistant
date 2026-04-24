from pypdf import PdfReader
import io


def load_pdf(file_bytes: bytes) -> str:
    pdf = PdfReader(io.BytesIO(file_bytes))

    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"

    return text


def load_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8")


def load_document(file_name: str, file_bytes: bytes) -> str:
    if file_name.endswith(".pdf"):
        return load_pdf(file_bytes)

    elif file_name.endswith(".txt"):
        return load_txt(file_bytes)

    else:
        raise ValueError("Unsupported file type")
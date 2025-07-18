import streamlit as st
from cv_parser import *

correction_prompt = "https://chatgpt.com/share/68790f3d-7a10-800f-bfaa-c04f4f6cf5b5"
# === Execution ===
st.title("Resume Reformater")
pdf_file = st.file_uploader("Upload your resume")
extracted_text = extract_text_from_pdf(pdf_file)
edited_text = st.text_area("Extracted text", value=extracted_text)
st.caption("NOTICE: For better accuracy Copy and Paste the"
            f" extracted text above into the prompt below and then paste "
            f"the output back into "
            f"EXTRACTED TEXT box")
st.markdown(f"[Use this prompt to format the text.]({correction_prompt})")


if st.button("convert"):
    document = read_word(template_docx)
    extracted_data = extract_sections(document)
    section_data = extract_sections(edited_text)
    data_to_insert = hidden_data_collector(edited_text, section_data)
    data = populate_word_dic(data_to_insert, extracted_data)
    final_text = bullet_points_check(data)
    word_file = replace_placeholders(final_text)
    convert_docx_to_pdf()

    with open("Converted_resume.pdf", "rb") as file:
        pdf_bytes = file.read()

    st.download_button(
        label="Download file",
        data=pdf_bytes,
        file_name="Converted_resume.pdf",
        mime="application/pdf",
    )

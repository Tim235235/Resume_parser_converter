import streamlit as st
from cv_parser import *

correction_prompt = "https://chatgpt.com/share/687a98af-3d28-800f-a4e6-16af01eac36d"
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

    if word_file and os.path.exists(word_file):
        with open(word_file, "rb") as file:
            st.download_button(
                label="Download Word Resume",
                data=file,
                file_name="Converted_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.error("Resume generation failed.")


import streamlit as st


st.title(
    "Form 예제"
)


with st.form(
    "my_form"
):


    name = st.text_input(
        "이름"
    )


    email = st.text_input(
        "Email"
    )


    age = st.number_input(
        "나이",
        min_value=0,
        max_value=150,
        value=20,
        step=1,
        format="%d"
    )


    submit = st.form_submit_button(
        "가입"
    )



if submit:


    st.success(
        "제출 완료"
    )


    st.write(
        name,
        email,
        age
    )
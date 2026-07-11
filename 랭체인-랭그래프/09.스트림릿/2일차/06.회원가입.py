import streamlit as st


st.title(
    "회원가입"
)


with st.form(
    "register"
):


    userid = st.text_input(
        "아이디"
    )


    password = st.text_input(
        "비밀번호",
        type="password"
    )


    email = st.text_input(
        "이메일"
    )


    birth = st.date_input(
        "생년월일"
    )


    gender = st.radio(
        "성별",
        [
            "남",
            "여"
        ]
    )


    agree = st.checkbox(
        "약관 동의"
    )



    submit = st.form_submit_button(
        "가입하기"
    )



if submit:
    if agree:
        st.success(
            "회원가입 완료"
        )

        st.write(
            {
                "id":userid,
                "email":email,
                "birth":birth,
                "gender":gender
            }
        )
    else:
        st.error(
            "약관 동의 필요"
        )
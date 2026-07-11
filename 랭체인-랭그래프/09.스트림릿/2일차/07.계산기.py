import streamlit as st


st.title(
    "계산기"
)


num1 = st.number_input(
    "첫번째 숫자"
)


num2 = st.number_input(
    "두번째 숫자"
)


operator = st.selectbox(
    "연산",
    [
        "+",
        "-",
        "*",
        "/"
    ]
)



if st.button(
    "계산"
):


    result = 0


    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error(
                "0으로 나눌 수 없습니다."
            )


    st.success(
        f"결과 : {result}"
    )
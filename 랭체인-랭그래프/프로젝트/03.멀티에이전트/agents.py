import sys
from pathlib import Path
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()

#Math Agent
def math_agent(state):

    prompt = f"""
    당신은 수학 전문가입니다.

    질문:
    {state["question"]}
    """

    result = llm.invoke(prompt)

    return {
        "answer": result.content
    }

#English Agent
def english_agent(state):

    prompt = f"""
    당신은 영어 번역 전문가입니다.

    질문:
    {state["question"]}
    """
    
    
    result = llm.invoke(prompt)
    print("이걸타나")
    return {
        "answer": result.content
    }
# General Agent
def general_agent(state):

    prompt = f"""
    당신은 일반 AI입니다.

    질문:
    {state["question"]}
    """

    result = llm.invoke(prompt)

    return {
        "answer": result.content
    }
from typing import TypedDict


class AnalysisState(TypedDict):
    question: str
    analysis_type: str
    code: str
    result: str
    dataframe: object
    error: str
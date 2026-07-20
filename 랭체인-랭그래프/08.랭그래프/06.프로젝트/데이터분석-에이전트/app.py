from graph import graph

import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent.parent)
)

from util import show_graph
show_graph(graph)

while True:

    question = input("\n질문(exit 종료): ")

    if question.lower() == "exit":
        break

    result = graph.invoke(
        {
            "question": question,
            "analysis_type": "",
            "code": "",
            "result": "",
            "dataframe": None,
            "error": ""
        }
    )
    print("\n============================")
    print(result["result"])
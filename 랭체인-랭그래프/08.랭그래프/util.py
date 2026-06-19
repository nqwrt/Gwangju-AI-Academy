import subprocess


def show_graph(graph):

    png = (
        graph
        .get_graph()
        .draw_mermaid_png()
    )

    file = "graph.png"

    with open(
        file,
        "wb"
    ) as f:

        f.write(
            png
        )

    subprocess.run(
        ["start", file],
        shell=True
    )
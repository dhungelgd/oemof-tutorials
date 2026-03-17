from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from oemof.network.graph import create_nx_graph

def plot_energy_system_graph(energy_system, scenario_name="scenario", save_dir=None):

    # Set default save directory to results
    if save_dir is None:
        project_root = Path(__file__).resolve().parent.parent
        save_dir = project_root / "results" / "graphs"
    else:
        save_dir = Path(save_dir)

    # Make sure folder exists
    save_dir.mkdir(parents=True, exist_ok=True)

    dot_file = save_dir / f"{scenario_name}.dot"
    png_file = save_dir / f"{scenario_name}.png"

    graph = create_nx_graph(energy_system)

    nx.drawing.nx_pydot.write_dot(graph, dot_file)
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="gray",
            font_size=9, font_weight="bold")
    plt.title(f"Energy System Graph: {scenario_name}")
    # plt.tight_layout()
    plt.savefig(png_file)
    plt.show()

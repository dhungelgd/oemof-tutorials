from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from oemof.network.graph import create_nx_graph
import plotly.graph_objects as go
import numpy as np

# plot energy system graph
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

# plot energy flows
def plot_energy_flows(flows, bus_name, start=None, end=None):

    # select time range
    if start is not None and end is not None:
        flows = flows.loc[start:end]

    # identify supply and demand
    supply_cols = [c for c in flows.columns if c.endswith(f"_{bus_name}")]
    demand_cols = [c for c in flows.columns if c.startswith(f"{bus_name}_")]

    if not supply_cols and not demand_cols:
        raise ValueError(f"No flows found for bus '{bus_name}'")

    # sort supply for cleaner plots
    supply_cols = sorted(supply_cols)

    # stack
    x = flows.index
    baseline = np.zeros(len(flows))

    plt.figure(figsize=(12, 6))

    # plot supply stack
    for col in supply_cols:
       values = flows[col].values

       plt.fill_between(
           x,
           baseline,
           baseline+values,
           step="pre",
           label=col.replace(f"_{bus_name}_", "")
       )

       baseline += values

    # plt demand
    if demand_cols:
        demand = flows[demand_cols].sum(axis=1)

        plt.step(
            x,
            demand,
            where="pre",
            color="black",
            linewidth=2,
            label="Demand",
        )

        plt.xlabel("Time", fontsize=14, fontweight="bold")
        plt.ylabel("Power (kW)", fontsize=14, fontweight="bold")

        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.gcf().autofmt_xdate()
        plt.tight_layout()

        plt.show()

# plot with plotly
def plot_energy_flows_plotly(flows, bus_name, start=None, end=None):

    # select time range
    if start is not None and end is not None:
        flows = flows.loc[start:end]

    # identify supply and demand
    supply_cols = [c for c in flows.columns if c.endswith(f"_{bus_name}")]
    demand_cols = [c for c in flows.columns if c.startswith(f"{bus_name}_")]

    if not supply_cols and not demand_cols:
        raise ValueError(f"No flows found for bus '{bus_name}'")

    # sort supply for cleaner plots
    supply_cols = sorted(supply_cols)

    # create figure
    fig = go.Figure()

    for col in supply_cols:

        fig.add_trace(
            go.Scatter(
                x=flows.index,
                y=flows[col],
                mode="lines",
                name=col.replace(f"_{bus_name}", ""),
                line=dict(width=0.5),
                stackgroup="one"
            )
        )

    # plot demand
    if demand_cols:
        demand = flows[demand_cols].sum(axis=1)

        fig.add_trace(
            go.Scatter(
                x=flows.index,
                y=demand,
                mode="lines",
                name="Demand",
                line=dict(color="black", width=3),
            )
        )

    # layout
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        xaxis=dict(
            title="Time",
            showline=True,
            linewidth=3,
            linecolor="black",
        ),
        yaxis=dict(
            title="Power (kW)",
            showline=True,
            linewidth=3,
            linecolor="black"
        ),
        legend=dict(font=dict(size=12)),
    )

    fig.show()




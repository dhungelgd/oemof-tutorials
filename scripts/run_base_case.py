from src.scenario_runner import run_scenario
from src.plotting import plot_energy_system_graph, plot_energy_flows, plot_energy_flows_plotly
from src.postprocessing import process_results, compute_energy_sums
from pathlib import Path
import os

scenario_name = "03_pv_battery_system"
project_root = Path(__file__).resolve().parent.parent
config_file = os.path.join(os.path.dirname(__file__), "..", "config", f"{scenario_name}.yaml")
es, results, meta_results = run_scenario(config_file)

# plot the network graph
plot_energy_system_graph(
    energy_system=es,
    scenario_name=scenario_name,
    save_dir=project_root / "results" / "graphs"
)

print(f"Total annual costs: {meta_results['objective']:.2f} €")

# process flows
flows = process_results(results=results, bus_name="electricity")
print(flows)

# print each enegy flow sums
print(compute_energy_sums(flows))

#plot the energy flows
plot_energy_flows(flows, bus_name="electricity", start="2021-02-01", end="2021-02-07")
plot_energy_flows_plotly(flows, bus_name="electricity", start="2021-02-01", end="2021-02-07")

from src.scenario_runner import run_scenario
from src.plotting import plot_energy_system_graph
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent
config_file = os.path.join(os.path.dirname(__file__), "..", "config", "technologies.yaml")
es, results, meta_results = run_scenario(config_file)

# plot the network graph
plot_energy_system_graph(
    energy_system=es,
    scenario_name="base_case",
    save_dir=project_root / "results" / "plots"
)

print(f"Total annual costs: {meta_results['objective']:.2f} €")


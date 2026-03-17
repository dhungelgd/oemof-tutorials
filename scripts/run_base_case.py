from src.scenario_runner import run_scenario
import os

config_file = os.path.join(os.path.dirname(__file__), "..", "config", "technologies.yaml")
es, results, meta_results = run_scenario(config_file)

print(f"Total annual costs: {meta_results['objective']:.2f} €")
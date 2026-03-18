from oemof import solph
from .model import build_energy_system
from .data_loader import load_csv, load_yaml

# create a function to run scenario based on given config fiel
def run_scenario(config_file):

    # load yaml config
    config = load_yaml(config_file)

    # load input csv data
    input_data = load_csv(config["technologies"]["electricity_demand"]["profile"])

    # build energy system
    es, buses = build_energy_system(config, input_data)

    # solver settings from yaml
    solver_cfg = config["solver"]

    # solve optimization model
    model = solph.Model(es)
    model.solve(solver = solver_cfg["name"], solve_kwargs={"tee": solver_cfg["tee"]})

    # extract results
    results = solph.processing.results(model)
    meta_results = solph.processing.meta_results(model)

    return es, results, meta_results

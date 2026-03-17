from oemof import solph
from .model import build_energy_system
from .data_loader import load_csv, load_yaml

# create a function to run scenario based on given config fiel
def run_scenario(config_file):

    # load yaml config
    config = load_yaml(config_file)

    # load input csv data
    load_profile = load_csv(config["demand"]["profile"])

    # build energy system
    es, el_bus, grid = build_energy_system(config, load_profile)

    # solver settings from yaml
    solver_cfg = config["solver"]

    # solve optimization
    model = solph.Model(es)
    model.solve(solver = solver_cfg["name"], solve_kwargs={"tee": solver_cfg["tee"]})

    # extract results
    results = solph.processing.results(model)
    meta_results = solph.processing.meta_results(model)

    return es, results, meta_results

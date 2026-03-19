from src.technologies import TECH_MAPPING
from oemof import solph

# build an energy system using solph
def build_energy_system(config, input_data):

    #create an energy system
    es = solph.EnergySystem(timeindex=input_data.index, infer_last_interval=True)

    # dictionary to store references to buses
    buses = {}

    # create buses
    buses["electricity"] = solph.Bus(label="electricity")
    es.add(buses["electricity"])

    # loop through all technology types in the mapping
    for tech_name, tech_cfg in config["technologies"].items():

        add_func = TECH_MAPPING.get(tech_name)

        if add_func is None:
            raise ValueError(f"No implementation for technology: {tech_name}")

        add_func(es, buses, tech_cfg, input_data)

    return es, buses
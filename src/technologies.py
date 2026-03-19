from oemof import solph

# create a function for each component

# electricity demand
def add_electricity_demand(es, buses, cfg, input_data):

    electricity_demand = solph.components.Sink(
        label="electricity_demand",
        inputs={
            buses["electricity"]: solph.Flow(
                nominal_capacity=cfg["scaling_factor"],
                fix=input_data[cfg["column"]]
            )
        }
    )

    es.add(electricity_demand)

# electricity grid
def add_electricity_grid(es, buses, cfg, input_data):

    grid = solph.components.Source(
        label="grid",
        outputs={
            buses["electricity"]: solph.Flow(
                variable_costs=cfg["variable_costs"]
            )
        }
    )

    es.add(grid)

# pv
def add_pv(es, buses, cfg, input_data):

    # decide whether PV is fixed or can be optimized
    if cfg.get("mode", "optimizable")  == "fixed":
        flow_param = {"fix": input_data[cfg["column"]]}
    else:
        flow_param = {"maximum": input_data[cfg["column"]]}

    pv = solph.components.Source(
        label="pv",
        outputs={
            buses["electricity"]: solph.Flow(
                nominal_capacity=cfg["capacity"],
                **flow_param
            )
        }
    )

    es.add(pv)

# mapping dictionary
TECH_MAPPING = {
    "electricity_demand": add_electricity_demand,
    "electricity_grid": add_electricity_grid,
    "pv": add_pv
}
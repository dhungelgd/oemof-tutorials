from oemof import solph
from src.economics import calculate_epc

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
    if cfg.get("mode", "fixed")  == "fixed":
        flow_param = {"fix": input_data[cfg["column"]]}
        nominal_capacity = cfg["capacity"]

    elif cfg.get("mode") == "invest":

        epc = calculate_epc(
            capex=cfg["capex"],
            fixed_opex_pct=cfg["opex"],
            lifetime=cfg["lifetime"],
            interest_rate=cfg["interest_rate"]
        )

        flow_param = {"fix": input_data[cfg["pv_column"]]}
        nominal_capacity = solph.Investment(ep_costs=epc)
    else:
        raise ValueError(f"Unknown mode {cfg['mode']} for PV")

    pv = solph.components.Source(
        label="pv",
        outputs={
            buses["electricity"]: solph.Flow(
                nominal_capacity=nominal_capacity,
                **flow_param
            )
        }
    )

    es.add(pv)

# battery
def add_battery(es, buses, cfg, input_data):

    if cfg.get("mode", "fixed") == "fixed":

        nominal_capacity = cfg["capacity"]

    elif cfg.get("mode") == "invest":

        epc = calculate_epc(
            capex=cfg["capex"],
            fixed_opex_pct=cfg["opex"],
            lifetime=cfg["lifetime"],
            interest_rate=cfg["interest_rate"]
        )

        nominal_capacity = solph.Investment(ep_costs=epc)

    else:
        raise ValueError(f"Unknown mode {cfg['mode']}")

    battery = solph.components.GenericStorage(
        label="Battery",
        nominal_capacity=nominal_capacity,

        inputs={
            buses["electricity"]: solph.Flow()
        },
        outputs={
            buses["electricity"]: solph.Flow()
        },

        inflow_conversion_factor=cfg["inflow_conversion_factor"],
        outflow_conversion_factor=1,   # recommended explicitly
        loss_rate=cfg["loss_rate"]
    )

    es.add(battery)

# mapping dictionary
TECH_MAPPING = {
    "electricity_demand": add_electricity_demand,
    "electricity_grid": add_electricity_grid,
    "pv": add_pv,
    "battery": add_battery
}
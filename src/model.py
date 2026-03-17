from oemof import solph

# build a energy system using solph
def build_energy_system(config, input_data):

    # create energy system
    es = solph.EnergySystem(
        timeindex=input_data.index,
        infer_last_interval=True
    )

    # create an electricity bus
    el_bus = solph.Bus(label="electricity")

    # electricity demand
    demand_cfg = config["demand"]
    electricity_demand = solph.components.Sink(
        label = "electricity_demand",
        inputs = {
            el_bus: solph.Flow(
                nominal_capacity=demand_cfg["scaling_factor"],
                fix=input_data[demand_cfg["column"]],
            )
        }
    )

    # add grid supply
    grid_cfg = config["grid"]
    grid = solph.Bus(
        label = "electricity_grid",
        outputs={el_bus: solph.Flow(variable_costs=grid_cfg["variable_costs"])},
        balanced=False
    )

    # add the components to the energy system
    es.add(el_bus, electricity_demand, grid)

    return es, el_bus, grid
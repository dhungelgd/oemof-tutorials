from oemof.solph import views

# Extract flows from a bus
def get_bus_flows(results, bus_name):

    flows = views.node(results, bus_name)["sequences"]

    return flows

# Flatten column names
def flatten_flows(df):
    # convert multi-index columns to simple string names
    # e.g. (("pv", "electricity"), "flow")  --> "pv_electricity"

    df_flat = df.copy()
    df_flat.columns = [
        f"{col[0][0]}_{col[0][1]}" for col in df.columns
    ]

    return df_flat

# Get supply and demand columns automatically
def split_supply_demand(flows, bus_name):
    # split flows into supply (to bus) and demand (from bus)

    supply_cols = [c for c in flows.columns if c.endswith(f"_{bus_name}")]
    demand_cols = [c for c in flows.columns if c.startswith(f"{bus_name}_")]

    return supply_cols, demand_cols

# compute total energy per flow
def compute_energy_sums(flows):

    return flows.sum()


# full processing pipeline
def process_results(results, bus_name):

    flows = get_bus_flows(results, bus_name)
    flows = flatten_flows(flows)

    return flows

# extract investment capacities from results
def get_investment_capacities(results):

    capacities = {}

    for (comp, bus), data in results.items():

        if not hasattr(comp, "label"):
            continue

        tech = comp.label

        scalars = data.get("scalars")

        if scalars is None:
            continue

        invest_val = None

        try:
            invest_val = scalars.get("invest", None)
        except Exception:
            pass

        if invest_val is None:
            try:
                for item in scalars:
                    if isinstance(item, tuple) and item[0] == "invest":
                        invest_val = item[1]
                        break
            except Exception:
                pass

        if invest_val is not None:
            capacities[tech] = float(invest_val)

    return capacities
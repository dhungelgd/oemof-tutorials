from oemof.tools import economics

# create a function to calculate epc
def calculate_epc(capex, fixed_opex_pct, lifetime, interest_rate):

    epc_capex = economics.annuity(capex=capex, n=lifetime, wacc=interest_rate)
    epc_opex = capex * fixed_opex_pct / 100

    return epc_capex + epc_opex




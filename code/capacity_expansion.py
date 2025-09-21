import xpress
def init_xpress_license():
    import os
    os.environ['XPAUTH_PATH'] = "xpauth.xpr" 
    license_path = "xpauth.xpr"

    xpress.beginlicensing()

    n, str_ = xpress.license(0, "")
    lic = 1111 - (n * n // 19)
    n, _ = xpress.license(lic, str_)
    xpress.init(lic_path=license_path)

    xpress.endlicensing()

init_xpress_license()



# Line-up with Julia code
import pandas as pd
import linopy

data_path = "/data/"
generators = pd.read_csv(data_path + "generators_for_expansion.csv")
generators.set_index('G', inplace=True)

demand = pd.read_csv(data_path + "demand_for_expansion.csv")
hours = len(demand)

# Incerase demand to 30 years
orig_demand = demand.copy()
for i in range(30-1):
    new_demand = orig_demand.copy()
    new_demand['Hour'] += hours*(i+1)
    demand = pd.concat([demand, new_demand], ignore_index=True)

NSECost = 9000  # $/MWh - Penalty for non-served energy

Expansion_Model = linopy.Model()

G = generators.index[:-2].tolist()  # Exclude last 2 rows (Wind and Solar)
H = demand['Hour'].tolist()

G_index = pd.Index(G, name="G")
H_index = pd.Index(H, name="H")

CAP = Expansion_Model.add_variables(
    lower=0,
    coords=[G_index],
    name="CAP"
)

GEN = Expansion_Model.add_variables(
    lower=0,
    coords=[G_index, H_index],
    name="GEN"
)

NSE = Expansion_Model.add_variables(
    lower=0,
    coords=[H_index],
    name="NSE"
)

demand_values = demand.rename(columns={'Hour': 'H'}).set_index('H')['Demand']
cDemandBalance = Expansion_Model.add_constraints(
    GEN.sum(dim='G') + NSE == demand_values,
    name="cDemandBalance"
)

cCapacity = Expansion_Model.add_constraints(
    GEN <= CAP,
    name="cCapacity"
)

Expansion_Model.add_objective(
    (generators['FixedCost'] * CAP).sum() +
    (generators['VarCost'] * GEN).sum() +
    (NSECost * NSE).sum()
)

# Solve the optimization model
Expansion_Model.solve(solver_name='xpress')
# Expansion_Model.solve()

# Extract solution values
cap_solution = CAP.solution.to_pandas()
gen_solution = GEN.solution.to_pandas()
nse_solution = NSE.solution.to_pandas()

generation_totals = gen_solution.sum(axis=1)
total_demand = demand_values.sum()
peak_demand = demand_values.max()

mwh_share = generation_totals / total_demand * 100
cap_share = cap_solution / peak_demand * 100

# Create results DataFrame (equivalent to Julia results)
results = pd.DataFrame({
    'Resource': G,
    'MW': cap_solution.values,
    'Percent_MW': cap_share.values,
    'GWh': generation_totals.values / 1000,  # Convert to GWh
    'Percent_GWh': mwh_share.values
})

# Add non-served energy results
nse_mw = nse_solution.max()  # Peak non-served energy
nse_mwh = nse_solution.sum()  # Total non-served energy

nse_row = pd.DataFrame({
    'Resource': ['NSE'],
    'MW': [nse_mw],
    'Percent_MW': [nse_mw / peak_demand * 100],
    'GWh': [nse_mwh / 1000],
    'Percent_GWh': [nse_mwh / total_demand * 100]
})

results = pd.concat([results, nse_row], ignore_index=True)
print(results)
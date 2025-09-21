ENV["XPRESS_JL_NO_AUTO_INIT"] = true
ENV["XPRESSDIR"] = "/xpressmp"

import Pkg
Pkg.add("Xpress")

using Xpress
liccheck(x::Vector{Cint}) = begin
    oemnum = 1111
    n = x[1]  # This corresponds to the 'n' from xpress.license(0, "") in Python
    lic = oemnum - (n * n ÷ 19)  # Use ÷ for integer division in Julia
    return Cint[lic]
end

Xpress.initialize(;
    liccheck = liccheck,
    verbose = true,
    xpauth_path = "xpauth.xpr",
)

# Line-up with Python code
using JuMP, HiGHS
using DataFrames, CSV, Statistics

data_path = "/data/"
generators = DataFrame(CSV.File(data_path*"generators_for_expansion.csv"))

demand = DataFrame(CSV.File(data_path*"demand_for_expansion.csv"))
hours = nrow(demand)

# Increase demand to 30 years
orig_demand = copy(demand)
for i in 1:29
    global demand
    new_demand = copy(orig_demand)
    new_demand.Hour .+= hours * i
    demand = vcat(demand, new_demand)
end

NSECost = 9000 # $/MWh

Expansion_Model = Model(Xpress.Optimizer)
# Expansion_Model = Model(HiGHS.Optimizer)

G = generators.G[1:(size(generators,1)-2)]
H = demand.Hour


@variables(Expansion_Model, begin
        CAP[g in G]         >= 0  # Generating capacity built (MW)
        GEN[g in G, h in H] >= 0  # Generation in each hour (MWh)
        NSE[h in H]         >= 0  # Non-served energy in each hour (MWh)
    end)

@constraints(Expansion_Model, begin
    cDemandBalance[h in H],    sum(GEN[g,h] for g in G) + NSE[h] == demand.Demand[h]
    cCapacity[g in G, h in H], GEN[g,h]                          <= CAP[g]
end)

@objective(Expansion_Model, Min,
    sum(generators[generators.G.==g,:FixedCost][1]*CAP[g] +
        sum(generators[generators.G.==g,:VarCost][1]*GEN[g,h] for h in H)
    for g in G) +
    sum(NSECost*NSE[h] for h in H)
);

optimize!(Expansion_Model)

generation = zeros(size(G, 1))
for i in 1:size(G,1)
    generation[i] = sum(value.(GEN)[G[i],:].data)
end

MWh_share = generation./sum(demand.Demand).*100
cap_share = value.(CAP).data./maximum(demand.Demand).*100
results = DataFrame(
    Resource = G,
    MW = value.(CAP).data,
    Percent_MW = cap_share,
    GWh = generation/1000,
    Percent_GWh = MWh_share
)

NSE_MW = maximum(value.(NSE).data)
NSE_MWh = sum(value.(NSE).data)

# Add non-served energy results
push!(results, ["NSE" NSE_MW NSE_MW/maximum(demand.Demand)*100 NSE_MWh/1000 NSE_MWh/sum(demand.Demand)*100])
print(results)
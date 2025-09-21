---
layout: post
title:  "jump vs linopy"
categories: development performance linopy pandas jump julia
tags: performance frameworks
---
# Linopy vs JuMP (quick notes)
During the effort to increase time to solve our linear optimisation problem I've desided to evaluate switching from Python to Julia.

Linopy [benchmarking page](https://linopy.readthedocs.io/en/latest/benchmark.html) claims that Julia has better performance in terms of solution time.

I've compared solution of capacity expansion model in Jump and Linopy.

Code for the model is taken from this [course](https://github.com/Power-Systems-Optimization-Course/power-systems-optimization/blob/master/Notebooks/03-Basic-Capacity-Expansion.ipynb).

I've extended demand to 30 years to increase the number of parameters of the model and size of the data.

# Here are results
| Library | HiGHs | Xpress |
| ---     | ---   | ---    |
|Linopy | 2m 31s | 23s
|JuMP | 2m 37s | 52s

Linopy used less memory as well.
Julia's Xpress library is not officially supported, that could explain why it was slower.

Code can be found in the `/code` folder.

# Conclusion
For learning purposes it was easier to use Julia's syntax to transition from math formulas to the model definition. But regarding solving time and data manipulation there are no significant benefits.

Pandas manipulates data faster than Julia's DataFrames library. It loads data quicker and uses less memory.

Since majority of time is spend in the solver and data preparation is more convenient in Pandas, don't see reasons to switch to Julia. At least for cases when no heavy computations are performed before the model is solved.


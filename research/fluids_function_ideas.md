# Potential Excel Functions from the CalebBell/fluids Python Package

## Overview
The [CalebBell/fluids](https://github.com/CalebBell/fluids) Python package provides a comprehensive set of fluid mechanics and transport property calculations for engineering applications. Integrating its capabilities into Excel via custom functions would enable engineers and scientists to perform advanced fluid dynamics analyses directly within spreadsheets. Below is a table of function ideas organized in the exact order of modules as shown in the official fluids documentation: https://fluids.readthedocs.io/modules.html

---

## Function Ideas by fluids API Module (Official Order)

### fluids.atmosphere
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Atmospheric properties         | Standard atmosphere, solar position, etc.           | Z, latitude, longitude, T, P          | varies              | `fluids.atmosphere.ATMOSPHERE_1976`, `fluids.atmosphere.solar_position`, etc. |

### fluids.compressible
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Isothermal/polytropic compression | Compressor work, pressure, temperature, efficiency | P1, P2, T, k, eta, n, Z              | J/mol, K, etc.      | `fluids.compressible.isothermal_work_compression`, `fluids.compressible.isentropic_work_compression`, `fluids.compressible.isothermal_gas`, etc. |
| Gas pipeline sizing            | Sizing and pressure drop for gas pipelines          | rho, fd, P1, P2, L, D, m              | kg/s, Pa, m         | `fluids.compressible.isothermal_gas`, `fluids.compressible.Panhandle_A`, etc. |

### fluids.control_valve
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Control valve sizing           | Valve flow coefficient (Cv/Kv) and sizing           | Q, ΔP, rho, D, valve data             | Cv, Kv, dimensionless | `fluids.control_valve.size_control_valve_l`, `fluids.control_valve.size_control_valve_g` |

### fluids.core
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Reynolds number                | Calculate Reynolds number for flow                  | D, V, rho, mu or nu                   | dimensionless       | `fluids.core.Reynolds`                  |
| Dimensionless numbers          | Prandtl, Nusselt, Biot, Bond, Capillary, etc.       | varies                                | dimensionless       | `fluids.core.*`                         |
| Loss coefficient conversions   | Convert K, L/D, f, head, dP                         | K, L, D, fd, V, rho                   | varies              | `fluids.core.K_from_f`, `fluids.core.dP_from_K`, etc. |

### fluids.drag
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Drag coefficient               | Drag on particles/spheres                          | Re, shape, D, rho, mu                 | dimensionless       | `fluids.drag.drag_sphere`, `fluids.drag.drag_coefficient` |
| Terminal velocity              | Terminal settling velocity of particles             | D, rhop, rho, mu, g                   | m/s                 | `fluids.drag.v_terminal`                |

### fluids.filters
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Filter pressure drop           | Pressure drop across filters/screens/grills         | filter type, V, rho                   | Pa                   | `fluids.filters.round_edge_screen`, `fluids.filters.square_edge_grill`, etc. |

### fluids.fittings
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Pressure drop (fittings)       | Pressure drop across fittings/valves                | K, V, rho                             | Pa                  | `fluids.core.dP_from_K`, `fluids.fittings.*`    |
| Valve loss coefficients        | K, Cv, Kv conversions, valve types                  | D, K, Cv, Kv                          | varies              | `fluids.fittings.K_to_Cv`, `fluids.fittings.Cv_to_K`, etc. |

### fluids.flow_meter
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Orifice flow                   | Flow rate or pressure drop across orifice           | D, d, ΔP, rho, C                      | m³/s, Pa            | `fluids.flow_meter.dP_orifice`, `fluids.flow_meter.orifice_expansibility` |
| Venturi/Nozzle flow            | Flow rate or pressure drop across venturi/nozzle    | D, d, ΔP, rho, C                      | m³/s, Pa            | `fluids.flow_meter.dP_venturi_tube`, `fluids.flow_meter.nozzle_expansibility` |
| Flow meter (cone, wedge, etc.) | Flow rate/ΔP for cone, wedge, and other meters      | D, d, ΔP, rho, C                      | m³/s, Pa            | `fluids.flow_meter.dP_cone_meter`, `fluids.flow_meter.dP_wedge_meter` |

### fluids.friction
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Friction factor                | Darcy friction factor (various correlations)        | Re, e/D                               | dimensionless       | `fluids.friction.friction_factor`       |

### fluids.geometry
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Tank geometry                  | Volume, surface area, and level for tanks           | D, L, head type, h                    | m³, m², m           | `fluids.geometry.TANK`                  |

### fluids.jet_pump
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Jet pump/eductor sizing        | Jet pump (eductor/ejector) performance              | fluid, geometry, flow                 | efficiency, flow     | `fluids.jet_pump.liquid_jet_pump`       |

### fluids.mixing
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Mixing calculations            | Mixer/agitator sizing, mixing time, K values        | mixer/geometry/fluid params           | varies               | `fluids.mixing.size_tee`, `fluids.mixing.agitator_time_homogeneous`, etc. |

### fluids.open_flow
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Open channel flow              | Manning/Chezy/weir equations for open channel       | n, S, A, R, weir params               | m³/s                | `fluids.open_flow.Manning`, `fluids.open_flow.Chezy`, `fluids.open_flow.Q_weir_rectangular_Kindsvater_Carter`, etc. |

### fluids.packed_bed
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Packed bed pressure drop       | Pressure drop through packed bed                    | dp, voidage, vs, rho, mu, L, Dt       | Pa                  | `fluids.packed_bed.dP_packed_bed`, `fluids.packed_bed.Ergun`, etc. |

### fluids.packed_tower
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Packed tower/demister          | Pressure drop, flooding, separation efficiency      | packing/demister params               | varies               | `fluids.packed_tower.Stichlmair_dry`, `fluids.packed_tower.dP_demister_dry_Setekleiv_Svendsen`, etc. |

### fluids.particle_size_distribution
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Particle size distribution     | Mean, D10, D50, D90, Sauter mean diameter, etc.     | ds, fractions                         | μm, mm, m           | `fluids.particle_size_distribution.ParticleSizeDistribution` |

### fluids.piping
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Pipe schedules/gauges          | Lookup pipe size, wall thickness, gauge conversion  | NPS, schedule, gauge                  | mm, in, etc.         | `fluids.piping.nearest_pipe`, `fluids.piping.gauge_from_t`, `fluids.piping.t_from_gauge` |

### fluids.pump
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Pump power                     | Calculate required pump power                       | Q, ΔP, η                              | W                   | (user formula), `fluids.pump.Corripio_pump_efficiency` |
| Pump/motor efficiency          | Estimate pump/motor/VFD efficiency                  | Power, load, type                     | %/fraction           | `fluids.pump.CSA_motor_efficiency`, `fluids.pump.motor_efficiency_underloaded`, `fluids.pump.VFD_efficiency` |

### fluids.safety_valve
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Safety/relief valve sizing     | Sizing/rating of safety/relief valves               | fluid, P, T, valve data               | area, flow, etc.     | `fluids.safety_valve.API520_A_g`, `fluids.safety_valve.API520_A_l`, etc. |

### fluids.separator
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Separator sizing               | Vapor-liquid separator sizing                       | fluid, flow, separator params         | velocity, K, etc.    | `fluids.separator.v_Sounders_Brown`, `fluids.separator.K_separator_Watkins` |

### fluids.two_phase, fluids.two_phase_voidage
| Function Name                  | Description                                         | Typical Inputs                        | Output Units         | fluids API Function(s)                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------|
| Two-phase flow                 | Pressure drop, flow regime, void fraction           | fluid/pipe params, phase info         | varies               | `fluids.two_phase.two_phase_dP`, `fluids.two_phase_voidage.void_fraction` |

---

## Notes
- All functions should include robust error handling for invalid inputs and missing data.
- Where possible, support both SI and common engineering units.
- Functions should be documented with clear argument tables and practical Excel usage examples.
- Advanced features (e.g., property plots, system curve generation, pump selection) could be added as separate functions.

---

## References
- [fluids documentation](https://fluids.readthedocs.io/)
- [fluids GitHub repository](https://github.com/CalebBell/fluids)

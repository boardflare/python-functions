# Fluids Python Package Modules Checklist

- [x] [Atmospheric properties (fluids.atmosphere)](https://fluids.readthedocs.io/fluids.atmosphere.html)
- [x] [Compressible flow and compressor sizing (fluids.compressible)](https://fluids.readthedocs.io/fluids.compressible.html)
- [x] [Control valve sizing and rating (fluids.control_valve)](https://fluids.readthedocs.io/fluids.control_valve.html)
- [ ] [Dimensionless numbers (fluids.core)](https://fluids.readthedocs.io/fluids.core.html)
- [ ] [Drag and terminal velocity (fluids.drag)](https://fluids.readthedocs.io/fluids.drag.html)
- [ ] [Filter pressure drop (fluids.filters)](https://fluids.readthedocs.io/fluids.filters.html)
- [ ] [Fittings pressure drop (fluids.fittings)](https://fluids.readthedocs.io/fluids.fittings.html)
- [ ] [Orifice plates, flow nozzles, Venturi tubes, cone and wedge meters (fluids.flow_meter)](https://fluids.readthedocs.io/fluids.flow_meter.html)
- [ ] [Friction factor and pipe roughness (fluids.friction)](https://fluids.readthedocs.io/fluids.friction.html)
- [ ] [Tank and Heat Exchanger Design (fluids.geometry)](https://fluids.readthedocs.io/fluids.geometry.html)
- [ ] [Jet Pump (ejector/eductor) Sizing and Rating (fluids.jet_pump)](https://fluids.readthedocs.io/fluids.jet_pump.html)
- [ ] [Mixing (fluids.mixing)](https://fluids.readthedocs.io/fluids.mixing.html)
- [ ] [Support for Numba (fluids.numba)](https://fluids.readthedocs.io/fluids.numba.html)
- [ ] [Hydrology, weirs and open flow (fluids.open_flow)](https://fluids.readthedocs.io/fluids.open_flow.html)
- [ ] [Packed bed pressure drop (fluids.packed_bed)](https://fluids.readthedocs.io/fluids.packed_bed.html)
- [ ] [Packing & demister pressure drop (fluids.packed_tower)](https://fluids.readthedocs.io/fluids.packed_tower.html)
- [ ] [Particle Size Distributions (fluids.particle_size_distribution)](https://fluids.readthedocs.io/fluids.particle_size_distribution.html)
- [ ] [Pipe schedules (fluids.piping)](https://fluids.readthedocs.io/fluids.piping.html)
- [ ] [Pump and motor sizing (fluids.pump)](https://fluids.readthedocs.io/fluids.pump.html)
- [ ] [Safety/relief valve sizing (fluids.safety_valve)](https://fluids.readthedocs.io/fluids.safety_valve.html)
- [ ] [Liquid-Vapor Separators (fluids.separator)](https://fluids.readthedocs.io/fluids.separator.html)
- [ ] [Pneumatic conveying (fluids.saltation)](https://fluids.readthedocs.io/fluids.saltation.html)
- [ ] [Two phase flow (fluids.two_phase)](https://fluids.readthedocs.io/fluids.two_phase.html)
- [ ] [Two-phase flow voidage (fluids.two_phase_voidage)](https://fluids.readthedocs.io/fluids.two_phase_voidage.html)
- [ ] [Support for pint Quantities (fluids.units)](https://fluids.readthedocs.io/fluids.units.html)
- [ ] [Support for NumPy arrays (fluids.vectorized)](https://fluids.readthedocs.io/fluids.vectorized.html)

---

## FLUIDS_ATMOSPHERE
**Description:** Computes atmospheric properties and solar calculations using various models.

**Parameters:**
- `method`: Calculation type (e.g., "ATMOSPHERE_1976", "NRLMSISE00", "solar_position", "solar_irradiation", "sunrise_sunset").
- Additional parameters depend on the method, such as:
  - For "ATMOSPHERE_1976": `Z` (elevation, m), `dT` (temperature offset, K)
  - For "NRLMSISE00": `Z`, `latitude`, `longitude`, `day`, `seconds`, `f107`, `f107_avg`, `geomagnetic_disturbance_indices`
  - For "solar_position": `moment`, `latitude`, `longitude`, `Z`, `T`, `P`, `atmos_refract`
  - For "solar_irradiation": `latitude`, `longitude`, `Z`, `moment`, `surface_tilt`, `surface_azimuth`, `T`, `P`, `solar_constant`, `atmos_refract`, `albedo`, `linke_turbidity`, etc.
- See [module docs](https://fluids.readthedocs.io/fluids.atmosphere.html) for full details.

**Returns:** Atmospheric properties (pressure, temperature, density, etc.), solar position, or solar radiation values depending on method.

---

## FLUIDS_COMPRESSIBLE
**Description:** Performs compressible flow and compressor sizing calculations, including isothermal/isentropic work, gas pipeline sizing, empirical equations, and choked flow.

**Parameters:**
- `method`: Calculation type (e.g., "isothermal_work_compression", "isentropic_work_compression", "isothermal_gas", "Panhandle_A", "Weymouth", "T_critical_flow", etc.)
- Additional parameters depend on the method, such as:
  - For work calculations: `P1`, `P2`, `T`, `k`, `Z`, `eta`, etc.
  - For pipeline sizing: `rho`, `fd`, `P1`, `P2`, `L`, `D`, `m`, `SG`, `Tavg`, `Q`, etc.
  - For choked/critical flow: `T`, `P`, `k`, etc.
- See [module docs](https://fluids.readthedocs.io/fluids.compressible.html) for full details.

**Returns:** Work, pressures, temperatures, flow rates, or other compressible flow properties depending on method.

---

## FLUIDS_CONTROL_VALVE
**Description:** Sizes and rates control valves for liquid and gas flow, including calculation of flow coefficients, choked flow, noise, and valve characteristics.

**Parameters:**
- `method`: Calculation type (e.g., "size_control_valve_l", "size_control_valve_g", "FF_critical_pressure_ratio_l", "is_choked_turbulent_l", "control_valve_noise_l_2015", etc.)
- Additional parameters depend on the method, such as:
  - For liquid valve sizing: `rho`, `Psat`, `Pc`, `mu`, `P1`, `P2`, `Q`, `D1`, `D2`, `d`, `FL`, `Fd`, etc.
  - For gas valve sizing: `T`, `MW`, `mu`, `gamma`, `Z`, `P1`, `P2`, `Q`, `D1`, `D2`, `d`, `FL`, `Fd`, `xT`, etc.
  - For noise calculations: `m`, `P1`, `P2`, `Psat`, `rho`, `c`, `Kv`, `d`, `Di`, `FL`, `Fd`, `t_pipe`, etc.
- See [module docs](https://fluids.readthedocs.io/fluids.control_valve.html) for full details.

**Returns:** Valve flow coefficients, choked flow status, noise levels, or other control valve properties depending on method.

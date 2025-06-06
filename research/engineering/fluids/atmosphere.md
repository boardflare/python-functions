# Atmospheric properties (fluids.atmosphere)

This module contains models of earth’s atmosphere. Models are empirical and based on extensive research, primarily by NASA.

For reporting bugs, adding feature requests, or submitting pull requests, please use the [GitHub issue tracker](https://github.com/CalebBell/fluids/) or contact the author at Caleb.Andrew.Bell@gmail.com.

## Atmospheres

### fluids.atmosphere.ATMOSPHERE_1976(Z, dT=0.0)
US Standard Atmosphere 1976 class, which calculates T, P, rho, v_sonic, mu, k, and g as a function of altitude above sea level. Designed to provide reasonable results up to an elevation of 86,000 m (0.4 Pa). The model is also valid under sea level, to -610 meters.

**Parameters:**
- **Z**: Elevation, [m]
- **dT**: Temperature difference from standard conditions used in determining the properties of the atmosphere, [K] (optional)

**Notes:**
- Up to 32 km, the International Standard Atmosphere (ISA) and World Meteorological Organization (WMO) standard atmosphere are identical.
- This is a revision of the US 1962 atmosphere.

**References:**
1. NOAA, NASA, and USAF. “U.S. Standard Atmosphere, 1976” October 15, 1976. http://ntrs.nasa.gov/search.jsp?R=19770009539
2. “ISO 2533:1975 - Standard Atmosphere.” ISO. http://www.iso.org/iso/catalogue_detail.htm?csnumber=7472
3. Yager, Robert J. “Calculating Atmospheric Conditions (Temperature, Pressure, Air Density, and Speed of Sound) Using C++,” June 2013. http://www.dtic.mil/cgi-bin/GetTRDoc?AD=ADA588839

**Examples:**
```python
five_km = ATMOSPHERE_1976(5000)
five_km.P, five_km.rho, five_km.mu
# (54048.28614576141, 0.7364284207799743, 1.628248135362207e-05)
five_km.k, five_km.g, five_km.v_sonic
# (0.02273190295142526, 9.791241076982665, 320.5455196704035)
```

**Attributes:**
- **T**: Temperature of atmosphere at specified conditions, [K]
- **P**: Pressure of atmosphere at specified conditions, [Pa]
- **rho**: Mass density of atmosphere at specified conditions [kg/m^3]
- **H**: Geopotential height, [m]
- **g**: Acceleration due to gravity, [m/s^2]
- **mu**: Viscosity of atmosphere at specified conditions, [Pa*s]
- **k**: Thermal conductivity of atmosphere at specified conditions, [W/m/K]
- **v_sonic**: Speed of sound of atmosphere at specified conditions, [m/s]

**Methods:**
- **density(T, P)**: Method defined in the US Standard Atmosphere 1976 for calculating density of air as a function of T and P. MW is defined as 28.9644 g/mol, and R as 8314.32 J/kmol/K

  $\rho_g = \frac{P \cdot MW}{T \cdot R \cdot 1000}$

- **gravity(Z)**: Method defined in the US Standard Atmosphere 1976 for calculating the gravitational acceleration above earth as a function of elevation only.

  $g = g_0 \left(\frac{r_0}{r_0 + Z}\right)^2$

- **pressure_integral(T1, P1, dH)**: Method to compute an integral of the pressure differential of an elevation difference with a base elevation defined by temperature T1 and pressure P1.

- **sonic_velocity(T)**: Method defined in the US Standard Atmosphere 1976 for calculating the speed of sound in air as a function of T only.

  $c = (\gamma R T / MW)^{0.5}$

- **thermal_conductivity(T)**: Method defined in the US Standard Atmosphere 1976 for calculating thermal conductivity of air as a function of T only.

  $k_g = 2.64638 \times 10^{-3} \frac{T^{1.5}}{T + 245.4 \cdot 10^{-12}/T}$

- **viscosity(T)**: Method defined in the US Standard Atmosphere 1976 for calculating viscosity of air as a function of T only.

  $\mu_g = 1.458 \times 10^{-6} \frac{T^{1.5}}{T + 110.4}$

---

### fluids.atmosphere.ATMOSPHERE_NRLMSISE00(Z, latitude=0.0, longitude=0.0, day=0, seconds=0.0, f107=150.0, f107_avg=150.0, geomagnetic_disturbance_indices=None)
NRLMSISE 00 model for calculating temperature and density of gases in the atmosphere, from ground level to 1000 km, as a function of time of year, longitude and latitude, solar activity and earth’s geomagnetic disturbance.

NRLMSISE stands for the US Naval Research Laboratory Mass Spectrometer and Incoherent Scatter Radar Exosphere model, released in 2001.

**Parameters:**
- **Z**: Elevation, [m]
- **latitude**: Latitude, between -90 and 90 [degrees] (optional)
- **longitude**: Longitude, between -180 and 180 or 0 and 360, [degrees] (optional)
- **day**: Day of year, 0-366 [day] (optional)
- **seconds**: Seconds since start of day, in UT1 time; using UTC provides no loss in accuracy [s] (optional)
- **f107**: Daily average 10.7 cm solar flux measurement [10^-22 W/m^2/Hz] (optional)
- **f107_avg**: 81-day sfu average [10^-22 W/m^2/Hz] (optional)
- **geomagnetic_disturbance_indices**: List of the 7 Ap indexes (optional)

**Notes:**
- No full description has been published of this model; it has been defined by its implementation only. It was written in FORTRAN, and is accessible at ftp://hanna.ccmc.gsfc.nasa.gov/pub/modelweb/atmospheric/msis/nrlmsise00/
- A C port of the model by Dominik Brodowski is available at http://www.brodo.de/space/nrlmsise/
- In 2013 Joshua Milas ported the C port to Python. This is an interface to his port.
- This model is based on measurements other than gravity; it does not provide a calculation method for g. It does not provide transport properties.
- This model takes on the order of ~2 ms.

**References:**
1. Picone, J. M., A. E. Hedin, D. P. Drob, and A. C. Aikin. “NRLMSISE-00 Empirical Model of the Atmosphere: Statistical Comparisons and Scientific Issues.” Journal of Geophysical Research: Space Physics 107, no. A12 (December 1, 2002): 1468. doi:10.1029/2002JA009430.
2. Tapping, K. F. “The 10.7 Cm Solar Radio Flux (F10.7).” Space Weather 11, no. 7 (July 1, 2013): 394-406. doi:10.1002/swe.20064.
3. Natalia Papitashvili. “NRLMSISE-00 Atmosphere Model.” http://ccmc.gsfc.nasa.gov/modelweb/models/nrlmsise00.php

**Examples:**
```python
atmosphere = ATMOSPHERE_NRLMSISE00(1E3, 45, 45, 150)
atmosphere.T, atmosphere.rho
# (285.5440860623, 1.10190620264)
```

**Attributes:**
- **rho**: Mass density [kg/m^3]
- **T**: Temperature, [K]
- **P**: Pressure, calculated with ideal gas law [Pa]
- **He_density**: Density of helium atoms [count/m^3]
- **O_density**: Density of monatomic oxygen [count/m^3]
- **N2_density**: Density of nitrogen molecules [count/m^3]
- **O2_density**: Density of oxygen molecules [count/m^3]
- **Ar_density**: Density of Argon atoms [count/m^3]
- **H_density**: Density of hydrogen atoms [count/m^3]
- **N_density**: Density of monatomic nitrogen [count/m^3]
- **O_anomalous_density**: Density of anomalous oxygen [count/m^3]
- **particle_density**: Total density of molecules [count/m^3]
- **components**: List of species making up the atmosphere [-]
- **zs**: Mole fractions of each molecule in the atmosphere, in order of components [-]

---

### fluids.atmosphere.airmass(func, angle, H_max=86400.0, R_planet=6371229.0, RI=1.000276)
Calculates mass of air per square meter in the atmosphere using a provided atmospheric model. The lowest air mass is calculated straight up; as the angle is lowered to nearer and nearer the horizon, the air mass increases, and can approach 40x or more the minimum airmass.

  $m(\gamma) = \int_0^\infty \rho \left\{1 - \left[1 + 2(RI-1)(1-\rho/\rho_0)\right][\cos\gamma(1+h/R)]^2\right\}^{-1/2} dH$

**Parameters:**
- **func**: Function which returns the density of the atmosphere as a function of elevation
- **angle**: Degrees above the horizon (90 = straight up), [degrees]
- **H_max**: Maximum height to compute the integration up to before the contribution of density becomes negligible, [m] (optional)
- **R_planet**: The radius of the planet for which the integration is being performed, [m] (optional)
- **RI**: The refractive index of the atmosphere (air on earth at 0.7 um as default) assumed a constant, [-] (optional)

**Returns:**
- **m**: Mass of air per square meter in the atmosphere, [kg/m^2]

**Notes:**
- Numerical integration via SciPy’s quad is used to perform the calculation.

**References:**
1. Kasten, Fritz, and Andrew T. Young. “Revised Optical Air Mass Tables and Approximation Formula.” Applied Optics 28, no. 22 (November 15, 1989): 4735-38. https://doi.org/10.1364/AO.28.004735.

**Examples:**
```python
airmass(lambda Z : ATMOSPHERE_1976(Z).rho, 90)
# 10356.12
```

---

## Solar Radiation and Position

### fluids.atmosphere.solar_position(moment, latitude, longitude, Z=0.0, T=298.15, P=101325.0, atmos_refract=0.5667)
Calculate the position of the sun in the sky. It is defined in terms of two angles - the zenith and the azimuth. The azimuth tells where a sundial would see the sun as coming from; the zenith tells how high in the sky it is. The solar elevation angle is returned for convenience; it is the complimentary angle of the zenith.

The sun’s refraction changes how high it appears as though the sun is; so values are returned with an optional conversion to the apparent angle. This impacts only the zenith/elevation.

Uses the Reda and Andreas (2004) model described in [1], originally incorporated into the excellent [pvlib library](https://github.com/pvlib/pvlib-python)

**Parameters:**
- **moment**: Time and date for the calculation, in UTC time OR in the time zone of the latitude/longitude specified BUT WITH A TZINFO ATTACHED! [-]
- **latitude**: Latitude, between -90 and 90 [degrees]
- **longitude**: Longitude, between -180 and 180, [degrees]
- **Z**: Elevation above sea level for the solar position calculation, [m] (optional)
- **T**: Temperature of atmosphere at ground level, [K] (optional)
- **P**: Pressure of atmosphere at ground level, [Pa] (optional)
- **atmos_refract**: Atmospheric refractivity, [degrees] (optional)

**Returns:**
- **apparent_zenith**: Zenith of the sun as observed from the ground based after accounting for atmospheric refraction, [degrees]
- **zenith**: Actual zenith of the sun (ignores atmospheric refraction), [degrees]
- **apparent_altitude**: Altitude of the sun as observed from the ground based after accounting for atmospheric refraction, [degrees]
- **altitude**: Actual altitude of the sun (ignores atmospheric refraction), [degrees]
- **azimuth**: The azimuth of the sun, [degrees]
- **equation_of_time**: Equation of time - the number of seconds to be added to the day’s mean solar time to obtain the apparent solar noon time, [seconds]

**Notes:**
- The solar altitude angle is defined as 90° - zenith. The elevation angle is just another name for the altitude angle.
- The azimuth is the angle in degrees that the sun is East of the North angle. It is positive North eastwards 0° to 360°.
- Due to differences in atmospheric refractivity, estimation of sunset and sunrise are accurate to no more than one minute.

**References:**
1. Reda, Ibrahim, and Afshin Andreas. “Solar Position Algorithm for Solar Radiation Applications.” Solar Energy 76, no. 5 (January 1, 2004): 577-89. https://doi.org/10.1016/j.solener.2003.12.003.
2. “Navigation - What Azimuth Description Systems Are in Use? - Astronomy Stack Exchange.” https://astronomy.stackexchange.com/questions/237/what-azimuth-description-systems-are-in-use?rq=1

**Examples:**
```python
import pytz
from datetime import datetime, timedelta
# Perth, Australia - sunrise
solar_position(pytz.timezone('Australia/Perth').localize(datetime(2020, 6, 6, 7, 10, 57)), -31.95265, 115.85742)
# [90.89617025931, 90.89617025931, -0.896170259317, -0.896170259317, 63.6016017691, 79.0711232143]

# Perth, Australia - Comparing against an online source
solar_position(pytz.timezone('Australia/Perth').localize(datetime(2020, 6, 6, 14, 30, 0)), -31.95265, 115.85742)
# [63.4080568623, 63.4400018158, 26.59194313766, 26.55999818417, 325.121376246, 75.7467475485]

# Perth, Australia - time input without timezone; must be converted by user to UTC!
solar_position(datetime(2020, 6, 6, 14, 30, 0) - timedelta(hours=8), -31.95265, 115.85742)
# [63.4080568623, 63.4400018158, 26.59194313766, 26.55999818417, 325.121376246, 75.7467475485]

# Sunrise occurs when the zenith is 90 degrees (Calgary, AB):
local_time = datetime(2018, 4, 15, 6, 43, 5)
local_time = pytz.timezone('America/Edmonton').localize(local_time)
solar_position(local_time, 51.0486, -114.07)[0]
# 90.0005468548

# Sunset occurs when the zenith is 90 degrees (13.5 hours later in this case):
solar_position(pytz.timezone('America/Edmonton').localize(datetime(2018, 4, 15, 20, 30, 28)), 51.0486, -114.07)
# [89.999569566, 90.5410381216, 0.000430433876, -0.541038121618, 286.831378190, 6.63142952587]
```

---

### fluids.atmosphere.solar_irradiation(latitude, longitude, Z, moment, surface_tilt, surface_azimuth, T=None, P=None, solar_constant=1366.1, atmos_refract=0.5667, albedo=0.25, linke_turbidity=None, extraradiation_method='spencer', airmass_model='kastenyoung1989', cache=None)
Calculates the amount of solar radiation and radiation reflected back the atmosphere which hits a surface at a specified tilt, and facing a specified azimuth.

This function is a wrapper for the [pvlib library](https://github.com/pvlib/pvlib-python), and requires it to be installed.

**Parameters:**
- **latitude**: Latitude, between -90 and 90 [degrees]
- **longitude**: Longitude, between -180 and 180, [degrees]
- **Z**: Elevation above sea level for the position, [m] (optional)
- **moment**: Time and date for the calculation, in UTC time OR in the time zone of the latitude/longitude specified BUT WITH A TZINFO ATTACHED! [-]
- **surface_tilt**: The angle above the horizontal of the object being hit by radiation, [degrees]
- **surface_azimuth**: The angle the object is facing (positive, North eastwards 0° to 360°), [degrees]
- **T**: Temperature of atmosphere at ground level, [K] (optional)
- **P**: Pressure of atmosphere at ground level, [Pa] (optional)
- **solar_constant**: The amount of solar radiation which reaches earth’s disk (at a standardized distance of 1 AU), [W/m^2] (optional)
- **atmos_refract**: Atmospheric refractivity at sunrise/sunset, [degrees] (optional)
- **albedo**: The average amount of reflection of the terrain surrounding the object at quite a distance, [-] (optional)
- **linke_turbidity**: The amount of pollution/water in the sky versus a perfect clear sky, [-] (optional)
- **extraradiation_method**: The specified method to calculate the effect of earth’s position on the amount of radiation which reaches earth according to the methods available in the pvlib library, [-] (optional)
- **airmass_model**: The specified method to calculate the amount of air the sunlight needs to travel through to reach the earth according to the methods available in the pvlib library, [-] (optional)
- **cache**: Dictionary to check for values to use to skip some calculations; apparent_zenith, zenith, azimuth supported, [-] (optional)

**Returns:**
- **poa_global**: The total irradiance in the plane of the surface, [W/m^2]
- **poa_direct**: The total beam irradiance in the plane of the surface, [W/m^2]
- **poa_diffuse**: The total diffuse irradiance in the plane of the surface, [W/m^2]
- **poa_sky_diffuse**: The sky component of the diffuse irradiance, excluding the impact from the ground, [W/m^2]
- **poa_ground_diffuse**: The ground-sky diffuse irradiance component, [W/m^2]

**Notes:**
- The retrieval of linke_turbidity requires the pytables library (and Pandas); if it is not installed, specify a value of linke_turbidity to avoid the dependency.
- There is some redundancy of the calculated results:
  - poa_diffuse = poa_ground_diffuse + poa_sky_diffuse
  - poa_global = poa_direct + poa_diffuse
- For a surface such as a pipe or vessel, an approach would be to split it into a number of rectangles and sum up the radiation absorbed by each.
- This calculation is fairly slow.

**References:**
1. Will Holmgren, Calama-Consulting, Tony Lorenzo, Uwe Krien, bmu, DaCoEx, mayudong, et al. Pvlib/Pvlib-Python: 0.5.1. Zenodo, 2017. https://doi.org/10.5281/zenodo.1016425.

**Examples:**
```python
import pytz
from datetime import datetime
solar_irradiation(Z=1100.0, latitude=51.0486, longitude=-114.07, linke_turbidity=3,
    moment=pytz.timezone('America/Edmonton').localize(datetime(2018, 4, 15, 13, 43, 5)), surface_tilt=41.0,
    surface_azimuth=180.0)
# (1065.7621896280, 945.2656564506, 120.49653317744, 95.31535344213, 25.181179735317)

cache = {'apparent_zenith': 41.099082295767545, 'zenith': 41.11285376417578, 'azimuth': 182.5631874250523}
solar_irradiation(Z=1100.0, latitude=51.0486, longitude=-114.07,
    moment=pytz.timezone('America/Edmonton').localize(datetime(2018, 4, 15, 13, 43, 5)), surface_tilt=41.0,
    linke_turbidity=3, T=300, P=1E5,
    surface_azimuth=180.0, cache=cache)
# (1042.567770367, 918.237754854, 124.3300155131, 99.622865737, 24.7071497753)

# At night, there is no solar radiation and this function returns zeros:
solar_irradiation(Z=1100.0, latitude=51.0486, longitude=-114.07, linke_turbidity=3,
    moment=pytz.timezone('America/Edmonton').localize(datetime(2018, 4, 15, 2, 43, 5)), surface_tilt=41.0,
    surface_azimuth=180.0)
# (0.0, -0.0, 0.0, 0.0, 0.0)
```

---

### fluids.atmosphere.sunrise_sunset(moment, latitude, longitude)
Calculates the times at which the sun is at sunset; sunrise; and halfway between sunrise and sunset (transit).

Uses the Reda and Andreas (2004) model described in [1], originally incorporated into the [pvlib library](https://github.com/pvlib/pvlib-python)

**Parameters:**
- **moment**: Date for the calculation; needs to contain only the year, month, and day; if it is timezone-aware, the return values will be localized to this timezone [-]
- **latitude**: Latitude, between -90 and 90 [degrees]
- **longitude**: Longitude, between -180 and 180, [degrees]

**Returns:**
- **sunrise**: The time at the specified day when the sun rises IN UTC IF MOMENT DOES NOT HAVE A TIMEZONE, OTHERWISE THE TIMEZONE GIVEN WITH IT, [-]
- **sunset**: The time at the specified day when the sun sets IN UTC IF MOMENT DOES NOT HAVE A TIMEZONE, OTHERWISE THE TIMEZONE GIVEN WITH IT, [-]
- **transit**: The time at the specified day when the sun is at solar noon - halfway between sunrise and sunset IN UTC IF MOMENT DOES NOT HAVE A TIMEZONE, OTHERWISE THE TIMEZONE GIVEN WITH IT, [-]

**Notes:**
- This function takes on the order of 2 ms per calculation.

**References:**
1. Reda, Ibrahim, and Afshin Andreas. “Solar Position Algorithm for Solar Radiation Applications.” Solar Energy 76, no. 5 (January 1, 2004): 577-89. https://doi.org/10.1016/j.solener.2003.12.003.

**Examples:**
```python
sunrise, sunset, transit = sunrise_sunset(datetime(2018, 4, 17), 51.0486, -114.07)
sunrise
# datetime.datetime(2018, 4, 17, 12, 36, 55, 782660)
sunset
# datetime.datetime(2018, 4, 18, 2, 34, 4, 249326)
transit
# datetime.datetime(2018, 4, 17, 19, 35, 46, 686265)

import pytz
sunrise_sunset(pytz.timezone('America/Edmonton').localize(datetime(2018, 4, 17)), 51.0486, -114.07)
# (datetime.datetime(2018, 4, 16, 6, 39, 1, 570479, tzinfo=<DstTzInfo 'America/Edmonton' MDT-1 day, 18:00:00 DST>),
#  datetime.datetime(2018, 4, 16, 20, 32, 25, 778162, tzinfo=<DstTzInfo 'America/Edmonton' MDT-1 day, 18:00:00 DST>),
#  datetime.datetime(2018, 4, 16, 13, 36, 0, 386341, tzinfo=<DstTzInfo 'America/Edmonton' MDT-1 day, 18:00:00 DST>))
```

---

### fluids.atmosphere.earthsun_distance(moment)
Calculates the distance between the earth and the sun as a function of date and time. Uses the Reda and Andreas (2004) model described in [1], originally incorporated into the [pvlib library](https://github.com/pvlib/pvlib-python)

**Parameters:**
- **moment**: Time and date for the calculation, in UTC time (or GMT, which is almost the same thing); OR a timezone-aware datetime instance which will be internally converted to UTC, [-]

**Returns:**
- **distance**: Distance between the center of the earth and the center of the sun, [m]

**Notes:**
- This function is quite accurate. The difference comes from the impact of the moon.
- Note this function is not continuous; the sun-earth distance is not sufficiently accurately modeled for the change to be continuous throughout each day.

**References:**
1. Reda, Ibrahim, and Afshin Andreas. “Solar Position Algorithm for Solar Radiation Applications.” Solar Energy 76, no. 5 (January 1, 2004): 577-89. https://doi.org/10.1016/j.solener.2003.12.003.

**Examples:**
```python
from datetime import datetime, timedelta
earthsun_distance(datetime(2003, 10, 17, 13, 30, 30))
# 149090925951.18338

earthsun_distance(datetime(2013, 1, 2, 4, 21, 50))
# 147098089490.67123

earthsun_distance(datetime(2013, 7, 5, 14, 44, 51, 0))
# 152097354414.36044

import pytz
earthsun_distance(pytz.timezone('America/Edmonton').localize(datetime(2020, 6, 6, 10, 0, 0, 0)))
# 151817805599.67142

earthsun_distance(datetime(2020, 6, 6, 10, 0, 0, 0))
# 151812898579.44104
```

---

## Additional Links
- [index](https://fluids.readthedocs.io/genindex.html) - General Index
- [modules](https://fluids.readthedocs.io/py-modindex.html) - Python Module Index
- [next](https://fluids.readthedocs.io/fluids.compressible.html) - Compressible flow and compressor sizing (fluids.compressible)
- [previous](https://fluids.readthedocs.io/fluids.html) - <no title>
- [Fluids 1.1.0 documentation](https://fluids.readthedocs.io/index.html)
- [API Reference](https://fluids.readthedocs.io/modules.html)
- [Atmospheric properties (fluids.atmosphere)](https://fluids.readthedocs.io/fluids.atmosphere.html)
- [Table of Contents](https://fluids.readthedocs.io/index.html)

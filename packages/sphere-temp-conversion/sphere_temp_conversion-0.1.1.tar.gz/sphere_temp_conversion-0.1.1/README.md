# Readme - sphere_temp_conversion

Provides functions for converting sample temperatures to setpoint temperatures and vice versa for the [Sphere Energy ASC-T All-solid-state battery testing device](https://www.sphere-energy.eu/solidstate-batteries).
Supports both the PEI and alumina (Al2O3) internal sleeve.
Maximum setpoint and sample temperatures are also accessible.

Not affiliated with Sphere Energy.

## Installation

    pip install sphere-temp-conversion

## Use

    import sphere_temp_conversion.converter as sphere
    
    sphere.get_max_setpoint(sphere.Material.PEI)
    sphere.get_max_sample_temp(sphere.Material.alumina)
    
    sphere.get_sample_temp_from_setpoint(100, sphere.Material.PEI)
    sphere.get_setpoint_from_sample_temp(100, sphere.Material.alumina)
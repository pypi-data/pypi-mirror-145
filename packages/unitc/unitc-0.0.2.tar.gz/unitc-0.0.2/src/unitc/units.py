""" Physical measurement units conversation module for Python 3.
"""
import numpy as np

G_ACCEL = 9.80665

length_dict = {'m': 1,
               'dm': 1e1,
               'cm': 1e2,
               'mm': 1e3,
               'μm': 1e6,
               'nm': 1e9,
               'pm': 1e12,
               'fm': 1e15,
               'am': 1e18,
               'zm': 1e21,
               'ym': 1e24,
               'dam': 1e-1,
               'hm': 1e-2,
               'km': 1e-3,
               'Mm': 1e-6,
               'Gm': 1e-9,
               'Tm': 1e-12,
               'Pm': 1e-15,
               'Em': 1e-18,
               'Zm': 1e-21,
               'Ym': 1e-24,
               'ft': 3.28084,
               'in': 39.37008,
               'NM': 5.399565e-4,
               'mi': 6.213712e-4}
mass_dict = {'kg': 1,
             'g': 1e3,
             'mg': 1e6,
             't': 1e-3,
             'lb': 2.204623,
             'oz': 35.27396}
time_dict = {'s': 1,
             'min': 1/60,
             'h': 1/3600}
acceleration_dict = {'m/s²': 1,
                     'ft/s²': length_dict['ft']}
angle_dict = {'rad': 1,
              'deg': np.pi/180}
area_dict = {'m²': 1,
             'dm²': length_dict['dm']**2,
             'cm²': length_dict['cm']**2,
             'mm²': length_dict['mm']**2,
             'μm²': length_dict['μm']**2,
             'nm²': length_dict['nm']**2,
             'pm²': length_dict['pm']**2,
             'fm²': length_dict['fm']**2,
             'am²': length_dict['am']**2,
             'zm²': length_dict['zm']**2,
             'ym²': length_dict['ym']**2,
             'dam²': length_dict['dam']**2,
             'hm²': length_dict['hm']**2,
             'km²': length_dict['km']**2,
             'Mm²': length_dict['Mm']**2,
             'Gm²': length_dict['Gm']**2,
             'Tm²': length_dict['Tm']**2,
             'Pm²': length_dict['Pm']**2,
             'Em²': length_dict['Em']**2,
             'Zm²': length_dict['Zm']**2,
             'Ym²': length_dict['Ym']**2,
             'ft²': length_dict['ft']**2,
             'in²': length_dict['in']**2,
             'NM²': length_dict['NM']**2,
             'mi²': length_dict['mi']**2}


density_dict = {'kg/m³': 1,
                'g/cm³': mass_dict['g']/length_dict['cm']**3,
                'lb/in³': mass_dict['lb']/length_dict['in']**3}
inertia_dict = {'kg·m²': 1,
                'lb·ft²': mass_dict['lb']/length_dict['ft']**3}
force_dict = {'N': 1,
              'kN': 1e-3,
              'lbf': mass_dict['lb']/G_ACCEL}
pressure_dict = {'Pa': 1,
                 'kPa': 1e-3,
                 'MPa': 1e-6,
                 'GPa': 1e-9,
                 'psi': 1.450377e-4,
                 'kpsi': 1.450377e-7,
                 'bar': 1e-5,
                 'atm': 9.869233e-6,
                 'mmHg': 7.500638e-3,
                 'lbf/ft²': force_dict['lbf']/length_dict['ft']**2}
power_dict = {'W': 1,
              'kW': 1e-3,
              'HP': 0.001341022}
second_moment_area_dict = {'m⁴': 1,
                           'cm⁴': length_dict['cm']**4,
                           'mm⁴': length_dict['mm']**4,
                           'ft⁴': length_dict['ft']**4,
                           'in⁴': length_dict['in']**4}
speed_dict = {'m/s': 1,
              'kt': length_dict['NM']/time_dict['h'],
              'km/h': length_dict['km']/time_dict['h']}
volume_dict = {'m³': 1,
               'dm³': length_dict['dm']**3,
               'cm³': length_dict['cm']**3,
               'mm³': length_dict['mm']**3,
               'μm³': length_dict['μm']**3,
               'nm³': length_dict['nm']**3,
               'pm³': length_dict['pm']**3,
               'fm³': length_dict['fm']**3,
               'am³': length_dict['am']**3,
               'zm³': length_dict['zm']**3,
               'ym³': length_dict['ym']**3,
               'dam³': length_dict['dam']**3,
               'hm³': length_dict['hm']**3,
               'km³': length_dict['km']**3,
               'Mm³': length_dict['Mm']**3,
               'Gm³': length_dict['Gm']**3,
               'Tm³': length_dict['Tm']**3,
               'Pm³': length_dict['Pm']**3,
               'Em³': length_dict['Em']**3,
               'Zm³': length_dict['Zm']**3,
               'Ym³': length_dict['Ym']**3,
               'l': 1 * 1e3,
               'dl': length_dict['dm']**3 * 1e3,
               'cl': length_dict['cm']**3 * 1e3,
               'ml': length_dict['mm']**3 * 1e3,
               'μl': length_dict['μm']**3 * 1e3,
               'nl': length_dict['nm']**3 * 1e3,
               'pl': length_dict['pm']**3 * 1e3,
               'fl': length_dict['fm']**3 * 1e3,
               'al': length_dict['am']**3 * 1e3,
               'zl': length_dict['zm']**3 * 1e3,
               'yl': length_dict['ym']**3 * 1e3,
               'dal': length_dict['dam']**3 * 1e3,
               'hl': length_dict['hm']**3 * 1e3,
               'kl': length_dict['km']**3 * 1e3,
               'Ml': length_dict['Mm']**3 * 1e3,
               'Gl': length_dict['Gm']**3 * 1e3,
               'Tl': length_dict['Tm']**3 * 1e3,
               'Pl': length_dict['Pm']**3 * 1e3,
               'El': length_dict['Em']**3 * 1e3,
               'Zl': length_dict['Zm']**3 * 1e3,
               'Yl': length_dict['Ym']**3 * 1e3,
               'ft³': length_dict['ft']**3,
               'in³': length_dict['in']**3,
               'NM³': length_dict['NM']**3,
               'mi³': length_dict['mi']**3,
               'gal': 264.172}


si_dicts = [acceleration_dict,
            angle_dict,
            area_dict,
            density_dict,
            force_dict,
            inertia_dict,
            length_dict,
            mass_dict,
            power_dict,
            pressure_dict,
            second_moment_area_dict,
            speed_dict,
            volume_dict]


def unit_conversion(value, from_unit=None, to_unit=None):
    """ Measurement units conversion.

    Using this function, `value` `from_unit` is converted to
    `new_value` `to_unit`. If one of the units is not provided, it is assumed
    to be an SI unit. If no units are provided, the same value is returned.

    Args:
        value (float, list, str or numpy.array): Value(s) to be converted. If
            given as a string, a unit can be specified.
        from_unit (str, optional): Unit of the input value(s).
        to_unit (str, optional): Unit the value(s) are converted to.

    Returns:
        float or numpy.ndarray: Converted value(s).

    Raises:
        ValueError: If given units are inconsistent, unknown or not compatible.
        NotImplementedError: Not implemented features.

    """
    if isinstance(value, (list)):
        value = np.array(value)
    elif isinstance(value, (str)):
        i_value, i_unit = value.split()
        if from_unit is not None and i_unit != from_unit:
            raise ValueError('Inconsistent units.')
        value = float(i_value)
        from_unit = i_unit

    if isinstance(value, (list, np.ndarray)):
        if isinstance(value[0], (str)):
            raise NotImplementedError('Conversion of a list of strings not yet'
                                      + ' implemented.')

    #
    if from_unit is None and to_unit is None:
        # If no units are provided, return same value
        return value

    if to_unit is None:
        # If only from_unit is provided, convert to SI units
        for dict_i in si_dicts:
            if from_unit in dict_i.keys():
                return value/dict_i[from_unit]
        raise ValueError(f"Unknown unit {from_unit}.")

    if from_unit is None:
        # If only to_unit is provided, assume that the input is given in SI
        # units
        for dict_i in si_dicts:
            if to_unit in dict_i.keys():
                return value*dict_i[to_unit]
        raise ValueError(f"Unknown unit {from_unit}.")

    # Check if from_unit and to_unit are in the same dict
    # and use it to calculate the new value
    for dict_i in si_dicts:
        if from_unit in dict_i.keys() and to_unit in dict_i.keys():
            return value*dict_i[to_unit]/dict_i[from_unit]
    raise ValueError(f'Units {from_unit} and {to_unit}' +
                     ' are not compatible.')

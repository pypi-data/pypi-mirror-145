import sys
import pint
from pint import UnitRegistry
from rocketunits.rocket_units import categoryD, convert_string, convert_value, \
                                 display_def_unitsD, display_unitsD, SI_unitsD
ureg = UnitRegistry()

new_cat = "Power"
def_units = 'hp'
si_units = 'kcal/s'
def_val =  1.0 * ureg( def_units )
print( '# Creating Unit Category for "%s"'%new_cat )
print( '# Read As: 1 default unit = conv_factor u_name units' )
print( 'create_category(       c_name="%s", def_units="%s" ) '%(new_cat, def_units)  )

unitL = set( [def_units, 'BTU/s', 'W', 'kW', 'MW', 'J/s', 'kJ/s', 'cal/s', 'kcal/s',  'ft*lbf/s', 
         'BTU/hr', 'J/hr', 'kJ/hr', 'cal/hr', 'kcal/hr', 'ft*lbf/hr'] )

max_len = max( [len(s) for s in unitL] )

convL = [ (def_val.to(s).magnitude, s) for s in unitL] 
convL.sort()
#print( convL )

S = 'add_units_to_category( c_name="%s", u_name="%s"%s, conv_factor=%s, offset=0.0 )'
for conval, units in convL:
    pad =  ' '*(max_len - len(units))
    print( S%(new_cat, units, pad, conval) )
    
print()
print( 'display_def_unitsD["%s"] = "%s"'%( new_cat, def_units ) )
    
print()
orderedL = [s for (_,s) in convL]
print( 'display_unitsD["%s"] = %s'%( new_cat, orderedL ) )

    
print()
print( 'SI_unitsD["%s"] = "%s"'%( new_cat, si_units ) )


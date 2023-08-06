import sys
import pint
from pint import UnitRegistry
from rocketunits.rocket_units import categoryD, convert_string, convert_value, \
                                 display_def_unitsD, display_unitsD, SI_unitsD
ureg = UnitRegistry()

new_cat = "HeatFlux"
def_units = 'BTU/in**2/s'
si_units = 'kcal/m**2/s'
def_val =  1.0 * ureg( def_units )
print( '# Creating Unit Category for "%s"'%new_cat )
print( '# Read As: 1 default unit = conv_factor u_name units' )
print( 'create_category(       c_name="%s", def_units="%s" ) '%(new_cat, def_units)  )

unitL = set( [def_units, 'kcal/m**2/s', 'cal/cm**2/s', 'BTU/ft**2/s', 'W/m**2',
              'kcal/m**2/hr', 'cal/cm**2/hr', 'BTU/ft**2/hr', 
              'W/cm**2', 'W/in**2', 'J/s/m**2' ] )

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


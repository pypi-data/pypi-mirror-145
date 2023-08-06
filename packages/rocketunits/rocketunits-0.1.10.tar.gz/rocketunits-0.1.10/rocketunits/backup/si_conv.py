import sys
import pint
from pint import UnitRegistry
from rocketunits.rocket_units import categoryD, convert_string, convert_value, \
                                 display_def_unitsD, display_unitsD, SI_unitsD
ureg = UnitRegistry()
ureg.define('gee = 9.80665 * m/s**2')

ureg.define('delK = degK')
ureg.define('delC = degC')
ureg.define('delF = degF')
ureg.define('delR = degR')

ureg.define('lbm = pound')
ureg.define('SG = g/ml')
ureg.define('specific_gravity = g/ml')

ureg.define('galUS = gallon')
ureg.define('elem = particle')
ureg.define('gmole = mole')

ureg.define('kcal = 1000 * cal')
ureg.define('my_mil = inch / 1000 ')
ureg.define('gal_H2O = 3.77842 kg')

ureg.define('lbmole = 453.592 gmole')
ureg.define('psia = lbf/inch**2')
ureg.define('psid = lbf/inch**2')
ureg.define('psf = lbf/ft**2')

ureg.define('my_cp = kg/s/m * 0.001')
ureg.define('barOil = ft**3 * 5.61458')
ureg.define('galUK = ft**3 * 0.160544')
ureg.define('gpm = galUS/min')

# def convert_value( inp_val=20.0, inp_units='degC', out_units='degK'):
# def convert_string( sinp="1 atm", rtn_units="psia" ):
equivUnitD = {}
equivUnitD['kcal/g/C'] =  'kcal/g/K'
equivUnitD['BTU/lbm/F'] =  'BTU/lbm/degR'
equivUnitD['cal/g/C'] =  'cal/g/K'
equivUnitD['BTU/inch**2/s/F'] =  'BTU/inch**2/s/degR'
equivUnitD['BTU/ft**2/hr/F'] =  'BTU/ft**2/hr/degR'

equivUnitD['lbf-sec/lbm'] = 'lbf*sec/lbm'
equivUnitD['N-sec/kg'] = 'N*sec/kg'
equivUnitD['mil'] = 'my_mil'
equivUnitD['BTU/s/inch/F'] =  'BTU/s/inch/degR'
equivUnitD['BTU/lbm/F'] = 'BTU/lbm/degR'
equivUnitD['BTU/s/ft/F'] = 'BTU/s/ft/degR'
equivUnitD['cal/s/cm/C'] = 'cal/s/cm/K'
equivUnitD['W/cm/C'] = 'W/cm/K'
equivUnitD['cal/s/m/C'] = 'cal/s/m/K'
equivUnitD['BTU/hr/ft/F'] = 'BTU/hr/ft/degR'
equivUnitD['cp'] = 'my_cp'


#equivUnitD['kJ/kg/K'] = 'skip'
#equivUnitD['J/kg/K'] = 'skip'
equivUnitD['cal/cm**2/s/C'] = 'cal/cm**2/s/K'
equivUnitD['kcal/m**2/hr/C'] = 'kcal/m**2/hr/K'
equivUnitD['W/m**2/C'] = 'W/m**2/K'
equivUnitD['cal/s/cm/C'] = 'cal/s/cm/K'
equivUnitD['W/cm/C'] = 'W/cm/K'
equivUnitD['kcal/m**2/hr/C'] = 'kcal/m**2/hr/K'
equivUnitD['cal/s/m/C'] = 'cal/s/m/K'
equivUnitD['xxx'] = 'xxx'
equivUnitD['xxx'] = 'xxx'
equivUnitD['xxx'] = 'xxx'
equivUnitD['xxx'] = 'xxx'

#equivUnitD['W/m/K'] = 'skip'
equivUnitD['xxx'] = 'skip'
equivUnitD['xxx'] = 'skip'
equivUnitD['xxx'] = 'skip'
equivUnitD['xxx'] = 'skip'
equivUnitD['xxx'] = 'skip'

pad = '        '

catL = sorted( list(categoryD.keys()) )
for cat in catL:
    si_unit = SI_unitsD[cat]
    pint_si_unit = equivUnitD.get( si_unit, si_unit )
    pint_si_unit = pint_si_unit.replace( '-','*' )
    
    print(pad+"# ", cat, " Using SI ref of 1.0", si_unit, '==', pint_si_unit)
    
    #print('Getting si_val of si_unit=', si_unit)
    si_val = 1.0 * ureg( pint_si_unit )
    
    for unit in display_unitsD[cat]:
        u = equivUnitD.get( unit, unit )
        
        #if u=='degF':
        #    u = 'degR'
        
        u = u.replace( '-','*' )
        if cat == "Isp" and u=="sec":
            u = 'lbf*sec/lbm'
        
        try:
            val = si_val.to( u )
        except:
            print( "Failed to convert", si_unit , " to", unit, '..or..', u )
            val = si_val.to( unit )
            sys.exit()
        print( pad+"self.assertAlmostEqual(1.0, %g / "%val.magnitude +\
            'convert_value(inp_val=1.0, inp_units="%s", out_units="%s"), places=5)'%(si_unit, unit))

#for units in categoryD['Angle']:
#    val = 1.0 * ureg(units) 
#    print( units, val, val.to("deg") )
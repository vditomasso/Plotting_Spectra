import math
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import numpy as np 
from scipy import stats
from scipy import interpolate
from operator import sub
from scipy.interpolate import interp1d
import pandas as pd
import types
import BDdb
db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')

# Queries for source id, shortname, RV, order, and spectra ID for all order 61 spectra with uncertainties whose objects have RVs
data=db.query.execute("select sources.id, sources.shortname, radial_velocities.radial_velocity, spectra.wavelength_order, spectra.id from sources join spectra on sources.id=spectra.source_id join radial_velocities on spectra.source_id=radial_velocities.source_id where spectra.wavelength_order=61 and length(spectra.unc)>0").fetchall()

comp_data=[]

for i in range(len(data)):
	opt_spec_type = db.query.execute("select spectral_types.spectral_type, spectral_types.gravity from spectral_types where spectral_types.source_id={} and spectral_types.regime='OPT'".format(data[i][0])).fetchone()
	ir_spec_type = db.query.execute("select spectral_types.spectral_type, spectral_types.gravity from spectral_types where spectral_types.source_id={} and spectral_types.regime='IR'".format(data[i][0])).fetchone()
	if (type(opt_spec_type) == types.NoneType):
		opt_spec_type = (None,None)
	else:
		pass
		
	if (type(ir_spec_type) == types.NoneType):
		ir_spec_type = (None,None)
	else:
		pass		
	
	tuple_in_loop=data[i] + opt_spec_type + ir_spec_type
	list_in_loop=list(tuple_in_loop)
	comp_data.append(list_in_loop)

source_ids=[]
shortnames=[]
rvs=[]
orders=[]
spec_ids=[]
opt_spec_types=[]
opt_gravitys=[]
ir_spec_types=[]
ir_gravitys=[]

for i in range(len(comp_data)):
	source_ids.append(comp_data[i][0])
	shortnames.append(comp_data[i][1])
	rvs.append(comp_data[i][2])
	orders.append(comp_data[i][3])
	spec_ids.append(comp_data[i][4])
	opt_spec_types.append(comp_data[i][5])
	opt_gravitys.append(comp_data[i][6])
	ir_spec_types.append(comp_data[i][7])
	ir_gravitys.append(comp_data[i][8])

d = {'source_id' : source_ids, 'shortname' : shortnames, 'rv' : rvs, 'order' : orders, 'opt_spec_type' : opt_spec_types, 'opt_gravity' : opt_gravitys, 'ir_spec_type' : ir_spec_types, 'ir_gravity' : ir_gravitys, 'spec_id' : spec_ids}
df = pd.DataFrame(d)
df.to_csv('comp_sample_order_61.txt',sep='\t')
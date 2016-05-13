import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 
import BDdb
db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')

# plot_all.plot_all([726,601,105,17,98,317,334,84,313,854,1722], 62)

def plot_all(list_of_source_ids, order_number):
	
	for i in list_of_source_ids :
		data = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id={} and spectra.wavelength_order={}".format(i,order_number)).fetchone()
		obj_info = "sourceid_"+str(i)
		print obj_info
		obj_info = data
		
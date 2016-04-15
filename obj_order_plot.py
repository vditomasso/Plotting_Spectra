import math
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import numpy as np 
import scipy
from operator import sub
from scipy.interpolate import interp1d
from decimal import Decimal

import BDdb
db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')

def obj_order_plot(tar_source_id, specid_58, specid_59, specid_61, specid_62, specid_63, specid_64, specid_65, comp_color) :


# Want to plot all the orders from one of our objects against the all the orders of another object
# 
# Want to give it a source id from our object and spectral IDs from the comparison objects
# 
# Query for our object's:
# - shortname, spectral type
# - 58: wavelength, flux


	tar_obj = db.query.execute("select sources.shortname, spectral_types.spectral_type from sources join spectral_types on sources.id=spectral_types.source_id where sources.id={}".format(tar_source_id)).fetchone()
	tar_58 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=58".format(tar_source_id)).fetchone()
	tar_59 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=59".format(tar_source_id)).fetchone()
	tar_61 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=61".format(tar_source_id)).fetchone()
	tar_62 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=62".format(tar_source_id)).fetchone()
	tar_63 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=63".format(tar_source_id)).fetchone()
	tar_64 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=64".format(tar_source_id)).fetchone()
	tar_65 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.source_id={} and spectra.wavelength_order=65".format(tar_source_id)).fetchone()

	comp_obj = db.query.execute("select sources.shortname, spectral_types.spectral_type from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id where spectra.id={}".format(specid_58)).fetchone()
	comp_58 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_58)).fetchone()
	comp_59 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_59)).fetchone()
	comp_61 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_61)).fetchone()
	comp_62 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_62)).fetchone()
	comp_63 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_63)).fetchone()
	comp_64 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_64)).fetchone()
	comp_65 = db.query.execute("select spectra.wavelength, spectra.flux, spectra.wavelength_order from spectra where spectra.id={}".format(specid_65)).fetchone()

# 	avg_f_tar=np.mean(f_tar)
# 	avg_f_young=np.mean(f_young)
# 	avg_f_field=np.mean(f_field)
	
# 	for i in [58,59,61,62,63,64,65]:
# 		thing = np.mean(tar_%s) % (i,i)
# 		add_to_tar_%s = 1 - tar_%s_avg % (i,i)
# 		tar_%s = tar_%s + add_to_tar_%s % (i,i)
	
# 	add_to_f_young = 1 - avg_f_young
# 	add_to_f_field = 1 - avg_f_field
# 	add_to_f_tar = 1 - avg_f_tar

# 	f_young_normalized = f_young + add_to_f_young
# 	f_tar_normalized = f_tar + add_to_f_tar
# 	f_field_normalized = f_field + add_to_f_field




	starname='2M'+str(tar_obj[0])+' M'+str(tar_obj[1])
	compname='2M'+str(comp_obj[0])+' '+str(comp_obj[1])

	f, axarr = plt.subplots(7)
	axarr[0].plot(tar_58[0], tar_58[1], 'k', linewidth=0.25)
	axarr[0].plot(comp_58[0], comp_58[1], 'k', c=comp_color, linewidth=0.25)
	axarr[1].plot(tar_59[0], tar_59[1], 'k', linewidth=0.25)
	axarr[1].plot(comp_59[0], comp_59[1], 'k', c=comp_color, linewidth=0.25)
	axarr[2].plot(tar_61[0], tar_61[1], 'k', linewidth=0.25)
	axarr[2].plot(comp_61[0], comp_61[1], 'k', c=comp_color, linewidth=0.25)
	axarr[3].plot(tar_62[0], tar_62[1], 'k', linewidth=0.25)
	axarr[3].plot(comp_62[0], comp_62[1], 'k', c=comp_color, linewidth=0.25)
	axarr[4].plot(tar_63[0], tar_63[1], 'k', linewidth=0.25)
	axarr[4].plot(comp_63[0], comp_63[1], 'k', c=comp_color, linewidth=0.25)
	axarr[5].plot(tar_64[0], tar_64[1], 'k', linewidth=0.25)
	axarr[5].plot(comp_64[0], comp_64[1], 'k', c=comp_color, linewidth=0.25)
	axarr[6].plot(tar_65[0], tar_65[1], 'k', linewidth=0.25)
	axarr[6].plot(comp_65[0], comp_65[1], 'k', c=comp_color, linewidth=0.25)
	axarr[0].annotate("Order = "+str(comp_58[2]),xy=(1.320, 0.2), xycoords='data',xytext=(1.320, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[0].annotate(starname,xy=(1.3075, 0.2), xycoords='data',xytext=(1.3075, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[1].annotate(compname,xy=(1.3075, 0.2), xycoords='data',xytext=(1.3075, 0.2), textcoords='data',size=20, va="center", ha="center", color=comp_color)
	axarr[0].set_xlim([1.304, 1.323])
	axarr[1].annotate(str(comp_59[2]),xy=(1.2995, 0.2), xycoords='data',xytext=(1.2995, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[1].set_xlim([1.282, 1.301])
	axarr[2].annotate(str(comp_61[2]),xy=(1.2565, 0.2), xycoords='data',xytext=(1.2565, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[2].set_xlim([1.241, 1.258])
	axarr[3].annotate(str(comp_62[2]),xy=(1.2365, 0.2), xycoords='data',xytext=(1.2365, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[3].set_xlim([1.220, 1.238])
	axarr[4].annotate(str(comp_63[2]),xy=(1.217, 0.2), xycoords='data',xytext=(1.217, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[4].set_xlim([1.201, 1.2185])
	axarr[5].annotate(str(comp_64[2]),xy=(1.198, 0.2), xycoords='data',xytext=(1.198, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[5].set_xlim([1.183, 1.1995])
	axarr[6].annotate(str(comp_65[2]),xy=(1.1795, 0.2), xycoords='data',xytext=(1.1795, 0.2), textcoords='data',size=20, va="center", ha="center")
	axarr[6].set_xlim([1.164, 1.181])
	
	for i in [0,1,2,3,4,5,6]:
		axarr[i].set_ylim([0.00,1.2])
		axarr[i].yaxis.set_ticks(np.arange(0.0,1.21,0.4))
    
    #Visually organizes overall plot and names the axes.
	f.set_figheight(15)
	f.set_figwidth(10)
	f.subplots_adjust(hspace=0.35)
	f.text(0.5, 0.04, 'Wavelength, (${\mu}m$)', ha='center', size=20)
	f.text(0.04, 0.5, 'Normalized Flux', va='center', rotation='vertical', size=20)


    #Saves file with starname.
# 	plt.show ()
#     f.savefig('stackedPlot_' + str(filename) + '.png')
	f.savefig('stackedPlot_practice' + '.png')
	f.clf()
	plt.close()
import math
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import numpy as np 
from scipy import stats
from operator import sub
from scipy.interpolate import interp1d
# import BDdb
# db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')
from astrodbkit import astrodb
db = astrodb.Database('/Users/victoriaditomasso/Dropbox/BDNYCdb/bdnycdev.db')

# The inputs are the spectral_id for the target object and the comparison object
def yfcq(spec_tar, spec_comp):

# This clears the figure, useful when saving the plots
	plt.clf()
	
# Gets the wavelength, flux, shortname, spectral type, RV, spectra_unc for the objects corresponding to the two spectral_ids
	data_tar = db.query("select spectra.spectrum, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_tar),fetch='one')
	data_comp = db.query("select spectra.spectrum, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_comp),fetch='one')

# 	data_tar = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity, spectra.unc from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_tar)).fetchone()
# 	data_comp = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity, spectra.unc from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_comp)).fetchone()

	print(data_tar)

# Separates out the wavelength array, flux array, RV and uncertainty as a float for the two spectra	
	
	w_tar,f_tar,unc_tar=data_tar[0].data
	w_comp,f_comp,unc_comp=data_comp[0].data

# 	w_tar = np.asarray(data_tar[0])
# 	f_tar = np.asarray(data_tar[1])
# 	
# 	w_comp = np.asarray(data_comp[0])
# 	f_comp = np.asarray(data_comp[1])
# 	
	rv_tar = data_tar[3]
	rv_comp = data_comp[3]
# 	
# 	unc_tar = data_tar[5]
# 	unc_comp = data_comp[5]
	
# Shifts the two spectra based on their RVs
	shifted_w_tar = (w_tar)*(1.-(rv_tar/2.99792458e5))
	shifted_w_comp = (w_comp)*(1.-(rv_comp/2.99792458e5))

# Finds a normalization coefficient	
	ck = sum((f_tar * f_comp)/(unc_tar * unc_comp))/sum((f_comp * f_comp)/(unc_tar * unc_comp))
	
	dk = sum((f_tar * f_comp)/((unc_tar)**2 + (unc_comp)**2))/sum((f_comp * f_comp)/((unc_tar)**2 + (unc_comp)**2))
	
	bk=sum((f_tar * f_comp))/sum((f_comp * f_comp))
	
# Creates an array of normalized flux for the comparison object
	f_comp_norm_ck = f_comp * ck
	f_comp_norm_dk = f_comp * dk

#Plots no shifting on top & just the RV shift on the bottom

#This plot is made up of two subplots
	plt.subplot(211)
#Makes the plots share an x-axis
	plt.gca().axes.get_xaxis().set_visible(False)
#Plots the original spectra over each other on top
	plt.plot(w_tar, f_tar, color='black')
	plt.plot(w_comp, f_comp, color='red')
# #Arbitrarily set y limits for ease of viewing
# 	plt.subplot(211).set_ylim(0, 1.2)

#Editing the bottom plot
	plt.subplot(212)
#Plots the RV shifted spectra over each other
	plt.plot(shifted_w_tar, f_tar, color='black')
	plt.plot(shifted_w_comp, f_comp, color='red')
# 	plt.subplot(212).set_ylim(0, 1.2)

#Makes the subplots appear right on top of one another, with no space in between
	plt.subplots_adjust(wspace=0,hspace=0)


# #Plots just RV shift on top & normalized spectra on the bottom
# 	
# #This plot is made up of two subplots
# 	plt.subplot(211)
# #Makes the plots share an x-axis
# 	plt.gca().axes.get_xaxis().set_visible(False)
# #Plots the original spectra over each other on top
# 	plt.plot(w_tar, f_tar, color='black')
# 	plt.plot(shifted_w_comp, f_comp, color='red')
# #Arbitrarily set y limits for ease of viewing
# 	plt.subplot(211).set_ylim(0, 1.2)
# 
# #Editing the bottom plot
# 	plt.subplot(212)
# #Plots the RV shifted spectra over each other
# 	plt.plot(shifted_w_tar, f_tar, color='black')
# 	plt.plot(shifted_w_comp, f_comp_norm_ck, color='red')
# #	plt.plot(shifted_w_comp, f_comp_norm_dk, color='blue')
# 	plt.subplot(212).set_ylim(0, 1.2)
# 
# #Makes the subplots appear right on top of one another, with no space in between
# 	plt.subplots_adjust(wspace=0,hspace=0)
	
# Prints the RVs of the target and comparison objects that you plotted
	print 'rv_tar=',rv_tar
	print 'rv,comp=',rv_comp
	
# Shows the plots
	plt.show()
	
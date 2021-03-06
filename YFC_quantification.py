import math
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import numpy as np 
from scipy import stats
from scipy import interpolate
from operator import sub
from scipy.interpolate import interp1d
import BDdb
db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')

# The inputs are the spectral_id for the target object and the comparison object
def yfcq(tar_source_id, spec_order):

# This clears the figure, useful when saving the plots
	plt.clf()
	
	data_tar = db.query.execute("select sources.id, sources.shortname, spectra.wavelength, spectra.flux, spectra.unc, radial_velocities.radial_velocity from sources join spectra on sources.id=spectra.source_id join radial_velocities on spectra.source_id=radial_velocities.source_id where spectra.source_id={} and spectra.wavelength_order={}".format(tar_source_id, spec_order)).fetchall()
	tar_spectype = db.query.execute("select spectral_types.spectral_type, spectral_types.gravity from spectral_types where spectral_types.source_id={} and (spectral_types.regime='OPT' or spectral_types.regime='IR')".format(tar_source_id)).fetchall()

	data_comp = db.query.execute("select sources.id, sources.shortname, spectra.wavelength, spectra.flux, spectra.unc, spectra.id, radial_velocities.radial_velocity from sources join spectra on sources.id=spectra.source_id join radial_velocities on spectra.source_id=radial_velocities.source_id where spectra.wavelength_order={} and exists (select radial_velocities.radial_velocity from spectra join radial_velocities on spectra.source_id=radial_velocities.source_id where spectra.instrument_id=9 and spectra.telescope_id=9) and exists(select radial_velocities.radial_velocity_unc)".format(spec_order)).fetchall()
# 	tar_spectype = #need to make this give me the spec_id of the comparison (so that I can group by it later) and give it all the same wheres as the previous query so that I get spectral types for all the objects that I pull spectra for in the previous query

	for i in range(len(data_comp)) :
	# #Gets the wavelength, flux, shortname, spectral type, RV, spectra_unc for the objects corresponding to the two spectral_ids
	# 	data_tar = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity, spectra.unc from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_tar)).fetchone()
	# 	data_comp = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity, spectra.unc from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_comp)).fetchone()

	# Separates out the wavelength array, flux array, RV and uncertainty as a float for the two spectra
		w_tar = np.asarray(data_tar[0][2])
		f_tar = np.asarray(data_tar[0][3])
	
		w_comp = np.asarray(data_comp[i][2])
		f_comp = np.asarray(data_comp[i][3])
	
		rv_tar = data_tar[0][5]
		rv_comp = data_comp[i][6]
	
		unc_tar = data_tar[0][4]
		unc_comp = data_comp[i][4]
	
	# Shifts the two spectra based on their RVs
		shifted_w_tar = (w_tar)*(1.-(rv_tar/2.99792458e5))
		shifted_w_comp = (w_comp)*(1.-(rv_comp/2.99792458e5))

	# Interpolates the flux for the comp object so that when I subtract it from the target flux, I will get a properly calculated residual
	# Remember: once you interpolate, you need to plot the w_tar vs the interpolated flux NOT w_comp vs interpolated flux
		x = shifted_w_tar
		xp = shifted_w_comp
		fp = f_comp
		f_comp_interp = np.interp(x, xp, fp)

	# Finds a normalization coefficient
		dk = sum((f_tar * f_comp)/((unc_tar)**2 + (unc_comp)**2))/sum((f_comp * f_comp)/((unc_tar)**2 + (unc_comp)**2))
	
	# Creates an array of normalized flux for the comparison object
# 		f_comp_norm_ck = f_comp * ck
		f_comp_norm_dk = f_comp * dk
		f_comp_norm_dk_interp = f_comp_interp * dk

	# Subtracting the fluxes to get the residual flux
		diff = (f_tar) - (f_comp_norm_dk_interp)

	#Sets the last flux point that will be used in quantification calculation/will be plotted
		l=1000

	#Checking if unc arrays are actually snrs and, if they are, converting them by doing 1/unc
		unc=np.asarray(unc_comp)
		avg_unc = np.sum(unc)/len(unc)
		if avg_unc > 4.0:
			unc_comp = 1.0/unc

	# Calculates the root mean square of the residuals for a quantification of the fit, skipping the first 4 and last 4 data points (because the spectra can get weird at te ends)
		rms = ((np.sum(diff[10:l]**2))/(len(diff[10:l])))**(0.5)
	# Calculates the chisq value, you divide by the degrees of freedom to get a value near 1
		chisq_b4div = np.sum((f_tar[:l]-f_comp_norm_dk_interp[:l])**2/((unc_tar[:l]**2)+(unc_comp[:l]**2)))
		chisq = chisq_b4div/len(f_tar[:l])
	
	#This plot is made up of two subplots
		plt.subplot(311)
	#Makes the plots share an x-axis
		plt.gca().axes.get_xaxis().set_visible(False)
	#Plots the RV shifted/normalized/interpolated spectra over each other
		plt.plot(shifted_w_tar[:l], f_tar[:l], color='black')
		plt.plot(shifted_w_tar[:l], f_comp_norm_dk_interp[:l], color='red')
		plt.subplot(311).set_ylim(0, 1.2)

	#Editing the bottom plot
		plt.subplot(312)
	#Plots the uncertainties of the two spectra
		plt.plot(shifted_w_tar[:l], unc_tar[:l], color='black')
		plt.plot(shifted_w_tar[:l], unc_comp[:l], color='red')
	# 	plt.plot(shifted_w_tar, abs(diff), color='gray')
	# 	plt.subplot(312).set_ylim(0, 1.2)

	#Plots residuals
		plt.subplot(313)
		plt.plot(shifted_w_tar[:l], diff[:l], color='gray')
# 		plt.plot(shifted_w_tar, np.zeros(1024))
		plt.subplot(313).set_ylim(-0.5, 0.5)
	
	
	# #Prints the RVs of the target and comparison objects that you plotted
	# 	print 'rv_tar=',rv_tar
	# 	print 'rv,comp=',rv_comp
	#	Print the calculated RMS
		print 'source_id=',data_comp[i][0],'shortname=',data_comp[i][1],'wavelength_order=',spec_order,'spec_id=',data_comp[i][5],'RMS=', rms, 'chisq=', chisq
		
	# Shows the plots
		plt.show()

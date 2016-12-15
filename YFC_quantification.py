#yfcq_auto
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
import pandas as pd
db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')

# The inputs are the target source id, the spec order being compared and the path to the text file with the comparison sample (has to be tab delimited)
def yfcq(tar_source_id, spec_order, path_to_comp_sample_dataframe):

# This clears the figure, useful when saving the plots
	plt.clf()
	
	data_tar = db.query.execute("select sources.id, sources.shortname, spectra.wavelength, spectra.flux, spectra.unc, radial_velocities.radial_velocity from sources join spectra on sources.id=spectra.source_id join radial_velocities on spectra.source_id=radial_velocities.source_id where spectra.source_id={} and spectra.wavelength_order={}".format(tar_source_id, spec_order)).fetchall()
	tar_spectype = db.query.execute("select spectral_types.spectral_type, spectral_types.gravity from spectral_types where spectral_types.source_id={} and (spectral_types.regime='OPT' or spectral_types.regime='IR')".format(tar_source_id)).fetchall()
	tar_opt_spec_type = db.query.execute("select spectral_types.spectral_type, spectral_types.gravity from spectral_types where spectral_types.source_id={} and spectral_types.regime='OPT'".format(tar_source_id)).fetchone()
	ir_spec_type = db.query.execute("select spectral_types.spectral_type, spectral_types.gravity from spectral_types where spectral_types.source_id={} and spectral_types.regime='IR'".format(tar_source_id)).fetchone()

	df=pd.read_csv(path_to_comp_sample_dataframe,sep='\t')
	
	chisqs=[]
	
	for i, row in df.iterrows() :
	
		chisq_indivs = []
	
#Gets the wavelength, flux, shortname, spectral type, RV, spectra_unc for the objects corresponding to the two spectral_ids
	# 	data_tar = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity, spectra.unc from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_tar)).fetchone()
	# 	data_comp = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, radial_velocities.radial_velocity, spectra.unc from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id join radial_velocities on sources.id=radial_velocities.source_id where spectra.id={}".format(spec_comp)).fetchone()

#Gets the wavelength, flux, and uncertainty for the spec_ids listed in comp_sample
		data_comp = db.query.execute("select spectra.wavelength, spectra.flux, spectra.unc from spectra where spectra.id={}".format(row['spec_id'])).fetchall()

	# Separates out the wavelength array, flux array, RV and uncertainty as a float for the two spectra	
		w_tar = np.asarray(data_tar[0][2])
		f_tar = np.asarray(data_tar[0][3])
	
		w_comp = np.asarray(data_comp[0][0])
		f_comp = np.asarray(data_comp[0][1])
	
		rv_tar = data_tar[0][5]
		rv_comp = row['rv']
	
		unc_tar = data_tar[0][4]
		unc_comp = data_comp[0][2]
	
	# Shifts the two spectra based on their RVs
		shifted_w_tar = (w_tar)*(1.-(rv_tar/2.99792458e5))
		shifted_w_comp = (w_comp)*(1.-(rv_comp/2.99792458e5))

	# Interpolates the flux for the comp object so that when I subtract it from the target flux, I will get a properly calculated residual
	# Remember: once you interpolate, you need to plot the w_tar vs the interpolated flux NOT w_comp vs interpolated flux
		x = shifted_w_tar
		xp = shifted_w_comp
		fp = f_comp
		f_comp_interp = np.interp(x, xp, fp)

	#Checking if unc arrays are actually snrs and, if they are, converting them by doing 1/unc
		unc=np.asarray(unc_comp)
		avg_unc = np.sum(unc)/len(unc)
		if avg_unc > 4.0:
			unc_comp = 1.0/unc
		if avg_unc == 1.0:
			print 'UNC AVG = 1:'

	# Interpolate the unc
		w = shifted_w_tar
		wp = shifted_w_comp
		up = unc_comp
		unc_comp_interp = np.interp(w, wp, up)

	# Finds a normalization coefficient	
		dk = sum((f_tar * f_comp)/((unc_tar)**2 + (unc_comp_interp)**2))/sum((f_comp * f_comp)/((unc_tar)**2 + (unc_comp_interp)**2))
	
	# Creates an array of normalized flux for the comparison object
# 		f_comp_norm_ck = f_comp * ck
		f_comp_norm_dk = f_comp * dk
		f_comp_norm_dk_interp = f_comp_interp * dk

	# Subtracting the fluxes to get the residual flux
		diff = (f_tar) - (f_comp_norm_dk_interp)

	#Sets the first and last flux point that will be used in quantification calculation/will be plotted
		f=50
		l=1000

	# Calculates the root mean square of the residuals for a quantification of the fit, skipping the first 4 and last 4 data points (because the spectra can get weird at te ends)
		rms = ((np.sum(diff[f:l]**2))/(len(diff[f:l])))**(0.5)
	# Calculates the chisq value, you divide by the degrees of freedom to get a value near 1
		chisq_b4div = np.sum((f_tar[f:l]-f_comp_norm_dk_interp[f:l])**2/((unc_tar[f:l]+unc_comp_interp[f:l])**2))
		chisq = chisq_b4div/len(f_tar[f:l])
		
		for j in range(len(f_tar)):
			chisq_indiv = ((f_tar[j]-f_comp_norm_dk_interp[j])**2/((unc_tar[j]+unc_comp_interp[j])**2))/(len(f_tar[f:l]))
			chisq_indivs.append(chisq_indiv)
		
# 	# Chisq without uncertainties
# 		chisq_wo = np.sum((f_tar[f:l]-f_comp_norm_dk_interp[f:l])**2)
	
	#This plot is made up of two subplots
		plt.subplot(311)
	#Makes the plots share an x-axis
		plt.gca().axes.get_xaxis().set_visible(False)
	#Plots the RV shifted/normalized/interpolated spectra over each other
		plt.plot(shifted_w_tar[f:l], f_tar[f:l], color='black')
		plt.plot(shifted_w_tar[f:l], f_comp_norm_dk_interp[f:l], color='red')
		plt.subplot(311).set_ylim(0, 1.2)

	#Editing the middle plot
		plt.subplot(312)
	#Plots the uncertainties of the two spectra
# 		plt.plot(shifted_w_tar[f:l], unc_tar[f:l], color='black')
# 		plt.plot(shifted_w_tar[f:l], unc_comp_interp[f:l], color='red')
	# 	plt.plot(shifted_w_tar, abs(diff), color='gray')
	# 	plt.subplot(312).set_ylim(0, 1.2)

	#Plots the spectra with uncertainties as shaded area
		plt.plot(shifted_w_tar[f:l], f_tar[f:l], color='black')
		plt.fill_between(shifted_w_tar[f:l], np.asarray(f_tar[f:l]-unc_tar[f:l]), np.asarray(f_tar[f:l]+unc_tar[f:l]), color='grey', alpha=0.3)
		plt.plot(shifted_w_tar[f:l], f_comp_norm_dk_interp[f:l], color='red')
		plt.fill_between(shifted_w_tar[f:l], np.asarray(f_comp_norm_dk_interp[f:l]-unc_comp_interp[f:l]), np.asarray(f_comp_norm_dk_interp[f:l]+unc_comp_interp[f:l]), color='red', alpha = 0.3)
		plt.subplot(312).set_ylim(0, 1.2)
	 
	#Plots residuals
		plt.subplot(313)
		plt.plot(shifted_w_tar[f:l], chisq_indivs[f:l], color='gray')
		plt.plot(shifted_w_tar[f:l], np.zeros((l-f)))
		plt.subplot(313).set_ylim(-0.2, 0.2)
# 		plt.annotate(label, xytext=()
	
	
	# #Prints the RVs of the target and comparison objects that you plotted
	# 	print 'rv_tar=',rv_tar
	# 	print 'rv,comp=',rv_comp
	#	Print the calculated RMS
		print 'source_id=',row['source_id'],'shortname=',row['shortname'],'wavelength_order=',row['order'],'spec_id=',row['spec_id'],'RMS=', rms, 'chisq=', chisq
		
	# Shows the plots
# 		plt.show()
		
		
# 		print row['shortname']
		
		label = '/Users/victoriaditomasso/Plotting_Spectra/'+str(row['shortname'])+'_'+str(chisq)+'.png'
		print label
# 		print type(label)
		chisqs.append(chisq)
		plt.savefig(label)

# 		print chisq_indivs
# 		print type(chisq_indivs)
		
	df['chisq'] = chisqs
	
	df.to_csv(str(data_tar[0][1])+'_'+str(spec_order)+'_chisq_bad_removed.txt',sep='\t')

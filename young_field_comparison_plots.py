import math
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import numpy as np 
from scipy import stats
from operator import sub
from scipy.interpolate import interp1d
import BDdb
db = BDdb.get_db('/Users/victoriaditomasso/Dropbox/BDNYCdb/BDNYCdeprecated.db')

# The inputs for this function are the three spectral IDs, in the order young, target and field aged plus the radial velocity of the target object and an optional shift value for the young & field objects
def yfcp(spec_young, spec_target, spec_field, rv_tar=0, shift_young=0, shift_field=0):
 

	# This clears the figure, useful when saving the plots (not just showing them). If you save the same plot repeatedly, clearing the figure keeps it from plotting over itself
	plt.clf() 
	
	# These queries give the wavelength array, flux array, the shortname (ie BRLT... or 2MASS...), the spectral type (written in numbers, 09 is M9, 12 is L2, etc), and the wavelength order for the given spectral_ids
	data_young = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, spectra.wavelength_order from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id where spectra.id={}".format(spec_young)).fetchone()
	data_target = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, spectra.wavelength_order from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id where spectra.id={}".format(spec_target)).fetchone()
	data_field = db.query.execute("select spectra.wavelength, spectra.flux, sources.shortname, spectral_types.spectral_type, spectra.wavelength_order from spectra join sources on spectra.source_id=sources.id join spectral_types on spectra.source_id=spectral_types.source_id where spectra.id={}".format(spec_field)).fetchone()

	# Separates out the different sets of information into arrays for each of the three objects
	w_tar = np.asarray(data_target[0][0:1010])
	f_tar = np.asarray(data_target[1][0:1010])
	
	w_young = np.asarray(data_young[0][0:1010])
	f_young = np.asarray(data_young[1][0:1010])
	
	w_field = np.asarray(data_field[0][0:1010])
	f_field = np.asarray(data_field[1][0:1010])
		
	# Shifts the wavelength of the young and field objects using the radial velocity of the target, so that they will line up horizontally when plotted
	shifted_w_young = ((w_young)*(1.+(rv_tar/2.99792458e5)))+shift_young
	shifted_w_field = (w_field)*(1.+(rv_tar/2.99792458e5))+shift_field
	
	# I use the average of the fluxes to make the three spectra line up vertically
	avg_f_tar=np.mean(f_tar)
	avg_f_young=np.mean(f_young)
	avg_f_field=np.mean(f_field)
		
	add_to_f_young = 1 - avg_f_young
	add_to_f_field = 1 - avg_f_field
	add_to_f_tar = 1 - avg_f_tar
	
	f_young_normalized = f_young + add_to_f_young
	f_tar_normalized = f_tar + add_to_f_tar
	f_field_normalized = f_field + add_to_f_field
		
	# Parses out the shortnames, spectral types and the wavelength order (I only specified the target wavelength order, but it's the same for all of the objects)	
	tar_name = data_target[2]
	young_name = data_young[2]
	field_name = data_field[2]
	
	tar_spec_type = data_target[3]
	young_spec_type = data_young[3]
	field_spec_type = data_field[3]
	
	tar_order = data_target[4]

	# Interpolates the flux for the young and field objects so that when I subtract them from the target flux, I will get a properly calculated residual
	x_tar = w_tar
	xp_young = shifted_w_young
	fp_young = f_young_normalized
	f_young_interp = np.interp(x_tar, xp_young, fp_young)
# 	print "f_young_interp = ", f_young_interp

	xp_field = shifted_w_field
	fp_field = f_field_normalized
	f_field_interp = np.interp(x_tar, xp_field, fp_field)
# 	print "f_field_interp = ", f_field_interp
	
	# Subtracting the fluxes to get the residual flux
	young_difference = (f_tar_normalized) - (f_young_interp)
	field_difference = (f_tar_normalized) - (f_field_interp)

	# Calculates the root mean square error of the residuals for a quantification of the fit
	rmse_young = (np.sum(young_difference**2))/(len(young_difference))**(0.5)
	rmse_field = (np.sum(field_difference**2))/(len(field_difference))**(0.5)

	# Changes the spectral type label from numbers to letter and number (ex: 6.5 becomes M6.5)
	if tar_spec_type == 6.5:
		tar_spec_type = 'M6.5'
	if tar_spec_type == 7.0:
		tar_spec_type = 'M7.0'
	if tar_spec_type == 7.5:
		tar_spec_type = 'M7.5'
	if tar_spec_type == 8.0:
		tar_spec_type = 'M8.0'
	if tar_spec_type == 8.5:
		tar_spec_type = 'M8.5'
	if tar_spec_type == 9.0:
		tar_spec_type = 'M9.0'
	if tar_spec_type == 9.5:
		tar_spec_type = 'M9.5'
	if tar_spec_type == 10.0:
		tar_spec_type = 'L0.0'
	if tar_spec_type == 10.5:
		tar_spec_type = 'L0.5'
	if tar_spec_type == 11.0:
		tar_spec_type = 'L1.0'
	if tar_spec_type == 11.5:
		tar_spec_type = 'L1.5'
	if tar_spec_type == 12.0:
		tar_spec_type = 'L2.0'
	if tar_spec_type == 12.5:
		tar_spec_type = 'L2.5'
	if tar_spec_type == 13.0:
		tar_spec_type = 'L3.0'
	if tar_spec_type == 13.5:
		tar_spec_type = 'L3.5'
	if tar_spec_type == 14.0:
		tar_spec_type = 'L4.0'
	if tar_spec_type == 14.5:
		tar_spec_type = 'L4.5'
	if tar_spec_type == 15.0:
		tar_spec_type = 'L5.0'
	if tar_spec_type == 15.5:
		tar_spec_type = 'L5.5'
	if tar_spec_type == 16.0:
		tar_spec_type = 'L6.0'
	if tar_spec_type == 16.5:
		tar_spec_type = 'L6.5'
	if tar_spec_type == 17.0:
		tar_spec_type = 'L7.0'
	if tar_spec_type == 17.5:
		tar_spec_type = 'L7.5'
	if tar_spec_type == 18.0:
		tar_spec_type = 'L8.0'
		
		
	if young_spec_type == 6.5:
		young_spec_type = 'M6.5'
	if young_spec_type == 7.0:
		young_spec_type = 'M7.0'
	if young_spec_type == 7.5:
		young_spec_type = 'M7.5'
	if young_spec_type == 8.0:
		young_spec_type = 'M8.0'
	if young_spec_type == 8.5:
		young_spec_type = 'M8.5'
	if young_spec_type == 9.0:
		young_spec_type = 'M9.0'
	if young_spec_type == 9.5:
		young_spec_type = 'M9.5'
	if young_spec_type == 10.0:
		young_spec_type = 'L0.0'
	if young_spec_type == 10.5:
		young_spec_type = 'L0.5'
	if young_spec_type == 11.0:
		young_spec_type = 'L1.0'
	if young_spec_type == 11.5:
		young_spec_type = 'L1.5'
	if young_spec_type == 12.0:
		young_spec_type = 'L2.0'
	if young_spec_type == 12.5:
		young_spec_type = 'L2.5'
	if young_spec_type == 13.0:
		young_spec_type = 'L3.0'
	if young_spec_type == 13.5:
		young_spec_type = 'L3.5'
	if young_spec_type == 14.0:
		young_spec_type = 'L4.0'
	if young_spec_type == 14.5:
		young_spec_type = 'L4.5'
	if young_spec_type == 15.0:
		young_spec_type = 'L5.0'
	if young_spec_type == 15.5:
		young_spec_type = 'L5.5'
	if young_spec_type == 16.0:
		young_spec_type = 'L6.0'
	if young_spec_type == 16.5:
		young_spec_type = 'L6.5'
	if young_spec_type == 17.0:
		young_spec_type = 'L7.0'
	if young_spec_type == 17.5:
		young_spec_type = 'L7.5'
	if young_spec_type == 18.0:
		young_spec_type = 'L8.0'
		
		
	if field_spec_type == 6.5:
		field_spec_type = 'M6.5'
	if field_spec_type == 7.0:
		field_spec_type = 'M7.0'
	if field_spec_type == 7.5:
		field_spec_type = 'M7.5'
	if field_spec_type == 8.0:
		field_spec_type = 'M8.0'
	if field_spec_type == 8.5:
		field_spec_type = 'M8.5'
	if field_spec_type == 9.0:
		field_spec_type = 'M9.0'
	if field_spec_type == 9.5:
		field_spec_type = 'M9.5'
	if field_spec_type == 10.0:
		field_spec_type = 'L0.0'
	if field_spec_type == 10.5:
		field_spec_type = 'L0.5'
	if field_spec_type == 11.0:
		field_spec_type = 'L1.0'
	if field_spec_type == 11.5:
		field_spec_type = 'L1.5'
	if field_spec_type == 12.0:
		field_spec_type = 'L2.0'
	if field_spec_type == 12.5:
		field_spec_type = 'L2.5'
	if field_spec_type == 13.0:
		field_spec_type = 'L3.0'
	if field_spec_type == 13.5:
		field_spec_type = 'L3.5'
	if field_spec_type == 14.0:
		field_spec_type = 'L4.0'
	if field_spec_type == 14.5:
		field_spec_type = 'L4.5'
	if field_spec_type == 15.0:
		field_spec_type = 'L5.0'
	if field_spec_type == 15.5:
		field_spec_type = 'L5.5'
	if field_spec_type == 16.0:
		field_spec_type = 'L6.0'
	if field_spec_type == 16.5:
		field_spec_type = 'L6.5'
	if field_spec_type == 17.0:
		field_spec_type = 'L7.0'
	if field_spec_type == 17.5:
		field_spec_type = 'L7.5'
	if field_spec_type == 18.0:
		field_spec_type = 'L8.0'

	
	# This is made up of two subplots	
	plt.subplot(211)
	# This makes the two plots share an x axis
	plt.gca().axes.get_xaxis().set_visible(False)
	# Plots the target object
	plt.plot(w_tar,f_tar_normalized,color='black', linewidth = 2)
	# Plots the young object
	plt.plot(shifted_w_young, f_young_normalized,color='r',label='2MASS ' + str(young_name), linewidth = 2)
	# Plots the young object using the interpolated flux values
# 	plt.plot(w_tar, f_young_interp, color='g', linewidth = 2)
	# Plots the residual
	plt.plot(w_tar, young_difference, color = 'gray',label='Residuals', linewidth = 2)
	# Sets the title
	plt.title('2MASS ' + str(tar_name) + ' Order ' + str(tar_order), ha='center', size=40)
	# Sets the y limits
	plt.subplot(211).set_ylim(min(young_difference), max(f_tar + add_to_f_tar))
	# Sets the font size of the y-axis labels
	plt.yticks(fontsize = 20)		
		
	# Makes the second subplot	
	plt.subplot(212)
	# Plots the target object
	plt.plot(w_tar,f_tar_normalized,color='black', linewidth = 2)
	# Plots the field object
	plt.plot(shifted_w_field, f_field_normalized,color='b',label='2MASS ' + str(field_name), linewidth = 2)
	# Plots the field object using the interpolated flux values
# 	plt.plot(w_tar, f_field_interp,color='g', linewidth = 2)
	# Plots the residual
	plt.plot(w_tar, field_difference, color = 'gray', label='Residuals', linewidth = 2)
	# Sets the x-axis label
	plt.xlabel('Wavelength, (${\mu}m$)', ha='center', size=30)
	# Sets the y limits
	plt.subplot(212).set_ylim(min(field_difference), max(f_tar + add_to_f_tar))
	# Sets the font size of the x and y labels
	plt.xticks(fontsize = 20)		
	plt.yticks(fontsize = 20)		

	# Makes the subplots appear right on top of one another, with no space in between
	plt.subplots_adjust(wspace=0,hspace=0)
			
	# Sets the size of the plot (I made it pretty big so that I could put it on a poster)
	fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(20, 20)
	
	# Sets the name of the figure for when you save it
	figname = str(tar_name) + ' Order ' + str(tar_order) + ' Young ' + str(young_name) + ' Field ' + str(field_name)
	# This text serves as the y-axis label
	fig.text(0.06, 0.5, 'Normalized Flux', va='center', rotation='vertical', fontsize=30)

	# This text serves as the legend	
	fig.text(.73, .74, '2M' + young_name, color='r', fontsize=30)
	fig.text(.73, .71, '2M' + tar_name, color='black', fontsize=30)
	fig.text(.73, .68, 'Residuals', color='gray', fontsize=30)

	fig.text(.73, .32, '2M' + field_name, color='b', fontsize=30)
	fig.text(.73, .29, '2M' + tar_name, color='black', fontsize=30)
	fig.text(.73, .26, 'Residuals', color='gray', fontsize=30)


	# Prints the quantification of the fits on the plots
	fig.text(.15,.51, 'RMSE young = ' + str(rmse_young), fontsize=25)
	fig.text(.15, .11, 'RMSE field = ' + str(rmse_field), fontsize=25)

	# Shows the plot
	plt.show()	
	# Saves the plot
# 	plt.savefig(figname)

	# Saves a textfile with your inputs so you can recreate the plot later, plus it save the RMSE values
	line1 = 'spec_young = '+str(spec_young)+', '+'2M'+str(young_name) 
	line2 = 'spec_target = '+str(spec_target)+', '+'2M'+str(tar_name)
	line3 = 'spec_field = '+str(spec_field)+', '+'2M'+str(field_name)
	line4 = 'rv_tar = '+str(rv_tar)+', shift_young = '+str(shift_young)+', shift_field = '+str(shift_field)
	line5 = 'young: RMSE = ' + str(rmse_young)
	line6 = 'field: RMSE = ' + str(rmse_field)

	text = open(str(figname) + '.txt', "w")
	text.write("%s \n %s \n %s \n %s \n %s \n %s \n" % (line1, line2, line3, line4, line5, line6))
	text.close()

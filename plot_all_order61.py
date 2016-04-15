import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 
import BDdb
db = BDdb.get_db('/Users/victoriaditomasso/Desktop/BDNYCdeprecated.db')

t0253 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=726 and spectra.wavelength_order=61").fetchone()
t0534 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=601 and spectra.wavelength_order=61").fetchone()
t1935 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=105 and spectra.wavelength_order=61").fetchone()
t0027 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=17 and spectra.wavelength_order=61").fetchone()
t0241 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=98 and spectra.wavelength_order=61").fetchone()
t0117 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=317 and spectra.wavelength_order=61").fetchone()
t0045 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=334 and spectra.wavelength_order=61").fetchone()
t1551 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=84 and spectra.wavelength_order=61").fetchone()
t2154 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=313 and spectra.wavelength_order=61").fetchone()
t1615 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=854 and spectra.wavelength_order=61").fetchone()
t0047 = db.query.execute("select spectra.wavelength, spectra.flux, spectral_types.spectral_type, sources.shortname from spectra join spectral_types on spectra.source_id=spectral_types.source_id join sources on sources.id=spectra.source_id where sources.id=1722 and spectra.wavelength_order=61").fetchone()

plt.clf()

fig = plt.gcf()
fig.set_size_inches(15, 20)


plt.xlim([1.241, 1.258])
plt.ylim([-0.5,11.5])

plt.plot(t0253[0],t0253[1]+10, label='2M'+str(t0253[3])+' '+str(t0253[2]))
plt.plot(t0534[0],t0534[1]+9, label='2M'+str(t0534[3])+' '+str(t0534[2]))
plt.plot(t1935[0],t1935[1]+8, label='2M'+str(t1935[3])+' '+str(t1935[2]))
plt.plot(t0027[0],t0027[1]+7, label='2M'+str(t0027[3])+' '+str(t0027[2]))
plt.plot(t0241[0],t0241[1]+6, label='2M'+str(t0241[3])+' '+str(t0241[2]))
plt.plot(t0117[0],t0117[1]+5, label='2M'+str(t0117[3])+' '+str(t0117[2]))
plt.plot(t0045[0],t0045[1]+4, label='2M'+str(t0045[3])+' '+str(t0045[2]))
plt.plot(t1551[0],t1551[1]+3, label='2M'+str(t1551[3])+' '+str(t1551[2]))
plt.plot(t2154[0],t2154[1]+2, label='2M'+str(t2154[3])+' '+str(t2154[2]))
plt.plot(t1615[0],t1615[1]+1, label='2M'+str(t1615[3])+' '+str(t1615[2]))
plt.plot(t0047[0],t0047[1]+0, label='2M'+str(t0047[3])+' '+str(t0047[2]))

plt.title('Order 61', ha='center', size=20)

plt.xlabel('Wavelength, (${\mu}m$)', ha='center', size=16)
plt.ylabel('Normalized Flux + Constant', ha='center', size=16)

box = plt.gca().get_position()
plt.gca().set_position([box.x0, box.y0 + box.height * 0.28, box.width, box.height * 0.72])    
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.17), fancybox=True, ncol=4, fontsize = 'medium')
#plt.show()
plt.savefig('Order 61')

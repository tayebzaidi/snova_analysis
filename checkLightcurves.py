import pylab
import json
import itertools

json_data=open('/home/tensortrash/Development/REU/snova_analysis/SplineDatarest2')
json_data_string = json_data.read()
data = json.loads(json_data_string)
json_data.close()

b_band = [i for i in data[1:] if (i['band']=='B')]
#v_band = [i for i in data[:] if i['band'] v']
print len(b_band)
for i in b_band:
    pylab.plot(i['phase'], i['splinedata'], 'k-')
    #pylab.plot(j['phase'], j['splinedata'], 'k-')
pylab.show()



from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import sys
import numpy as np
import json

#@profile
def main():
    with open('SplinedataDES_all_18000') as json_data:
        data = json.load(json_data)

    dt = np.dtype('|S16')
    
    g_length = 0
    r_length = 0
    i_length = 0
    z_length = 0

    for bdata in data:
        if bdata['band'] == 'g':
            g_length += 1
        if bdata['band'] == 'r':
            r_length += 1
        if bdata['band'] == 'i':
            i_length += 1
        if bdata['band'] == 'z':
            z_length += 1

    raw_data = np.zeros([r_length,40])
    raw_labels = np.zeros(r_length)
    raw_names = np.zeros(r_length, dtype=dt)

    print len(data) 
    i = 0

    
    for bdata in data:
        if bdata['band'] != 'r':
            continue
        
        spldata = bdata['spldata_sampled']
        raw_data[i,:] = np.array(spldata)
        sntype = bdata['stype']
        #if sntype in [2, 21, 22, 23, 66, -1]:
        #    sntype = 0
        #else:
        #    sntype = 1
        raw_labels[i] = sntype
        raw_names[i] = bdata['id']
        i += 1
    
    traindata_mask = np.random.uniform(0,1, r_length) <=.20
    train, testing = np.where(traindata_mask == True), np.where(traindata_mask == False)

    traindata = raw_data[train]
    testdata = raw_data[testing]


    clf = RandomForestClassifier(n_jobs=2)
    clf.fit(traindata, raw_labels[train])

    preds = clf.predict(testdata)

    print preds
    print raw_labels[testing]
    correct = preds - raw_labels[testing]
    idx = np.where(correct == 0)
    correct_ratio = len(correct[idx]) / float(len(correct))
    print correct_ratio
    #plt.hist(correct, bins = 90)
    #plt.show()

if __name__ == '__main__':
    sys.exit(main())

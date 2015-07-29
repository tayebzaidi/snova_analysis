from sklearn.ensemble import RandomForestClassifier
import numpy as np
import json

#@profile
def main():
    with open('SplinedataU') as json_data:
        data = json.load(json_data)

    dt = np.dtype('|S16')
    raw_data = np.empty([len(data),40])
    raw_labels = np.empty(len(data))
    raw_names = np.empty(len(data), dtype=dt)

    
    for i, bdata in enumerate(data):
        spldata = bdata['spldata_sampled']
        raw_data[i,:] = np.array(spldata)
        raw_labels[i] = bdata['stype']
        raw_names[i] = bdata['id']
    
    traindata_mask = np.random.uniform(0,1, len(data)) <=.80
    
    train, testing = np.where(traindata_mask == True), np.where(traindata_mask == False)

    traindata = raw_data[train]
    testdata = raw_data[testing]


    clf = RandomForestClassifier(n_jobs=2)
    clf.fit(traindata, raw_labels[train])

    preds = clf.predict(testdata)

    correct = preds - raw_labels[testing]
    idx = np.where(correct == 0)
    correct_ratio = len(correct[idx]) / float(len(correct))
    print correct_ratio

if __name__ == '__main__':
    main()

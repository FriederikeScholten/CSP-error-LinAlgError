

from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.preprocessing import ICA, corrmap
import numpy as np
from mne import Epochs, pick_types, events_from_annotations
from sklearn.model_selection import RepeatedStratifiedKFold
from mne.decoding import CSP




def load_data(subjects, runs=[6, 10, 14]):
    raws = [None] * len(subjects)
    for i, subject in enumerate(subjects):
        raw_fnames = eegbci.load_data(subject+1, runs)
        raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
        eegbci.standardize(raw)  # set channel names
        standard_1005 = make_standard_montage('standard_1005')
        raw.set_montage(standard_1005)
        raw.rename_channels(lambda x: x.strip('.'))
        raws[i] = raw
        
    return raws


def ICA_analysis(raws):
    raw_template = load_data(subjects=[0])
    raw_template[0].filter(7, 30, fir_design='firwin', skip_by_annotation='edge')
    ica_template = ICA(n_components=20, random_state=0, max_iter=800).fit(raw_template[0])
    template_eog_component = ica_template.get_components()[:, 7]
    template_ecg_component = ica_template.get_components()[:, 0]
    
    icas = [None] * len(raws)
    for i, raw in enumerate(raws):
        icas[i] = ICA(n_components=20, random_state=0, max_iter=800).fit(raw)
    
    # ica_template.plot_sources(raw_template[0])
    # icas[0].plot_sources(raws[0])
    
    try:
        corrmap(icas, template=template_eog_component, threshold=0.8, label='blink', plot=False)
    except:
        None
        
    try:
        corrmap(icas, template=template_ecg_component, threshold=0.8, label='QRS', plot=False)
    except:
        None
        
    for subject in range(len(icas)):
        remove_list = np.empty([0], dtype='int')
        for k in icas[subject].labels_.values():
            remove_list = np.append(remove_list, k)
        print("remove_list: {}".format(remove_list))
        icas[subject].exclude = remove_list
        raws[subject] = icas[subject].apply(raws[subject])
    
    return raws


def preprocessing(raws):
    # bandpass filter raw object
    for subject in range(len(raws)):
        raws[subject].filter(7, 30, fir_design='firwin', skip_by_annotation='edge')
    
    # # ICA filtering raw object
    raws = ICA_analysis(raws)
    
    # Crop and epoch data 
    epochs = [None] * len(raws)
    tmin, tmax = 0, 521/160
    n_samples = round(raws[0].info['sfreq'] * (tmax - tmin) + 1)
    
    n_channels = len(raws[0].info['chs'])
    X = np.empty([0,n_channels,n_samples])
    y = np.empty([0], dtype='int')
    
    for subject, raw in enumerate(raws):
        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = pick_types(raw.info, eeg=True, exclude='bads')
        
        event_id = dict(hands=2, feet=3)
        epochs[subject] = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks, baseline=None, preload=True)

        X = np.append(X, epochs[subject].get_data(),0) #dim 1: events, dim 2: channels, dim 3: samples
        y = np.append(y, epochs[subject].events[:, -1] - 2)
    
    return X, y    

raws_train = load_data(subjects=[2])
X_train, y_train = preprocessing(raws_train)

cv_inner = RepeatedStratifiedKFold(n_splits=3, n_repeats=1, random_state=0)
for train_index, test_index in cv_inner.split(X_train, y_train):
    print('train_index is: ', train_index)
    print('test_index: ', test_index)
    X1, X2 = X_train[train_index], X_train[test_index]
    y1, y2 = y_train[train_index], y_train[test_index]

    CSP(n_components=5, reg=1e-4).fit(X1, y1)


# indeces evoking error:

train_index = [ 0,  3,  4 , 6  ,7 , 9, 10, 12, 13, 15, 18 ,19 ,20 ,21 ,24 ,25 ,26, 27, 28 ,30 ,31, 33, 35, 36, 38,39, 40 ,42 ,43, 44]

test_index = [ 1 , 2 , 5 , 8, 11, 14, 16, 17 ,22, 23 ,29 ,32 ,34, 37, 41]


X1, X2 = X_train[train_index], X_train[test_index]
y1, y2 = y_train[train_index], y_train[test_index]

# save compressed .npz file
np.savez_compressed('preprocessingoutput', x1 = X1, x2 = X2, y1 = y1, y2 = y2)

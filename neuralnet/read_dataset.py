import numpy as np

def read_dataset(path_to_dataset_file):
    """ 
        Returns:
        
        dataset (numpy.ndarray): matrix with feature vector + label on last column
                                                
                                                dataset = [[x01,x02,...,x030,y0],
                                                           [x11,x12,...,x130,y1],
                                                           [x11,x12,...,x130,y2],
                                                           ...
                                                           ]
    """
    dataset  = []
    

    indexFile = open(path_to_dataset_file, 'r')
    for sample in indexFile:
        last_row = [] 
        
        # Values separated by commas
        values = sample.split(",")

        for i in range(len(values)):
            last_row.append(float(values[i]))
        
        # Convert labels to {0,1} format in case they are in {-1,1}
        if(last_row[len(last_row)-1]==-1):
            last_row[len(last_row)-1]=0
        
        dataset.append(last_row)
    dataset = np.array(dataset)
    return dataset

def separate_labels(dataset):
    """
        Returns:
        
        X(numpy.ndarray): sample feature matrix X = [[x1],
                                                     [x2],
                                                     [x3],
                                                     .......]                                                     
                                where xi is the 30-dimensional feature of each sample

        Y(numpy.ndarray): class label vector Y = [[y1],
                                                  [y2],
                                                  [y3],
                                                   ...]
                             where yi is 1/0, the label of each sample
    """
    X = []
    Y = []
    for i in range(dataset.shape[0]):
        last_x = []
        last_y = []
        for j in range(dataset.shape[1] - 1):
            last_x.append(dataset[i][j])
        last_y.append(dataset[i][dataset.shape[1] - 1])
        X.append(last_x)
        Y.append(last_y)

    X = np.array(X)
    Y = np.array(Y)
    
    return X, Y

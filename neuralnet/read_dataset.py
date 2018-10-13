import numpy as np

def read_dataset(path_to_dataset_file):
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

    indexFile = open(path_to_dataset_file, 'r')
    for sample in indexFile:
        
        
        last_x = []
        last_y = []
        currentNumber = ""
        #last_x.append(1)     # Bias feature
        
        # Values separated by commas
        values = sample.split(",")
        
        for i in range(len(values)-1):
            last_x.append(float(values[i]))

        # Last value is the label
        last_y.append(float(values[len(values)-1]))
        
        # Convert labels to {0,1} format in case they are in {-1,1}
        if(last_y[0]==-1):
            last_y[0]=0

        X.append(last_x)
        Y.append(last_y)
    
    X = np.array(X)
    Y = np.array(Y)

    return X, Y

import tensorflow as tf
import numpy as np
from neuralnet import logistic_model 
from neuralnet import read_dataset 

'''

This function returns tensorflow model for future predictions with unlabeled data

'''
def train_model(traindata_path, implemented_features ,hidden_units, num_iterations, learning_rate):

    # Calculate indices of features to take into account
    feature_indices = []
    for i in range(len(implemented_features)):
        feature_indices.append(implemented_features[i]-1)
        
    # Always include label column
    feature_indices.append(30)
    
    # Load Dataset
    dataset = read_dataset.read_dataset(traindata_path)
    
    # Select only implemented features
    dataset = dataset[:,feature_indices]
    
    # Shuffle dataset
    np.random.shuffle(dataset)


    # Separate 60% Training set / 40% Test Set
    train_test_ratio = 0.6
    trainset_size    = int(np.round(dataset.shape[0] * train_test_ratio))
    testset_size     = dataset.shape[0] - trainset_size

    train_dataset    = dataset[0:trainset_size,:]
    test_dataset     = dataset[trainset_size:,:]
    train_X, train_Y = read_dataset.separate_labels(train_dataset)
    test_X , test_Y  = read_dataset.separate_labels(test_dataset)

    # Network parameters
    input_units   = train_X.shape[1]
    output_units  = 1

    model = logistic_model.logistic_model(input_units, hidden_units, output_units)

    # Build TensorFlow training graph
    model.build_graph(learning_rate)

    # Train model via gradient descent.
    for i in range(num_iterations):
        model.session.run(model.grad_descent, feed_dict={model.X: train_X, model.Y: train_Y})

    train_accuracy = model.session.run(model.accuracy, feed_dict={model.X: train_X, model.Y: train_Y})
    test_accuracy  = model.session.run(model.accuracy, feed_dict={model.X: test_X, model.Y: test_Y})

    test_predict = model.session.run(model.predict, feed_dict={model.X: test_X, model.Y: test_Y})
    print("\nTraining Set accuracy:" , str.format('{0:.3f}', train_accuracy*100), "%")
    print("Test Set accuracy:" , str.format('{0:.3f}', test_accuracy*100), "%")

    return model

import tensorflow as tf
from logistic_model import logistic_model 
from read_dataset import *

# Load training dataset    
X, Y = read_dataset('../data/trainset.csv')

# Network parameters
input_units   = X.shape[1]
hiddent_units = 30
output_units  = 1

# Learning parameters
num_iterations = 100
learning_rate  = 0.5


model = logistic_model(input_units, hiddent_units, output_units)

# Build TensorFlow training graph
model.build_graph(learning_rate)

# Train model via gradient descent.
session = tf.Session()
session.run(tf.global_variables_initializer())

for i in range(num_iterations):
    session.run(model.grad_descent, feed_dict={model.X: X, model.Y: Y})

#predict       = session.run(model.predict, feed_dict={model.X: X})
#round_predict = session.run(model.rounded_prediction, feed_dict={model.X: X})
#mistakes      = session.run(model.mistakes, feed_dict={model.X: X, model.Y: Y})
accuracy       = session.run(model.accuracy, feed_dict={model.X: X, model.Y: Y})
print("Training accuracy:" , str.format('{0:.3f}', accuracy*100), "%")

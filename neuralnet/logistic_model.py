import tensorflow as tf

class logistic_model(object):
    
    def __init__(self, input_units, hidden_units_1, output_units):
        
        self.input_units = input_units
        self.hidden_units_1 = hidden_units_1
        self.output_units = output_units
        
        self.W0_init = tf.random_normal([self.input_units, self.hidden_units_1])-0.5
        self.B0_init = tf.random_normal([1,self.hidden_units_1])-0.5
        self.W1_init = tf.random_normal([self.hidden_units_1, self.output_units])-0.5
        self.B1_init = tf.random_normal([1,self.output_units])-0.5

    
    
    def build_graph(self, learn_rate):
        
        # Placerholders for input data
        self.X = tf.placeholder(tf.float32)
        self.Y = tf.placeholder(tf.float32)
        
        # Model parameters (W - weights , B - Bias)
        self.W0 = tf.Variable(self.W0_init)
        self.B0 = tf.Variable(self.B0_init)
        self.W1 = tf.Variable(self.W1_init)
        self.B1 = tf.Variable(self.B1_init)

        # Feed Forward
        self.forward_1 = tf.add(tf.matmul(self.X, self.W0), self.B0)          # Forward from input to hidden (result is 1xh)
        self.sigmoid_1 = tf.sigmoid(self.forward_1)
        self.forward_2 = tf.add(tf.matmul(self.sigmoid_1, self.W1), self.B1)  # Forward from hidden1 to output
        self.predict   = tf.sigmoid(self.forward_2)                           # Sigmoid activation on output to get final result (Phishin probability)
        
        # Optimization
        self.loss = tf.losses.sigmoid_cross_entropy(self.Y, self.predict)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learn_rate)
        self.grad_descent = self.optimizer.minimize(self.loss)

        # Training Set accuracy
        self.rounded_prediction = tf.round(self.predict)
        self.mistakes           = tf.abs(self.rounded_prediction - self.Y)
        self.mistake_fraction   = tf.reduce_sum(self.mistakes)/tf.to_float(tf.size(self.mistakes))
        self.accuracy           = 1.0 - self.mistake_fraction

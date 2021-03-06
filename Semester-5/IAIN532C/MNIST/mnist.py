import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from matplotlib import pyplot as plt

class MNIST_Model:
    def __init__(self):
        old_v = tf.logging.get_verbosity()
        tf.logging.set_verbosity(tf.logging.ERROR)
        '''Download the dataset from http://yann.lecun.com/exdb/mnist/ and put the .gz files in MNIST_data/'''
        self.mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
        tf.logging.set_verbosity(old_v)
        print('Total training images: {}'.format(len(self.mnist.train.images)))

    def train(self, batch_size=100, learning_rate=.5, batches=2000):
        x = tf.placeholder(tf.float32, shape=[None, 784])
        y = tf.placeholder(tf.float32, shape=[None, 10])

        W1 = tf.Variable(tf.random_normal([784, 50], stddev=.1))
        b1 = tf.Variable(tf.random_normal([50], stddev=.1))
        hidden = tf.nn.relu(tf.add(tf.matmul(x, W1), b1))

        W2 = tf.Variable(tf.random_normal([50, 10], stddev=.1))
        b2 = tf.Variable(tf.random_normal([10], stddev=.1))
        y_ = tf.nn.softmax(tf.add(tf.matmul(hidden, W2), b2))

        loss = tf.reduce_mean(-tf.reduce_sum((y * tf.log(y_)), axis=1))
        train = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

        # y_ = tf.matmul(hidden, W) + b
        # loss = tf.losses.softmax_cross_entropy(y, y_)
        # train = tf.train.AdamOptimizer().minimize(loss)
        
        prediction = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(prediction, tf.float32))

        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)
            for num in range(1, batches+1):
                batch_x, batch_y = self.mnist.train.next_batch(batch_size)
                _, acc = sess.run([train, accuracy], feed_dict={x: batch_x, y: batch_y})
                print('Batch {}/{}: {}'.format(num, batches, acc))
            self.W1, self.b1, self.W2, self.b2 = sess.run([W1, b1, W2, b2])
            self.accuracy = self._accuracy()

    def predict(self, batch_x):
        x = tf.placeholder(tf.float32, shape=[None, 784])
        W1 = self.W1
        b1 = self.b1
        hidden = tf.nn.relu(tf.add(tf.matmul(x, W1), b1))
        
        W2 = self.W2
        b2 = self.b2
        y_ = tf.nn.softmax(tf.add(tf.matmul(hidden, W2), b2))

        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)
            return sess.run(tf.argmax(y_, 1), feed_dict={x: batch_x})

    def _accuracy(self):
        images, labels = model.mnist.test.images, model.mnist.test.labels
        labels = np.array(list(map(lambda x: list(x).index(1), labels)))
        predicted = model.predict(images)
        return 1.*np.count_nonzero(predicted == labels)/len(labels)
        return acc

model = MNIST_Model()
model.train()
print('Accuracy: {}'.format(model.accuracy))

x = model.mnist.test.images[:9]
y = model.predict(x)
print(y)
for i,im in zip(range(len(x)),x):
    plt.subplot(3, 3, i+1)
    plt.imshow(im.reshape(28,28))
plt.show()

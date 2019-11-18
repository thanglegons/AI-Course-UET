# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        list_c_acc = []
        for C in Cgrid:
            for iteration in range(self.max_iterations):
                #Training phase
                print "Starting iteration ", iteration, "..."
                for i in range(len(trainingData)):
                    # Calculate score for each label
                    predicted_score = util.Counter()
                    for label in self.legalLabels:
                        predicted_score[label] = trainingData[i].__mul__(self.weights[label])

                    predicted_label = predicted_score.argMax()
                    correct_label = trainingLabels[i]
                    
                    toco = (self.weights[predicted_label].__sub__(self.weights[correct_label]).__mul__(trainingData[i]) + 1.0) / (2.0 * trainingData[i].__mul__(trainingData[i]))

                    toco = min(C, toco)
                    # toco = 1

                    coef_feature = util.Counter()
                    for feature in self.features:
                        coef_feature[feature] = trainingData[i][feature] * toco

                    # Update weights
                    if predicted_label != correct_label:
                        self.weights[predicted_label] = self.weights[predicted_label].__sub__(coef_feature)
                        self.weights[correct_label].__radd__(coef_feature)
                        
            #Validation phase
            accuracy = 0
            print(len(validationData))
            for i in range(len(validationData)):
                predicted_score = util.Counter()
                for label in self.legalLabels:
                    predicted_score[label] = validationData[i].__mul__(self.weights[label])
                predicted_label = predicted_score.argMax()
                correct_label = validationLabels[i]
                print predicted_label, correct_label
                accuracy += (predicted_label == correct_label)
            
            list_c_acc.append((accuracy, self.weights))
        
        list_c_acc = sorted(list_c_acc, reverse=True)
        print([x[0] for x in list_c_acc])
        self.weights = list_c_acc[0][1]
        
                

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses



#This is the "3 Layer Network" near the bottom of: 
#http://iamtrask.github.io/2015/07/12/basic-python-network/

#First, housekeeping: import numpy, a powerful library of math tools.
5 import numpy as np

#1 Sigmoid Function: changes numbers to probabilities and computes confidence to use in gradient descent
8 def nonlin(x,deriv=False):
9   if(deriv==True):
10    return x*(1-x)
11  
12  return 1/(1+np.exp(-x))

#2 The X Matrix: This is the responses to our survey from 4 of our customers, 
#in language the computer understands.  Row 1 is the first customer's set of 
#Yes/No answers to the first 3 of our survey questions: 
#"1" means Yes to, "Have cat who poops?" The "0" means No to "Drink imported beer?"
#The 1 for "Visited the LitterRip.com website?" means Yes.  There are 3 more rows
#(i.e., 3 more customers and their responses) below that.  
#Got it?  That's 4 customers and their Yes/No responses 
#to the first 3 questions (the 4th question is used in the next step below).  
#These are the set of inputs that we will use to train our network.
23 X = np.array([[1,0,1],
24               [0,1,1],
25               [0,0,1],
26               [1,1,1]])
#3The y Vector: Our testing set of 4 target values. These are our 4 customers' Yes/No answers 
#to question four of the survey, "Actually purchased Litter Rip?"  When our neural network
#outputs a prediction, we test it against their answer to this question 4, which 
#is what really happened.  When our network's
#predictions compare well with these 4 target values, that means the network is 
#accurate and ready to take on our second dataset, i.e., predicting whether our 
#hot prospects from the (hot) veterinarian will buy Litter Rip!
34 y = np.array([[1],
35               [1],
36               [0],
37               [0]])
#4 SEED: This is housekeeping. One has to seed the random numbers we will generate
#in the synapses during the training process, to make debugging easier.
40 np.random.seed(1)
#5 SYNAPSES: aka "Weights." These 2 matrices are the "brain" which predicts, learns
#from trial-and-error, then improves in the next iteration.  If you remember the 
#diagram of the curvy red bowl above, syn0 and syn1 are the 
#X and Y axes on the white grid under the red bowl, so each time we tweak these 
#values, we march the grid coordinates of Point A (think, "moving the yellow arrow")
#towards the red bowl's bottom, where error is near zero.
47 syn0 = 2*np.random.random((3,4)) - 1 # Synapse 0 has 12 weights, and connects l0 to l1.
48 syn1 = 2*np.random.random((4,1)) - 1 # Synapse 1 has 4 weights, and connects l1 to l2.

#6 FOR LOOP: this iterator takes our network through 60,000 predictions, 
#tests, and improvements.
52 for j in range(60000):

  #7 FEED FORWARD: Think of l0, l1 and l2 as 3 matrix layers of "neurons" 
  #that combine with the "synapses" matrices in #5 to predict, compare and improve.
  # l0, or X, is the 3 features/questions of our survey, recorded for 4 customers.
57  l0=X
58  l1=nonlin(np.dot(l0,syn0))
59  l2=nonlin(np.dot(l1,syn1))

  #8 The TARGET values against which we test our prediction, l2, to see how much 
  #we missed it by. y is a 4x1 vector containing our 4 customer responses to question
  #four, "Did you buy Litter Rip?" When we subtract the l2 vector (our first 4 predictions)
  #from y (the Actual Truth about who bought), we get l2_error, which is how much 
  #our predictions missed the target by, on this particular iteration.
66  l2_error = y - l2

  #9 PRINT ERROR--a parlor trick: in 60,000 iterations, j divided by 10,000 leaves 
  #a remainder of 0 only 6 times. We're going to check our data every 10,000 iterations
  #to see if the l2_error (the yellow arrow of height under the white ball, Point A)
  #is reducing, and whether we're missing our target y by less with each prediction.
72  if (j% 10000)==0:
73    print("Avg l2_error after 10,000 more iterations: "+str(np.mean(np.abs(l2_error))))



#10 This is the beginning of back propagation.  All following steps share the goal of 
  # adjusting the weights in syn0 and syn1 to improve our prediction.  To make our 
  # adjustments as efficient as possible, we want to address the biggest errors in our weights.  
  # To do this, we first calculate confidence levels of each l2 prediction by
  # taking the slope of each l2 guess, and then multiplying it by the l2_error.  
  # In other words, we compute l2_delta by multiplying each error by the slope 
  # of the sigmoid at that value.  Why?  Well, the values of l2_error that correspond 
  # to high-confidence predictions (i.e., close to 0 or 1) should be multiplied by a 
  # small number (which represents low slope and high confidence) so they change little.
  # This ensures that the network prioritizes changing our worst predictions first, 
  # (i.e., low-confidence predictions close to 0.5, therefore having steep slope). 
88  l2_delta = l2_error*nonlin(l2,deriv=True)

  #11 BACK PROPAGATION, continued: In Step 7, we fed forward our input, l0, through 
  #l1 into l2, our prediction. Now we work backwards to find what errors l1 had when
  #we fed through it.  l1_error is the difference between the most recent computed l1 
  #and the ideal l1 that would provide the ideal l2 we want.  To find l1_error, we 
  #have to multiply l2_delta (i.e., what we want our l2 to be in the next iteration) 
  #by our last iteration of what we *thought* were the optimal weights (syn1). 
  # In other words, to update syn0, we need to account for the effects of 
  # syn1 (at current values) on the network's prediction.  We do this by taking the 
  # product of the newly computed l2_delta and the current values of syn1 to give 
  # l1_error, which corresponds to the amount our update to syn0 should change l1 next time.
100  l1_error = l2_delta.dot(syn1.T)
  #12 Similar to #10 above, we want to tweak this 
  #middle layer, l1, so it sends a better prediction to l2, so l2 will better 
  #predict target y.  In other words, tweak the weights in order to produce large 
  #changes in low confidence values and small changes in high confidence values.

  #To do this, just like in #10 we multiply l1_error by the slope of the 
  #sigmoid at the value of l1 to ensure that the network applies larger changes 
  #to synapse weights that affect low-confidence (e.g., close to 0.5) predictions for l1.
109  l1_delta = l1_error * nonlin(l1,deriv=True)

  #13 UPDATE SYNAPSES: aka Gradient Descent. This step is where the synapses, the true
  #"brain" of our network, learn from their mistakes, remember, and improve--learning!
  # We multiply each delta by their corresponding layers to update each weight in both of our 
  #synapses so that our next prediction will be even better.
115  syn1 += l1.T.dot(l2_delta)
116  syn0 += l0.T.dot(l1_delta)

#Print results!
119 print("Our y-l2 error value after all 60,000 iterations of training: ")
120 print(l2)
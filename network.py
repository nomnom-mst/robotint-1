import numpy as np
import neuron
import glob
from PIL import Image
import sys

## parameter
repeatNum = 1000
m_num = 10
out_num = 6
noiseProb = 0.1

## get noise
argvs = sys.argv
argc = len(argvs)

if (argc == 1):
    noiseProb = 0
elif (argc == 2):
    noiseProb = float(argvs[1])
else:
    print "Please input noise probability!"
    quit()

## define noise generator function
def NoiseGenerator(data):
    noise = 255 * np.random.rand()
    prob = np.random.rand()
    if prob > 1-noiseProb:
        data = noise
    return data

## initial dummy data
_input = np.random.rand(100)
w = np.random.normal(0,0.1,size=(m_num,100)) 
wo = np.random.normal(0,0.1,size=(out_num,m_num))
answer = [[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]

##loading teacher image  --- OK
images = []
for name in glob.glob('image/*.jpg'):
    images.append(Image.open(name).convert('L').getdata())
    print name


##initial setting --- OK
print 'initialize'
nInput = []
nMiddle = []
nOutput = []
for i in range(100):
    nInput.append( neuron.InputNeuron(_input[i]) )
    
for j in range(m_num):
    nMiddle.append(neuron.Neuron(1.0))
    for k in range(100):
        nMiddle[j].connect(nInput[k],w[j][k])

for j in range(out_num):
    nOutput.append(neuron.Neuron(1.0))
    for k in range(m_num):
        nOutput[j].connect(nMiddle[k],wo[j][k])
    print nOutput[j].output() ####Printing initial output


##learning --OK
print 'learning now'
temp = 0
count = 0
for k in range(repeatNum):
    for j,image in enumerate(images):
        
    ### new data loading--OK
        for i,data in enumerate(image):
            nInput[i].refreshdata(data/255.0)
      
    ### delta --too small
        diff = []
        for i in range(out_num):
            diff.append(nOutput[i].output() - answer[j][i])
            nOutput[i].generateDelta(diff[i])
            
        for neu in nMiddle :
            neu.calculateDelta()

    ###learning---maybe OK
        for neu in nOutput :
            neu.update()
                    
    ###BPLearning
        for neu in nMiddle:
            neu.update()

    ##evaluation
        for d in diff:
            temp += d**2
            count += 1

        eva = np.sqrt(temp) / count
        print eva
        if (eva < 0.001):
            break
    if (eva < 0.001):
        break
    execute_count = k+1


print 'finish learning'
print "eva =", eva
print "count =", execute_count

##test---OK
print 'test now'
for image in images:
    result = []

    for i ,data in enumerate(image):
        data = NoiseGenerator(data) ###plus noise on data
        nInput[i].refreshdata(data)

    for i in range(out_num):
        result.append(nOutput[i].output())
    print result

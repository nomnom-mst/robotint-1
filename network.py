import numpy as np
import neuron


_input[i] = np.random.rand(100)
answer[out_num] = [hoge]
w[k] = np.random.rand(100);
wo[k] = np.random.rand(100);

m_num = 50
out_num = 6

##initial setting
for i in range(100):
    ni[i] = neuron.InputNeuron(_input[i])

for j in range(m_num):
    nm[j] = neuron.Neuron()
    for k in range(100):
        nm[j].connectPrev(ni[k],w[k])
        ni[k].connectNext(nm[j],w[k])

for j in range(out_num):
    no[j] = neuron.Neuron()
    no[j].generateDelta
    for k in range(m_num):
        no[j].connectPrev(nm[k],wo[k])
        nm[k].connectNext(no[j],wo[k])

for j in range(m_num):
    nm[j].calculateDelta

##learnig
for i in range(out_num):
    no[i].update( no[i].output - answer[j] )

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
def saveFile(list, fname):
	with open(fname,"w") as f:
		for column in list:
			for i in range (0,column.__len__()):
				if i!=column.__len__()-1:
					f.write(str(column[i])+",")
				else:
					f.write(str(column[i]))
			
			f.write("\n")
			
	f.close()

labels = np.array([0]*700 + [1]*700 + [2]*700)

one_hot_labels = np.zeros((2100, 3))
print (one_hot_labels)

for i in range(2100):
    one_hot_labels[i, labels[i]] = 1

print (one_hot_labels)

saveFile(one_hot_labels,"label_set.txt")
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(41)
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
	
cat_images = np.random.randn(700, 2) + np.array([0, -3])
mouse_images = np.random.randn(700, 2) + np.array([3, 3])
dog_images = np.random.randn(700, 2) + np.array([-3, 3])

feature_set = np.vstack([cat_images, mouse_images, dog_images])

saveFile(feature_set,"feature_gen_set.txt")
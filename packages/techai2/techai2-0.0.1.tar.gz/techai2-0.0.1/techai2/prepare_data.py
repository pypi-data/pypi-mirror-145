import time
import random
import numpy as np
def set_data(X, Y, batch_size, shake_data):
    X = np.array(X)
    Y = np.array(Y)
    if len(X) != len(Y):
        print("TechAI.Error: Data(X) and Data(Y) in't same Length")
    try:
        X = X.tolist()
    except:
        pass
    try:
        Y = Y.tolist()
    except:
        pass
    new_x = []
    new_y = []
    for x in range(len(X)):
        new_x.append(X[x])
        new_y.append(Y[x])
    new_x = np.array(new_x)
    new_y = np.array(new_y)
    shaked_x = []
    shaked_y = []
    quick_list = []
    if shake_data == True:
        for x in range(len(X)):
            quick_list.append(x)
        for x in range(len(X)):
            nr = random.choice(quick_list)
            quick_list.remove(nr)
            shaked_x.append(X[nr])
            shaked_y.append(Y[nr])
        new_x = np.array(shaked_x)
        new_y = np.array(shaked_y)
    X = new_x.copy()
    Y = new_y.copy()
    batch_X = []
    batch_Y = []
    bufor_x = []
    bufor_y = []
    nr = 0
    counter = len(X)
    while counter > 0:
        for x in range(batch_size):
            bufor_x.append(X[nr])
            bufor_y.append(Y[nr])
            counter -= 1
            nr += 1
            if counter == 0:
                break
        batch_X.append(bufor_x.copy())
        batch_Y.append(bufor_y.copy())
        bufor_x = []
        bufor_y = []
    new_x_b = []
    new_y_b = []
    for batch in batch_X:
        new_x_b.append(np.array(batch))
    for batch in batch_Y:
        new_y_b.append(np.array(batch))
    return new_x_b, new_y_b
    pass






























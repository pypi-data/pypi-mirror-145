# -1NeuronPerceptron_Pypi
 1Neuron|Perceptron|_Pypi

 """
author: Nazmul 
email: md.nazmul.islam0087@gmail.com
"""


## How to use this

## First install the library using below command by using latest version-

```bash

pip install 1NeuronPerceptron-Pypi-mdnazmulislam0087==0.0.4

```
## Run the below code to see the training and plot file for or Gate, similarly you can use AND, NAND and XOR GATE to see the difference-

```python





from oneNeuronPerceptron.perceptron import Perceptron
from oneNeuronPerceptron.all_utils import prepare_data, save_model, save_plot


import pandas as pd
import numpy as np
import logging
import os 

logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=logging_str)



def main(data, eta, epochs, modelfilename,plotfilename):
    df = pd.DataFrame(data)
    logging.info(f"The dataframe is : {df}")
    X,y = prepare_data(df)
    model = Perceptron(eta=eta, epochs=epochs)
    model.fit(X, y)

    _ = model.total_loss()

    save_model(model, filename=modelfilename)
    save_plot(df, file_name=plotfilename, model=model)

if __name__=="__main__": # << entry point <<
    OR = {
        "x1": [0,0,1,1],
        "x2": [0,1,0,1],
        "y": [0,1,1,1],
    }
    
    ETA = 0.3 # 0 and 1
    EPOCHS = 10
    
    
    
    
    try:
        logging.info(">>>>> starting training >>>>>")
        main(data=OR, eta=ETA, epochs=EPOCHS, modelfilename="or.model", plotfilename="or.png")
        logging.info("<<<<< training done successfully<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e  
```
# Packages required-
1. matplotlib
2. numpy
3. pandas
4. joblib
5. tqdm

# Limitation
Using one Neuron Perceptron, We cant make decision boundary for XOR GATe, In summary XOR Gate classification is not possible using one Neuron Perceptron

 # Reference -
[official python docs](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/guides/building-and-testing-python#publishing-to-package-registries)

[Read me editor](https://readme.so/editor)

# more details can be found
[1Neuron Perceptron](https://github.com/mdnazmulislam0087/1NeuronPerceptron)



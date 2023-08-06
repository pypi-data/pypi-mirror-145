"""
author: Nazmul 
email: md.nazmul.islam0087@gmail.com
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib # FOR SAVING MY MODEL AS A BINARY FILE
from matplotlib.colors import ListedColormap
import os
import logging

plt.style.use("fivethirtyeight") # THIS IS STYLE OF GRAPHS



# prepare data
def prepare_data(df):
  """ This is used to separate the dependent and independent columns/features

  Args:
      df (pd.DataFrame): input is the pandas DataFrame 

  Returns:
      tuple: This returns the dependent and independent columns/features
  """
  logging.info("Preparing the data by segregating the independent and dependent variables")
  X = df.drop("y", axis=1)
  y = df["y"]
  return X, y


# save model
def save_model(model, filename):
  """ This is used to save the model in binary format.

  Args:
      model (python object): Trained Model
      filename (filename): File name of the model that to be saved
  """
  logging.info("saving the trained model")
  model_dir = "models"
  os.makedirs(model_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  filePath = os.path.join(model_dir, filename) # model/filename
  joblib.dump(model, filePath)
  
  logging.info(f"saved the trained model {filePath}")
  

# Save plot  
def save_plot(df, file_name, model):
  """This is used to save the plot of the model

  Args:
      df (Pandas Dataframe): This is the dataframe
      file_name (object): Name of the file to be saved
      model (object): model name that is Trained
  """
  logging.info("saving the Plot and Decision boudary")
  def _create_base_plot(df):
    logging.info("creating the base plot")
    df.plot(kind="scatter", x="x1", y="x2", c="y", s=100, cmap="winter")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8)

  def _plot_decision_regions(X, y, classfier, resolution=0.02):
    logging.info("plotting the decision regions")
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])

    X = X.values # as a array
    x1 = X[:, 0] 
    x2 = X[:, 1]
    x1_min, x1_max = x1.min() -1 , x1.max() + 1
    x2_min, x2_max = x2.min() -1 , x2.max() + 1  

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), 
                           np.arange(x2_min, x2_max, resolution))
    logging.info(xx1)
    logging.info(xx1.ravel())
    Z = classfier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    plt.plot()
    


  X, y = prepare_data(df)

  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  plotPath = os.path.join(plot_dir, file_name) # model/filename
  plt.savefig(plotPath)
  logging.info(f"saved the plot in  {plotPath}")
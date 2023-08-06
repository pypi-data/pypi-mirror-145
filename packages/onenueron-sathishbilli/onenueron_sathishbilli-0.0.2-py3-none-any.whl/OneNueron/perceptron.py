import numpy as np
from logging import error
class Perceptron:
  def __init__(self,eta,epochs):
    self.weights=np.random.randn(3)*(10^-4) #initialize the weights
    print(f"initiali weights :{self.weights}")
    self.eta=eta#learning rate
    self.epochs=epochs

  def activationfunctions(self,inputs,weights):

    z=np.dot(inputs,weights)
    return np.where(z<0,0,1)
    self.inputs=inputs
    self.weights=weights

  def fit(self,x,y):
    self.x=x
    self.y=y

    x_with_bias=np.c_[self.x,-np.ones((len(self.x),1))]# concat the bias into input
    print(f"x_with_bias :{x_with_bias}")

    for epoch in range(self.epochs):
      print('----'*10)
      print(f" for epoch {epoch}")
      print('----'*10)

      y_hat=self.activationfunctions(x_with_bias,self.weights)#forward propagation
      i=0
      if y==y_hat:
        i+=1

      


      print(f"y_hat :\n{y_hat}")
      print('#'*20)
      print(f"accuracy :\n{i/4}")


      self.error=self.y-y_hat
      self.update_weights=[]
      
      print(f"error :{self.error}")

      
      print()

      self.weights=self.weights+self.eta+np.dot(x_with_bias.T,self.error)#backward propagation
      self.update_weights.append(self.weights)
      print(f"update weights afer epoch:\n{epoch}/{self.epochs} : \n{self.weights}")
      print('*****'*10)
      if self.error[0]==0 and self.error[1]==1 and self.error[2]==1 and self.error[3]==1:
         print(f" our best weight values :{self.update_weights}")

      


  def predict(self,x):


    x_with_bias=np.c_[self.x,-np.ones((len(self.x),1))]# concat the bias into input
    return  self.activationfunctions(x_with_bias,self.weights)

  def total_loss(self):
    total_loss=np.sum(self.error)
    print(f"total_loss :{total_loss}")
    return total_loss  
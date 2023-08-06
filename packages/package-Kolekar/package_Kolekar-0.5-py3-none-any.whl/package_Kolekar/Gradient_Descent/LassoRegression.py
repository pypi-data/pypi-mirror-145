from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class LassoRegressionModel:
      def __init__(self,learning_rate,max_iter,l1_penalty):
          """
            Return with Learning Rate and max_iter.
            
                 Learning Rate (float) = rang varies from (0.4,0.001)
                 max_iter       (int)  = range varies from (0,1,00,000)
                 l1_penality    (int)  = range varies from (1,200)
            Parameters:
            -----------
            
            Returns:
            -----------
                  Define a type of model which user want to use.
          """
          self.learning_rate = learning_rate
          self.max_iter      = max_iter
          self.l1_penalty    = l1_penalty
        
      def data_preparation(self,dataset):
          '''Returns with Feature vectors of independent feature and Target Feature.
                Parameters:
                        dataset (Table format)
                        X (DataFrame)   : Independent Feature Vector
                        y (Dataframe)   : Dependent Feature Vector

                Returns:
                        X,y
                Methods:
                ----------
                raw_data = dy.iloc[:,:-1]
                time     = dy.iloc[:,-1].values.reshape(-1,1)
          ''' 
          self.dataset  = dataset
          self.X        = self.dataset.iloc[:,:-1]
          self.y        = self.dataset.iloc[:,-1]
          return self.X, self.y    
   
      def data_normalization(self,dataset):
          '''Returns with Feature vectors of independent feature and Target Feature.
                Parameters:
                ----------
                        dataset (Table format)
                        X (DataFrame)   : Independent Feature Vector
                        y (Dataframe)   : Dependent Feature Vector
                        MinMaxScaler()  :(scaler used with feature_range =(0.0,1.1))
                        
                Returns:
                ----------
                        X_scaled,y_scaled
                        
                Methods:
                ----------
                  from sklearn.preprocessing import MinMaxScaler
                  scaled1 = MinMaxScaler(feature_range=(0.1, 1.1))
                  scaled2 = MinMaxScaler(feature_range=(0.1, 1.1))
                  X_scaled  = scaled1.fit_transform(raw_data)
                  y_scaled = scaled2.fit_transform(time)
          '''
          self.dataset = dataset
          self.X,self.y = self.data_preparation(self.dataset)
        
          self.X = self.X.values
          self.y = self.y.values.reshape(-1,1)
        
          self.scaled  = MinMaxScaler(feature_range=(0.1, 1.1))
          self.scaled1 = MinMaxScaler(feature_range=(0.1, 1.1))
          
          self.X_scaled  = self.scaled.fit_transform(self.X)
          self.y_scaled  = self.scaled1.fit_transform(self.y)
            
          self.y_scaled  = self.y_scaled.reshape(-1)
        
          return self.X_scaled,self.y_scaled

      def data_split_train_test(self,sample_X,sample_y): 
          '''Returns with train test split using independent and dependent feature vectors.
                Parameters:
                ----------
                        dataset (Table format)
                        X_scaled (DataFrame)   : Independent Feature Vector
                        y_scaled (Dataframe)   : Dependent Feature Vector

                        
                Returns:
                ----------
                         X_train,X_test,y_train,y_test
                        
                Methods:
                ----------

          '''
          self.sample_X = sample_X
          self.sample_y = sample_y
          self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.sample_X,self.sample_y,train_size=0.8,random_state=42)
          return self.X_train, self.X_test, self.y_train, self.y_test
        
      def data_split_train_test(self,sample_X,sample_y): 
          '''Returns with train test split using independent and dependent feature vectors.
                Parameters:
                ----------
                        dataset (Table format)
                        X_scaled (DataFrame)   : Independent Feature Vector
                        y_scaled (Dataframe)   : Dependent Feature Vector

                        
                Returns:
                ----------
                         X_train,X_test,y_train,y_test
                        
                Methods:
                ----------

          '''
          self.sample_X = sample_X
          self.sample_y = sample_y
          self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.sample_X,self.sample_y,train_size=0.8,random_state=42)
          return self.X_train, self.X_test, self.y_train, self.y_test
        
      def get_fit(self,X,y):
          '''Returns with Feature vectors of independent feature and Target Feature.
                Parameters:
                        dataset (Table format)
                        X (DataFrame)   : Independent Feature Vector
                        y (Dataframe)   : Dependent Feature Vector

                Returns:
                        X,y
                Methods:
                ----------
                raw_data = dy.iloc[:,:-1]
                time     = dy.iloc[:,-1].values.reshape(-1,1)
          '''
          self.X = X
          self.y = y
          self.y = np.array(self.y).reshape(-1)
          self.m = self.X.shape[0]
          self.n = self.X.shape[1]
          self.w = np.ones(self.n)
          self.b = 0
          for i in range(0,self.max_iter+1,1):
                 self.update_weights()
          return self
   
      def update_weights(self):
          """
            Parameters:
            -----------
            
            Returns:
            -----------
                  X : Set of independent variables
                  y : Set of Dependent variable.
          """
          self.y_pred = self.predict(self.X)
          
          self.dw = (2/self.m)*(-self.X.T.dot(self.y-self.y_pred)+self.w*self.l1_penalty)
          self.db = -(2/self.m)*sum(self.y-self.y_pred)
          self.w = self.w-self.learning_rate*self.dw
          self.b = self.b-self.learning_rate*self.db
          return self
     
      def predict(self,X):
          """
          Returns:
          ------------
               y_pred    : dtype(float)  :  Predicted output from assigned variable X
          """
          return X.dot(self.w)+self.b
    
      def performance_evaluation(self,true,pred):
            '''Returns with performance_evaluation. 
                Parameters:
                ----------
                true : actual value
                pred : predicted value
                Returns:
                ----------
                          mae   :Mean Absolute Error
                          mse   :Mean Square Error
                          rmse  :Root Mean Square Error
                          mape  :Mean Absolute Percentage Error
                          r^2 scores : Coefficient of the Determinations
                        
                Methods:
                ----------
            ''' 
            self.true = np.array(true).reshape(-1)
            self.pred = np.array(pred).reshape(-1)

            self.mae  = np.mean(np.abs(self.true-self.pred))
            self.mse  = np.mean(np.square(self.true-self.pred))
            self.mape = np.mean(np.abs(self.true-self.pred)/self.true)*100
            self.rmse = np.sqrt(self.mse)
            self.r2   = 1-np.mean(np.square(self.true-self.pred))/np.mean(np.square(self.true-np.mean(self.true)))
            return self.mae,self.mse,self.rmse,self.mape,self.r2

print(LassoRegressionModel.__doc__)
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
class Average_weight_Ensemble:

      def __init__(self):
           pass

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
    
      def set_base_models(self):
          '''Returns with base models which initially used for performing individual prediction.
                Parameters:
                ----------
                "rfr" is denoted to RandomForestRegressor()
                "knn" is denoted to KNeighborsRegressor()
                "lr"  is denoted  to LinearRegression() 
                "svr" is denoted  to SVR() Support Vector Regression
                "etr" is denoted  to ExtraTreesRegressor()
                "dt"  is denoted  to DecisionTreeRegressor()
                'abr' is denoted  to AdaBoostRegressor()
                'gbr' is denoted  to GradientBoostingRegressor()
                Returns:
                ----------
                         [('rfr', RandomForestRegressor()),
                         ('knn', KNeighborsRegressor()),
                         ('lr', LinearRegression()),
                         ('svr', SVR()),
                         ('etr', ExtraTreesRegressor()),
                         ('dt', DecisionTreeRegressor()),
                         ('abr', AdaBoostRegressor()),
                         ('gbr', GradientBoostingRegressor())]     
                Methods:
                ----------
          '''
          self.base_model =[]
          self.base_model.append(("rfr",RandomForestRegressor()))
          self.base_model.append(("knn",KNeighborsRegressor()))  
          self.base_model.append(("lr",LinearRegression()))
          self.base_model.append(("svr",SVR()))
          self.base_model.append(("etr",ExtraTreesRegressor()))
          self.base_model.append(("dt",DecisionTreeRegressor()))
          self.base_model.append(('abr',AdaBoostRegressor()))
          self.base_model.append(('gbr',GradientBoostingRegressor()))
          return self.base_model

      def accuracy_filter(self,threshold,base_model,train_X,test_X,train_y,test_y):
            '''Returns with accuracy filter that eliminated low accuracy model affecting performance of individual models.
                Parameters:
                ----------
                threshold  = based on same threshold value low accuracy model will eliminated (default value=0.5)
                base_model = list of the base model suggested to user.
                train_X    = Train X (set of independent feature vector with 80% population)
                test_X     = Test  X (set of independent feature vector with 20% population)
                train_y    = Train y (set of independent feature vector with 80% population)
                test_y     = Test y  (set of dependent feature vector with 20% population)
                Returns:
                ----------
                            model	accuracy
                        0	rfr 	0.758273
                        1	knn 	0.728700
                        2	lr  	0.265320
                        
                Methods:
                ----------
            '''            
            self.list1,self.list2=[],[]
            self.threshold  = threshold
            self.base_model = base_model
            self.train_X    = train_X
            self.test_X     = test_X
            self.train_y    = train_y
            self.test_y     = test_y
            for self.n in self.base_model:
                self.model = self.n[1] 
                self.model.fit(self.train_X,self.train_y)
                self.pred_y  = self.model.predict(test_X)
                self.acc = metrics.r2_score(self.test_y,self.pred_y)
                if self.acc>self.threshold:
                   self.list1.append(self.n[0])
                   self.list2.append(self.acc)
            self.results = pd.DataFrame({"model":self.list1,'accuracy':self.list2})
            return self.results 

      def get_weights(self,threshold,base_model,train_X,test_X,train_y,test_y):
            '''Returns with accuracy filter that eliminated low accuracy model affecting performance of individual models.
                Parameters:
                ----------
                threshold  = based on same threshold value low accuracy model will eliminated (default value=0.5)
                base_model = list of the base model suggested to user.
                train_X    = Train X (set of independent feature vector with 80% population)
                test_X     = Test  X (set of independent feature vector with 20% population)
                train_y    = Train y (set of independent feature vector with 80% population)
                test_y     = Test y  (set of dependent feature vector with 20% population)
                Returns:
                ----------
                        model	accuracy	weights
                    	etr 	0.965471	0.222222
                    	rfr 	0.964405	0.194444
                    	knn 	0.959638	0.166667
                    	gbr 	0.944255	0.138889
                    	dt  	0.933217	0.111111
                    	svr 	0.930786	0.083333
                    	abr 	0.912432	0.055556
                    	lr  	0.863439	0.027778
                        
                Methods:
                ----------
            '''  
            self.threshold  = threshold
            self.base_model = base_model
            self.train_X    = train_X
            self.test_X     = test_X
            self.train_y    = train_y
            self.test_y     = test_y
            self.results = self.accuracy_filter(self.threshold,self.base_model,self.train_X,self.test_X,self.train_y,self.test_y)
            self.results = self.results.sort_values("accuracy",ascending=False)
            self.new     = [self.f for self.f in np.arange(1,self.results.shape[0]+1)]
            self.new.sort(reverse=True) 
            self.results['weights'] = self.new /np.sum(self.new)
            return self.results 
        
      def get_Averaging_technique(self,base_model,train_X,train_y,test_X):
             '''Returns with Averaging technique. The take average of the every base model to predict desired output.
                Parameters:
                ----------
                base_model = list of the base model suggested to user.
                train_X    = Train X (set of independent feature vector with 80% population)
                test_X     = Test  X (set of independent feature vector with 20% population)
                train_y    = Train y (set of independent feature vector with 80% population)
                test_y     = Test y  (set of dependent feature vector with 20% population)
                Returns:
                ----------
                          y_pred_test : It predicted output by considering Test X set of data
                        
                Methods:
                ----------
             ''' 
             self.base_model = base_model
             self.train_X = train_X
             self.test_X  = test_X 
             self.train_y = train_y
             vt = VotingRegressor(estimators=self.base_model)
             vt.fit(self.train_X,self.train_y)
             return vt.predict(self.test_X)
        
      def get_weighted_Avg_technique(self,base_model,train_X,train_y,test_X,weights):
             '''Returns with Averaging technique. The take average of the every base model to predict desired output.
                Parameters:
                ----------
                base_model = list of the base model suggested to user.
                train_X    = Train X (set of independent feature vector with 80% population)
                test_X     = Test  X (set of independent feature vector with 20% population)
                train_y    = Train y (set of independent feature vector with 80% population)
                test_y     = Test y  (set of dependent feature vector with 20% population)
                weights    = Assigne weights to predicted Models.
                Returns:
                ----------
                          y_pred_test : It predicted output by considering Test X set of data
                        
                Methods:
                ----------
             ''' 
             self.base_model = base_model
             self.train_X = train_X
             self.test_X  = test_X 
             self.train_y = train_y
             self.weights  = weights
             vt = VotingRegressor(estimators=self.base_model,weights=self.weights)
             vt.fit(self.train_X,self.train_y)
             return vt.predict(self.test_X)
            
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

print(Average_weight_Ensemble.__doc__)
class Averaging:
    def __init__(self):
        """
        
        Multiple predictions are made for each data point and the average of the 
        predictions from all the models are used to make the final prediction.
        """
        pass

    def set_base_models(self):
          """
          Lets the user set multiple user defined base models. 
          
          Note: The models the user wishes to use have to be imported separately. 
          
          Attributes:
          ----------
          base_model: user defined base models. 
          
          Example
          -------
            >>> base_model =[('rfr', RandomForestRegressor()), 
                             ('knn', KNeighborsRegressor()), ('lr', LinearRegression())]

          """
          import pandas as pd
          import numpy as np
          from sklearn.ensemble import VotingRegressor
          self.base_model =[]

          return print("[('rfr', RandomForestRegressor()), ('knn', KNeighborsRegressor()), ('lr', LinearRegression())]")

    def get_Averaging_technique(self,base_model,train_X,train_y,test_X):

             """
             Averages out the performance of each model and builds
             a new model as output based on the average. 
             
             Parameters
             ----------
             base_model: models set as the base models for averaging.
             train_X: input train data.
             train_y: output train data.
             test_X: input test data.

             Example
             -------
                >>> from tkmt_package.ensemble import weighted_Averaging

                >>> wt = weighted_Averaging()

                >>> summary.weights.values

                >>> ypred_test = wt.get_weighted_Avg_technique(base_model= base_models,
                                                                train_X=x_train,
                                                                train_y= y_train, 
                                                                test_X=x_test, 
                                                                weights= weights1)
                                          
             """
             import pandas as pd
             import numpy as np
             from sklearn.ensemble import VotingRegressor
             self.__base_model = base_model
             self.__train_X = train_X
             self.__test_X  = test_X 
             self.__train_y = train_y
             vt = VotingRegressor(estimators=self.__base_model)
             vt.fit(self.__train_X,self.__train_y)
             return vt.predict(self.__test_X)

Averaging.__doc__

class weighted_Averaging:
    def __init__(self):
          """
        
          All the models are assigned different weights defining the importance of each model
          for prediction and then the predictions are made for each data point and the 
          average of the predictions from all the models are used to make the final prediction.

          """
          pass

    def get_weighted_Avg_technique(self,base_model,train_X,train_y,test_X,weights):
             """
             Averages out the performance of each model based on weights
             and builds a new model as output. 
             
             Parameters
             ----------
             base_model: models set as the base models for averaging.
             train_X: input train data.
             train_y: output train data.
             test_X: input test data.
             weights: weights obtained from the models.

             Example
             -------
                >>> from tkmt_package.ensemble import weighted_Averaging

                >>> wt = weighted_Averaging()

                >>> summary.weights.values

                >>> ypred_test = wt.get_weighted_Avg_technique(base_model= base_models,
                                                                train_X=x_train,
                                                                train_y= y_train, 
                                                                test_X=x_test, 
                                                                weights= weights1)

             """
             import pandas as pd
             import numpy as np
             from sklearn.ensemble import VotingRegressor
             self.__base_model = base_model
             self.__train_X = train_X
             self.__test_X  = test_X 
             self.__train_y = train_y
             self.__weights  = weights
             vt = VotingRegressor(estimators=self.__base_model,weights=self.__weights)
             vt.fit(self.__train_X,self.__train_y)
             return vt.predict(self.__test_X)
      
weighted_Averaging.__doc__

class Rank_weighted:
    def __init__(self):
          """
          Multiple models are trained on the data points and based on the individual accuracy, weights are assigned to those models
          and then predictions are made for each data point and the average of the predictions from all the models are used to make
          the final prediction.
          """
          pass

    def get_weights(self,threshold,base_model,train_X,test_X,train_y,test_y):

            """
            Gives the weights of the user defined models based on their accuracies. 
            
            Parameters
            ----------
            threshold: minimum accuracy expected from the models.
            base_model: models statisfying the threshold. 
            train_X: input train data.
            test_X: input test data.
            train_y: output train data.
            test_y: output test data.
            
            Example
            -------
            >>> from tkmt_package.ensemble import Rank_weighted

            >>> rkwt = Rank_weighted()

            >>> summary = rkwt.get_weights(threshold= 0.5,
                                            base_model= base_models,
                                            train_X= x_train,
                                            test_X= x_test,
                                            train_y= y_train,
                                            test_y= y_test)
                          
            """
            import pandas as pd
            import numpy as np

            self.__list1,self.__list2=[],[]
            for n in base_model:
                self.__model = n[1] 
                self.__model.fit(train_X,train_y)
                self.__pred_y  = self.__model.predict(test_X)
                self.__acc = 1-np.mean(np.square(test_y- self.__pred_y))/np.mean(np.square(test_y-np.mean(test_y)))
                if self.__acc>threshold:
                   self.__list1.append(n[0])
                   self.__list2.append(self.__acc)

            self.__results = pd.DataFrame({"model":self.__list1,'accuracy':self.__list2})
            self.__results = self.__results.sort_values("accuracy",ascending=False)
            self.__new     = [f for f in np.arange(1,self.__results.shape[0]+1)]
            self.__new.sort(reverse=True) 
            self.__results['weights'] = self.__new /np.sum(self.__new)
            return self.__results

    def get_rank_weighted_technique(self,base_model,train_X,train_y,test_X,weights):
             """
             Averages out the performance of each model based on weights
             and builds a new model as output. 
             
             Parameters
             ----------
             base_model: models set as the base models for averaging.
             train_X: input train data.
             train_y: output train data.
             test_X: input test data.
             weights: weights obtained from the models.
             
             Example
             ---------
            >>> from tkmt_package.ensemble import Rank_weighted

            >>> rkwt = Rank_weighted()

            >>> summary = rkwt.get_weights(threshold= 0.5,
                                            base_model= base_models,
                                            train_X= x_train,
                                            test_X= x_test,
                                            train_y= y_train,
                                            test_y= y_test)

            >>> weights1 = summary.weights.values
            >>> ypred_test = rkwt.get_rank_weighted_technique(base_model= base_models,
                                                            train_X=x_train, 
                                                            train_y= y_train,
                                                            test_X=x_test,
                                                            weights= weights1)


             """
             import pandas as pd
             import numpy as np
             from sklearn.ensemble import VotingRegressor

             self.__base_model = base_model
             self.__train_X = train_X
             self.__test_X  = test_X 
             self.__train_y = train_y
             self.__weights  = weights
             vt = VotingRegressor(estimators=self.__base_model,weights=self.__weights)
             vt.fit(self.__train_X,self.__train_y)
             return vt.predict(self.__test_X)

Rank_weighted.__doc__

class votingClassifer:
      def __init__(self,estimator):
          """
          Multiple models are used to make predictions for each data point. 
          The predictions by each model are considered as a ‘vote’. The predictions obtained from the majority
          of the models are used as the final prediction.

          """
          import pandas as pd
          import numpy as np
            
          self.__estimator = estimator
        
      def get_fit(self,X_train,y_train):
          """
          Trains the input(X_train) and output(X_test) data.

          Parameters
          ----------
          X_train: input training data
          y_train: output training data
         
          Example
         —--------
            >>> from tkmt_package.ensemble import votingClassifer
            >>> vc = votingClassifer()
            >>> vc.get_fit(X_train,y_train)

          """
          import pandas as pd
          import numpy as np
          from sklearn.ensemble import VotingClassifier
          self.__X  = X_train
          self.__y  = y_train
          self.__vc = VotingClassifier(estimators=self.__estimator) 
          self.__vc.fit(self.__X,self.__y)
        
      def get_predict(self,X_test):
          """
          Tests the input and output data and makes predictions. 

          Parameters
          ----------
          X_test: input testing data 
         
        Example
        —--------
        >>> from tkmt_package.ensemble import votingClassifer
        >>> vc = votingClassifer()
        >>> y_pred = vc.get_predict(X_test)

          """
          import pandas as pd
          import numpy as np
        
          self.__X_test = X_test
          y_pred = self.__vc.predict(self.__X_test)
          return y_pred

votingClassifer.__doc__
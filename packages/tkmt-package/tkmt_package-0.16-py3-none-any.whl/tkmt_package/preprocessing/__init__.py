class Preprocessing:
    def __init__(self):
          """
          Data preprocessing is done using tools to assign input and output variables,
          data scaling, train test split.

          """
          pass


    def data_preparation(self,dataset):
          """
           Assigns the dependent and the independent variables. 
           
           Parameters
           ----------
           dataset: variable assigned to the dataset.

           Attributes
           ----------
           X: input/dependent variables; returns all columns except the last. 
           y: output/ independent variable; returns the last column only.
           
           Example
           -----------

            >>> from tkmt_package.preprocessing import Preprocessing
            >>> dy = df[['cycle','voltage', 'current', 'temperature']]
            >>> prep = Preprocessing()
            >>> X1,y1= prep.data_preparation(dy)

           
          """
          import pandas as pd
          import numpy as np
          self.__dataset  = dataset
          self.__X        = self.__dataset.iloc[:,:-1]
          self.__y        = self.__dataset.iloc[:,-1]
          return self.__X, self.__y
        
    def data_normalization(self):
          """
          Rescales the data such that all the feature values are in the range 0 to 1.
          
          Attributes
          ----------
          X_scal: scaled dependent variables; 
                  returns all columns except last with its values rescaled between 0 to 1.
                  
          y_scal: scaled independent variables;  
                  returns the last column with its values rescaled between 0 to 1.
          
          Example
          -------
            >>> from tkmt_package.preprocessing import Preprocessing
            >>> prep = Preprocessing()
            >>> X_scal,y_scal = prep.data_normalization()

          
          """
          import pandas as pd
          import numpy as np
          from sklearn.preprocessing import MinMaxScaler

          self.__X,self.__y = self.data_preparation(self.__dataset)
        
          self.__X = self.__X.values
          self.__y = self.__y.values.reshape(-1,1)
        
          self.scaled  = MinMaxScaler(feature_range=(0.1, 1.1))
          self.scaled_y = MinMaxScaler(feature_range=(0.1, 1.1))
          
          self.__X_scaled  = self.scaled.fit_transform(self.__X)
          self.__y_scaled  = self.scaled_y.fit_transform(self.__y)
            
          self.__y_scaled  = self.__y_scaled.reshape(-1)
        
          return self.__X_scaled,self.__y_scaled

    def data_split_train_test(self,sample_X,sample_y):
          """
          Splits the data such that 80% of the data goes for training 
          and 20% of the data goes for testing with the random state as 42.
          
          Parameters
          ----------
          sample_X: input features 
          sample_y: output features

          Attributes
          ----------
          X_train: 80% of the data in X.
          X_test: 20% of the data in X.
          y_train: 80% of the data in y.
          y_test: 20% of the data in y.
          
          Example
          -------
          >>> from tkmt_package.preprocessing import Preprocessing
          >>> prep = Preprocessing()
          >>> X_train,X_test,y_train,y_test = prep.data_split_train_test(X,y)

          """
          import pandas as pd
          import numpy as np
          from sklearn.model_selection import train_test_split

          self.__sample_X = sample_X
          self.__sample_y = sample_y
          self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(self.__sample_X,self.__sample_y,train_size=0.8,random_state=42)
          return self.__X_train, self.__X_test, self.__y_train, self.__y_test

Preprocessing.__doc__
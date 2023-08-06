class Evaluation:
   def performance_evaluation(self,true,pred):
                """
                Shows the performance of the model in terms of accuracy, MAE, MSE, MAPE and RMSE.
                
                Parameters
                ----------
                true: actual test output. 
                pred: predicted test output.
                
                Attributes
                ----------
                y_test: actual test output. 
                y_test_pred: predicted test output

                Example
                -------
                >>> from tkmt_package.evaluation import Evaluation
                >>> eva = Evaluation()
                >>> eva.performance_evaluation(y_test, y_test_pred)
                """
                import numpy as np 
                true = np.array(true).reshape(-1)
                pred = np.array(pred).reshape(-1)

                mae  = np.mean(np.abs(true-pred))
                mse  = np.mean(np.square(true-pred))
                mape = np.mean(np.abs(true-pred)/true)*100
                rmse = np.sqrt(mse)
                r2   = 1-np.mean(np.square(true-pred))/np.mean(np.square(true-np.mean(true)))

                return print("MAE: {}\nMSE: {}\nRMSE: {}\nMAPE: {}\nR^2 score: {}".format(mae,mse,rmse,mape,r2))
          
   def get_plot_regression(self,true,pred,ascending,label):
            """
            Plots the actual vs predicted output graph.

            Parameters
            —----------
            true: actual output
            pred: predicted output
            ascending: reconstructs the dataframe in an ascending or descending order           
            label: true value and predicted value label

            Attributes
            ----------
            y_test: actual test output. 
            y_test_pred: predicted test output.
            
            Example
            -----------
            >>> from tkmt_package.evaluation import Evaluation
            >>> eva = Evaluation()
            >>> true, pred = eva.get_plot_regression(true=y_test, pred=y_test_pred, ascending= False, label= "Discharge_Capacity")


            """
            import pandas as pd
            import numpy as np 
            import matplotlib.pyplot as plt
            
            real = np.array(true).reshape(-1,1)
            y_pred = np.array(pred).reshape(-1,1)

            #real   = self.scaled_y.inverse_transform(true)
            #y_pred = self.scaled_y.inverse_transform(pred)

            dataset = pd.DataFrame({"real":real.reshape(-1),"predict":y_pred.reshape(-1)}).sort_values('real',ascending=ascending)
            datapoints = np.arange(1, dataset.shape[0]+1)
            #print(len(datapoints),dataset.shape)
            plt.figure(figsize=(8,4))
            plt.plot(datapoints,dataset.predict,label= "{} (Pred)".format(label))
            plt.plot(datapoints,dataset.real,label   = "{} (Real)".format(label))
            
            plt.xlim(np.min(datapoints),np.max(datapoints))
            plt.xlabel("Datapoints")
            plt.ylabel("Actual vs Predicted {}".format(label))
            plt.legend()
            plt.grid()
            plt.show()
            return dataset.real,dataset.predict

   def get_plot_classification(self,true,pred,X_labels,y_labels,cmap_index=3,figsize=(10,10),title='VotingClassifier'):
            """
            Plots the confusion matrix.

            Parameters
            —---------
            true: actual output
            pred: predicted output
            X_labels: labels on the x axis             
            y_labels: labels on the y axis 
            cmap_index: 178 possible colour combinations 
            figsize: size of the confusion matrix figure
            title: title of the figure
            
            Example
            -------
            >>> from tkmt_package.evaluation import Evaluation
            >>> eva = Evaluation()
            >>> true, pred = eva.get_plot_classification(true,pred,
                                                         X_labels,
                                                         y_labels,
                                                         cmap_index=3,
                                                         figsize=(10,10),
                                                         title='VotingClassifier')
            """
            import matplotlib.pyplot as plt
            import seaborn as sns
            import numpy as np
            from sklearn import metrics

            self.__m,self.__n= figsize[0],figsize[1]

            self.__Xlabels = X_labels
            self.__ylabels = y_labels
            #self.__dpi     = dpi
            self.__title   = title
            #self.__savefile = savefile

            self.__true = np.array(true).reshape(-1,1)
            self.__pred = np.array(pred).reshape(-1,1)

            cmap=['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap',
                'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r',
                'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r',
                'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples',
                'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r',
                'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia',
                'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot',
                'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 
                'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r',
                'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray',
                'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
                'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r',
                'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet',
                'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 
                'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 
                'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r',
                'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r',
                'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r']
            # cmap has maximum length 178.
            self.__cmap = cmap    
   
            plt.figure(figsize=(self.__m,self.__n))
            cm = metrics.confusion_matrix(self.__true,self.__pred)    

            sns.heatmap(cm,annot=True,
                               cmap=self.__cmap[cmap_index],
                               fmt='g',
                               xticklabels=self.__Xlabels,
                               yticklabels=self.__ylabels)
            plt.title(self.__title)
            
Evaluation.__doc__
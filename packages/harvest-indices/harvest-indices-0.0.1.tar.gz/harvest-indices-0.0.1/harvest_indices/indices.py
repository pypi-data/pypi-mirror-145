# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 16:38:39 2022

@author: Florian Ellsäßer

This package enables the calculation of traditional harvest indices THI (such as 
frequently used by central European farmers), the Standardized Harvest Index SHI 
that we developped to analyze the harvest data base cropdata.de (please check 
cropdata.de/about for more information also about a paper that we are currently
writing) and finally we also implemented the Relative Harvest Index RHI similar 
as e.g. in Ben-Ari et al (2018) and Beillouin et al. (2020). With these indices 
it is possible to analyze harvest anomalies on historical harvest data. 

For questions, bugs and ideas please contact me via info@cropdata.de

If you want to cite this version of the harvest-data package, please do as this:
Florian Ellsäßer, 2022, harvest-indices python package to analyze harvest anomalies, 
https://pypi.org/project/harvest-indices/
We are planning to submit a paper covering the package in detail. 
"""

# import the necessary libraries
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

# This class takes 1D-array data e.g. single columns of a pandas data frame
class HarvestIndices:
    def __init__(self):
        '''This class takes 1D-arrays or Series e.g. single columns of a pandas 
        data frame and calculates the THI, the SHI or the RHI.'''
                
    def getTHI(in_array,prev_years=None):
        '''This method enables the calculation of traditional harvest indices
        THI (that is usually taking the mean of previous years and comparing it 
        with the current harvest productivity). 
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                prev_years (int) =      this variable contains the number of previous
                                        years to be considered as the reference 
                                        for the current harvest year. The input 
                                        should be an int or None if all the years
                                        should be considered.
                                    
        Returns:
                trad_index_values (numpy.ndarray) = This array contains the THI
                                        results
        '''
        # create an instance using the TraditionalHarvestIndex class
        trad_index = TraditionalHarvestIndex(prev_years=prev_years)
        # convert the input data to numpy array 
        new_array = np.array(in_array)
        # get index using the getTHI method of the TraditionalHarvestIndex class
        trad_index_values = trad_index.getTHI(new_array)
               
        return trad_index_values
    
    def getSHI(in_array,classifier=False):
        '''This method enables the calculation of the Standardized Harvest Index
        SHI that relates the current harvest year to previous years by standardizing 
        all the values to a standard distribution. 
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                classifier (boolean) =  this variable contains either a True or 
                                        False value to indicate if the results of 
                                        the SHI should be classified in extreme,
                                        severe or no anomalies
                                    
        Returns:
                std_index_values (numpy.ndarray) = This array contains the SHI
                                        results
        '''
        # create an instance using the StandardizedHarvestIndex class
        std_index = StandardizedHarvestIndex()
        # convert the data to numpy array 
        new_array = np.array(in_array)
        # get index
        std_index_values = std_index.getSHI(new_array,classifier)
            
        return std_index_values
    
    def getRHI(in_array,classifier=False):
        '''This method enables the calculation of the Relative Harvest Index
        RHI that relates the current harvest year to previous years by standardizing 
        all the values to a standard distribution. 
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                classifier (boolean) =  this variable contains either a True or 
                                        False value to indicate if the results of 
                                        the SHI should be classified in extreme,
                                        severe or no anomalies
                                    
        Returns:
                rhi_index_values (numpy.ndarray) = This array contains the SHI
                                        results
        '''
        # create an instance using the RelativeHarvestIndex class
        rhi_index = RelativeHarvestIndex()
        # convert the data to numpy array 
        new_array = np.array(in_array)
        # get index
        rhi_index_values = rhi_index.getRHI(new_array,classifier)
                
        return rhi_index_values
    
class TraditionalHarvestIndex:
    '''This class enables the calculation of traditional harvest indices
        THI (that is usually taking the mean of previous years and comparing it 
        with the current harvest productivity). 
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                prev_years (int) =      this variable contains the number of previous
                                        years to be considered as the reference 
                                        for the current harvest year. The input 
                                        should be an int or None if all the years
                                        should be considered.
                                    
        Returns:
                -
    '''
    def __init__(self,in_array=None,prev_years=None):
        
        self.in_array = in_array
        self.prev_years=prev_years
    
    def getTHI(self,in_array):
        '''This method wraps the other methods below into a workflow to calculate
        the THI index. It first defines the number of previous years if this hasn't
        been done yet, then gets the average of the years of interest, calculates
        the difference of the values to this average and finally standardizes the 
        output.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                prev_years (int) =      this variable contains the number of previous
                                        years to be considered as the reference 
                                        for the current harvest year. The input 
                                        should be an int or None if all the years
                                        should be considered.
                                    
        Returns:
                out_array (numpy.ndarray) = This array contains the THI results
        '''
        
        # get the previous years as a variable
        prev_years = self.prev_years
        
        # if empty array is passed, return the same sized empty array back 
        if np.isnan(in_array).all():
            a = np.empty((1,len(in_array)))
            a[:] = np.nan
            
            return a
        else:
            # check if the prev_years are defined or not
            if self.prev_years == None:
                # if they are not defined run the average for all years
                out_array = self.get_average_all_years(in_array)
                # standardize the output
                out_array = self.standardize(out_array) 
            else:
                # if they are defined, run them for the defined years range 
                out_array = self.get_average_prev_years(in_array, prev_years)
                # standardize the output
                out_array = self.standardize(out_array)    
                
            return out_array
    
    def standardize(self,in_array):
        '''This method standardizes the input array. NaNs are masked off to allow 
        for this procedure.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
        
        Returns:
                out_array (numpy.ndarray) = This array contains the standardized
                                        results
        '''
        # Use a mask to mark the NaNs
        in_array_masked = np.ma.array(in_array, mask=np.isnan(in_array)) 
        # standardize using masked array
        out_array = in_array / np.std(in_array_masked) 
        
        return out_array
    
    def get_average_all_years(self,in_array):
        '''This method gets the mean of the input array and then calculates the 
        difference of the in_array values to this mean.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
        
        Returns:
                out_array (numpy.ndarray) = This array contains the standardized
                                        results
        '''
        # first get the average of all years
        averages_all_years = in_array.mean()
        # now in_array- average
        result = in_array - averages_all_years
        return result
    
    def get_average_prev_years(self, in_array, prev_years):
        '''This method gets the mean of the previous years in the input array and 
        then calculates the difference of the in_array values to this mean.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
        
                prev_years (int) =      this variable contains the number of previous
                                        years to be considered as the reference 
                                        for the current harvest year. 
                                    
        Returns:
                result (numpy.ndarray) = This array contains the THI results
        '''
        # add an extra year to have the actual number of years
        prev_years = prev_years+1
        # first get the moving average of the previous years
        averages_prev_years = self.get_moving_average(in_array, prev_years)
        # now get the difference of in_array and average
        result = in_array - averages_prev_years
        
        return np.array(result)
    
    def get_moving_average(self, in_array, in_prev_years):
        '''This method gets the mean of the previous years using a moving average.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
        
                in_prev_years (int) =   this variable contains the number of previous
                                        years to be considered as the reference 
                                        for the current harvest year. 
                                    
        Returns:
                result_array (numpy.ndarray) = This array contains the means
        '''
        # get the average array using a moving average
        average_array = np.convolve(in_array, np.ones(in_prev_years), 'valid') / in_prev_years
        # get an empty numpy array with the first years -1 
        empty_array = np.array([np.nan]*(in_prev_years-1))
        # concatenate the arrays
        result_array = np.concatenate([empty_array,average_array])
        
        return result_array
           

class StandardizedHarvestIndex:
    '''This class enables the calculation of the Standardized Harvest Index
        SHI.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                classifier (boolean) =  this variable contains either a True or 
                                        False value to indicate if the results of 
                                        the SHI should be classified in extreme,
                                        severe or no anomalies
                                    
        Returns:
                -
    '''
    def __init__(self,in_array=None,classifier=False):
                
        self.in_array = None
        self.classifier = classifier
    
    def getSHI(self,in_array,classifier=False):
        '''This method ties the workflow for the calculation of the SHI together.
        First it is checked whether the classifier variable is set to True, then
        the input array is converted to a standard normal distribution, if the 
        cassifier variable is True, the data is classified into 5 groups.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
        
                classifier (boolean) =  this variable contains either a True or 
                                        False value to indicate if the results of 
                                        the SHI should be classified in extreme,
                                        severe or no anomalies
                                        
        Returns:
                out_array (numpy.ndarray) = This array contains the SHI results.
        '''
        
        # check whether the classifier is set to true or not
        if classifier==True:
            # if it is True, set the objects parameter True too
            self.classifier =True
        else:
            pass
        
        # if empty array is passed, return the same sized empty array back 
        if np.isnan(in_array).all():
            a = np.empty((1,len(in_array)))
            a[:] = np.nan
            
            return a
        else:
            # convert in array to standard normal distribution
            out_array = (in_array - np.mean(in_array))/np.std(in_array)        
            # now check if the classifier is desired and classify 
            if self.classifier == True:
                # run classifier function
                out_array = self.classify_array(out_array)
            else:
                # or else do nothing
                out_array = out_array
                
            return out_array
            
    def classify_array(self,std_yield_anomalies):
        '''This method classifies the standardized yield anomalies into five 
        classes ranging from -2 to 2.
        Parameters: 
                std_yield_anomalies (numpy.ndarray) = 1D input array containing 
                                        the standardized yield anomalies. 
                                        
        Returns:
                std_yield_anomalies (numpy.ndarray) = These are the classified
                                        yield anomalies. 
        '''
        # if bigger than expected
        std_yield_anomalies[(std_yield_anomalies>=1) & (std_yield_anomalies<2)] = 1
        std_yield_anomalies[(std_yield_anomalies>=2)] = 2
        # if regular
        std_yield_anomalies[(std_yield_anomalies<1) & (std_yield_anomalies>(-1))] = 0
        # if lower than expected
        std_yield_anomalies[(std_yield_anomalies<=(-1)) & (std_yield_anomalies>(-2))] = -1
        std_yield_anomalies[(std_yield_anomalies<=(-2))] = -2
            
        return std_yield_anomalies
    
class RelativeHarvestIndex:
    '''This class enables the calculation of the Relative Harvest Index RHI.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). It is very
                                        important that these data are in a yearly
                                        order, starting with the lowest year
                                        and ending with the last year of the record.
        
                classifier (boolean) =  this variable contains either a True or 
                                        False value to indicate if the results of 
                                        the SHI should be classified in extreme,
                                        severe or no anomalies
                                    
        Returns:
                -
    '''
    
    def __init__(self,in_array=None,classifier=False):
        
        self.in_array = None
        self.classifier = classifier
    
    def getRHI(self,in_array, classifier=False):
        '''This method runs the workflow to calculate the RHI. It first checks if 
        a classification is required, then runs a loess regression to get the expected 
        values, then it creates the difference between expected and actual values
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
        
                classifier (boolean) =  this variable contains either a True or 
                                        False value to indicate if the results of 
                                        the SHI should be classified in extreme,
                                        severe or no anomalies
                                        
        Returns:
                out_array (numpy.ndarray) = This array contains the RHI results.
        '''
        
        # check if a classification is required
        if classifier==True:
            self.classifier =True
        else:
            pass
        
        # if empty array is passed, return the same sized empty array back 
        if np.isnan(in_array).all():
            a = np.empty((1,len(in_array)))
            a[:] = np.nan
            
            return a
        else:    
            # make pandas series 
            in_series = pd.Series(in_array)
            # get the loess regression of the value as an array of expected values 
            expected_values = list(self.make_lowess(in_series))
            # now calculate eq.1 from Ben-Ari et al. (2018)
            dataframe = pd.DataFrame({'productivity':list(in_array), 'expected_values':expected_values})
            # calculate the yield anomalies
            dataframe['rel_yield_anomalies'] = (dataframe.productivity-dataframe.expected_values) / dataframe.expected_values
            
            # now check if the classifier is desired and classify 
            if self.classifier == True:
                # run classifier function
                out_array = self.classify_array(dataframe['rel_yield_anomalies'])
            else:
                out_array = dataframe['rel_yield_anomalies']
            return out_array
    
    def make_lowess(self,series):
        '''This method runs a lowess regression and returns the expected values.
        
        Parameters: 
                in_array (1D-array) =   1D input array containing yearly productivity
                                        records usually in (dt/ha). 
                                        
        Returns:
                out_array (pandas.core.series.Series) = This array contains the 
                                        expected results for the harvest.
        '''
        
        # get the values of the series
        endog = series.values
        # get the index values
        exog = series.index.values
        # smoothen by lowess
        smooth = lowess(endog, exog)
        # transpose
        index, data = np.transpose(smooth)
        
        return pd.Series(data, index=index)    

    def classify_array(self,rel_yield_anomalies):
        '''This method classifies the standardized yield anomalies into five 
        classes ranging from -2 to 2.
        Parameters: 
                rel_yield_anomalies (numpy.ndarray) = 1D input array containing 
                                        the standardized yield anomalies. 
                                        
        Returns:
                rel_yield_anomalies (numpy.ndarray) = These are the classified
                                        yield anomalies. 
        '''
        
        # if bigger than expected
        rel_yield_anomalies[(rel_yield_anomalies>=0.15)] = 2
        rel_yield_anomalies[(rel_yield_anomalies>=0.1) & (rel_yield_anomalies<0.15)] = 1
        # if regular
        rel_yield_anomalies[(rel_yield_anomalies<0.1) & (rel_yield_anomalies>(-0.10))] = 0
        # if lower than expected
        rel_yield_anomalies[(rel_yield_anomalies<=(-0.15))] = -2
        rel_yield_anomalies[(rel_yield_anomalies<=(-0.1)) & (rel_yield_anomalies>(-0.15))] = -1
        
        return rel_yield_anomalies

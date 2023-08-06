# designmatrix.py
#
# Create design matrix
#
# This file is part of HectorP 0.0.2.
#
# HectorP is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later 
# version.
#
# HectorP is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with 
# HectorP. If not, see <https://www.gnu.org/licenses/>.
#
#  8/ 2/2019 Machiel Bos, Coimbra
# 29/12/2021 Machiel Bos, Santa Clara
#==============================================================================

import numpy as np
import sys
import math
from hectorp.control import Control
from hectorp.control import SingletonMeta
from hectorp.observations import Observations

#==============================================================================
# Class definitions 
#==============================================================================
    
class DesignMatrix(metaclass=SingletonMeta):

    def __init__(self):
        """Define the class variables
        """
        #--- get Control parameters (singleton)
        control = Control()
        try:
            self.verbose = control.params['Verbose']
        except:
            self.verbose = True

        #--- Get observations (singleton)
        self.ts = Observations()

        #--- small number
        EPS = 1.0e-4
    
        #--- How many periods and offsets do we habe?
        try:
            periodic_signals = control.params['periodicsignals']
        except:
            if self.verbose==True:
                print('No extra periodic signals are included.')
            periodic_signals = []

        if np.isscalar(periodic_signals)==True:
            self.periods = [periodic_signals]
        else:
            self.periods = []
            for i in range(0,len(periodic_signals)):
                self.periods.append(periodic_signals[i])

        #--- length of arrays          
        n_periods = len(self.periods)
        n_offsets = len(self.ts.offsets)
        
        #--- Number of observations
        m = len(self.ts.data.index)
        if m==0:
            print('Zero length of time series!? am crashing...')
            sys.exit()
       
        #--- Remember time halfway between start and end
        self.th = 0.5*(self.ts.data.index[0] + self.ts.data.index[-1])
 
        n = 2 + 2*n_periods + n_offsets
        self.H = np.zeros((m,n))
        for i in range(0,m):
            self.H[i,0] = 1.0
            self.H[i,1] = i - 0.5*(m-1)
            for j in range(0,n_periods):
                self.H[i,2+2*j+0] = \
                   math.cos(2*math.pi*i*self.ts.sampling_period/self.periods[j])
                self.H[i,2+2*j+1] = \
                   math.sin(2*math.pi*i*self.ts.sampling_period/self.periods[j])
            for j in range(0,n_offsets):
                if self.ts.offsets[j]<self.ts.data.index[i]+EPS:
                    self.H[i,2+2*n_periods+j] = 1.0



    def show_results(self,output,theta,error):
        """ Show results from least-squares on screen and save to json-dict

        Args:
            output (dictionary): where the estimate values are saved (json)
            theta (float array) : least-squares estimated parameters
            error (float array) : STD of estimated parameters
        """

        control = Control()
        unit = control.params['PhysicalUnit']
        ds = 365.25

        if self.verbose==True:
            print("bias : {0:.3f} +/- {1:.3f} (at {2:.2f})".format(theta[0],\
							    error[0],self.th))
            print("trend: {0:.3f} +/- {1:.3f} {2:s}/yr".format(theta[1]*ds,\
							    error[1]*ds,unit))
            i = 2
            for j in range(0,len(self.periods)):
                print("cos {0:8.3f} : {1:.3f} +/- {2:.3f} {3:s}".format(\
			    self.periods[j],theta[i],error[i],unit)); i += 1
                print("sin {0:8.3f} : {1:.3f} +/- {2:.3f} {3:s}".format(\
			    self.periods[j],theta[i],error[i],unit)); i += 1
            for j in range(0,len(self.ts.offsets)):
                print("offset at {0:10.4f} : {1:7.2f} +/- {2:5.2f} {3:s}".\
			format(\
		         self.ts.offsets[j],theta[i],error[i],unit)); i += 1

        #--- JSON
        output['trend'] = ds*theta[1]
        output['trend_sigma'] = ds*error[1]
        i = 2
        for j in range(0,len(self.periods)):
            output["cos_{0:.3f}".format(self.periods[j])] = theta[i] 
            output["cos_{0:.3f}_sigma".format(self.periods[j])] = error[i]
            i += 1 
            output["sin_{0:.3f}".format(self.periods[j])] = theta[i] 
            output["sin_{0:.3f}_sigma".format(self.periods[j])] = error[i]
            i += 1 
        output['jump_epochs'] = self.ts.offsets
        output['jump_sizes'] = theta[i:].tolist()
        output['jump_sigmas'] = error[i:].tolist()



    def add_mod(self,theta):
        """ Compute xhat and add it to the Panda Dataframe

        Args:
            theta (array float): contains estimated least-squares parameters

        """

        xhat = self.H @ theta
        self.ts.add_mod(xhat)

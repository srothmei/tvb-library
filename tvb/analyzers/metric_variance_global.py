# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and 
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General 
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Filler analyzer: Takes a TimeSeries object and returns a Float.

.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
.. moduleauthor:: Stuart A. Knock <Stuart@tvb.invalid>

"""

import tvb.analyzers.metrics_base as metrics_base
import tvb.datatypes.time_series as time_series_module
from tvb.basic.logger.builder import get_logger
import tvb.basic.traits.types_basic as basic


LOG = get_logger(__name__)



class GlobalVariance(metrics_base.BaseTimeseriesMetricAlgorithm):
    """
    Zero-centres all the time-series and then calculates the variance over all 
    data points.
    
    Input:
    TimeSeries datatype 
    
    Output: 
    Float
    
    This is a crude indicator of "excitability" or oscillation amplitude of the
    models over the entire network.
    """

    time_series = time_series_module.TimeSeries(
        label="Time Series",
        required=True,
        doc="""The TimeSeries for which the zero centered Global Variance is to
            be computed.""")


    start_point = basic.Float(
        label = "Start point (ms)",
        default =  0.0,
        required = False,
        doc = """The timeseries may have a transient. The start point determines how
              many points of the TimeSeries will be discarded before computing
              the metric. By default it takes the entire TimeSeries""")

    segment = basic.Integer(
        label = "Segmentation factor",
        default = 4,
        required=False,
        doc = """Divide the input time-series into discrete equally sized sequences 
              and use the last one to compute the metric."""
        )
    
    def evaluate(self):
        """
        Compute the zero centered global variance of the time_series. 
        """
        cls_attr_name = self.__class__.__name__ + ".time_series"
        self.time_series.trait["data"].log_debug(owner=cls_attr_name)


        shape = self.time_series.data.shape
        tpts  = self.time_series.data.shape[0]

        if self.start_point != 0.0:
            start_tpt = self.start_point / self.time_series.sample_period
            LOG.debug("Will discard: %s time points" % start_tpt)
        else: 
            start_tpt = 0

        if start_tpt > tpts:
            LOG.waring("The time-series is shorter than the starting point")
            LOG.debug("Will divide the time-series into %d segments." % self.segment)
            # Lazy strategy
            start_tpt = int((self.segment - 1) * (tpts//self.segment))
        
        zero_mean_data = (self.time_series.data[start_tpt:, :] - self.time_series.data[start_tpt:, :].mean(axis=0))
        global_variance = zero_mean_data.var()
        return global_variance  
    
    
    def result_shape(self):
        """
        Returns the shape of the main result of the ... 
        """
        return (1, )
    
    
    def result_size(self):
        """
        Returns the storage size in Bytes of the results of the ... .
        """
        return 8.0  # Bytes
    
    
    def extended_result_size(self):
        """
        Returns the storage size in Bytes of the extended result of the ....
        That is, it includes storage of the evaluated ...
        """
        return 8.0  # Bytes



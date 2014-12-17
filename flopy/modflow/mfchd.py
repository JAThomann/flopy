"""
mfchd module.  Contains the ModflowChd class. Note that the user can access
the ModflowChd class as `flopy.modflow.ModflowChd`.

Additional information for this MODFLOW package can be found at the `Online
MODFLOW Guide
<http://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/index.html?chd.htm>`_.

"""

import numpy as np
from flopy.mbase import Package
from flopy.utils.util_list import mflist

class ModflowChd(Package):
    """
    MODFLOW Constant Head Package Class.

    Parameters
    ----------
    model : model object
        The model object (of type :class:`flopy.modflow.mf.Modflow`) to which
        this package will be added.
    layer_row_column_data : list of records
        In its most general form, this is a triple list of chd records  The
        innermost list is the layer, row, column, shead, and ehead for a single
        chd.  Then for a stress period, there can be a list of chds.  Then
        for a simulation, there can be a separate list for each stress period.
        This gives the form of
            layer_row_column_data = [
                     [  #stress period 1
                       [l1, r1, c1, shead1, ehead1],
                       [l2, r2, c2, shead2, ehead2],
                       [l3, r3, c3, shead3, ehead3],
                       ],
                     [  #stress period 2
                       [l1, r1, c1, shead1, ehead1],
                       [l2, r2, c2, shead2, ehead2],
                       [l3, r3, c3, shead3, ehead3],
                       ], ...
                     [  #stress period kper
                       [l1, r1, c1, shead1, ehead1],
                       [l2, r2, c2, shead2, ehead2],
                       [l3, r3, c3, shead3, ehead3],
                       ],
                    ]
        Note that if there are not records in layer_row_column_data, then the
        last group of chds will apply until the end of the simulation.
    layer_row_column_shead_ehead : list of records
        Deprecated - use layer_row_column_data instead.
    options : list of strings
        Package options. (default is None).
    extension : string
        Filename extension (default is 'chd')
    unitnumber : int
        File unit number (default is 24).
    zerobase : boolean (default is True)
        True when zero-based indices are used: layers, rows, columns start at 0
        False when one-based indices are used: layers, rows, columns start at 1 (deprecated)

    Attributes
    ----------
    mxactc : int
        Maximum number of chds for all stress periods.  This is calculated
        automatically by FloPy based on the information in
        layer_row_column_data.

    Methods
    -------

    See Also
    --------

    Notes
    -----
    Parameters are not supported in FloPy.

    Examples
    --------

    >>> import flopy
    >>> m = flopy.modflow.Modflow()
    >>> lrcd = [[[2, 3, 4, 10., 10.1]]]  #this chd will be applied to all
    >>>                                  #stress periods
    >>> chd = flopy.modflow.ModflowChd(m, layer_row_column_data=lrcd)

    """
    def __init__(self, model, stress_period_data=None,dtype=None,
                 cosines=None, extension ='chd', unitnumber=24):
        # Call ancestor's init to set self.parent, extension, name and unit number
        Package.__init__(self, model, extension, 'CHD', unitnumber)
        self.url = 'chd.htm'
        self.heading = '# CHD for MODFLOW, generated by Flopy.'

        if dtype is not None:
            self.dtype = dtype
        else:
            self.dtype = self.get_default_dtype()
        self.stress_period_data = mflist(model,self.dtype,stress_period_data)

        self.np = 0
        self.parent.add_package(self)
    def __repr__(self):
        return 'CHD package class'
    def ncells( self):
        # Returns the  maximum number of cells that have recharge (developped for MT3DMS SSM package)
        return self.stress_period_data.mxact
    def write_file(self):
        f_chd = open(self.fn_path, 'w')
        f_chd.write('{0:s}\n'.format(self.heading))
        f_chd.write(' {0:9d}\n'.format(self.stress_period_data.mxact))
        self.stress_period_data.write_transient(f_chd)
        f_chd.close()

    @staticmethod
    def get_default_dtype():
        dtype = np.dtype([("k",np.int),("i",np.int),\
                         ("j",np.int),("shead",np.float32),\
                        ("ehead",np.float32)])


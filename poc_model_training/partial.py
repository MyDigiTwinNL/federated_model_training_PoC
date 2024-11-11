"""
This file contains all partial algorithm functions, that are normally executed
on all nodes for which the algorithm is executed.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled). From there, they are sent to the partial task
or directly to the user (if they requested partial results).
"""
import pandas as pd
import time
from typing import Any

from vantage6.algorithm.tools.util import info, warn, error
from vantage6.algorithm.tools.decorators import data


@data(1)
def partial(
    df1: pd.DataFrame, colname: str
) -> Any:

    """ Decentral part of the algorithm """
    # TODO this is a simple example to show you how to return something simple.
    # Replace it by your own code
    info("Computing something")
    info(f">>>> colname argument:{colname}")    

    info("Sleeping for 3000 secs")
    time.sleep(3000)    
    
    return df1[colname].max()
    


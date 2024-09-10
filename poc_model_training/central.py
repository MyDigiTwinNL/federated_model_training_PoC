"""
This file contains all central algorithm functions. It is important to note
that the central method is executed on a node, just like any other method.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled).
"""
from typing import Any

from vantage6.algorithm.tools.util import info, warn, error
from vantage6.algorithm.tools.decorators import algorithm_client
from vantage6.algorithm.client import AlgorithmClient
import numpy as np



@algorithm_client
def central(
    client: AlgorithmClient, arg1
) -> Any:
    

    """
    - Creating a central model
    - Request training on each node (each node trains its own model - with a given number of epochs)
    - Wait for the results, get weights and biases from the nodes.
    - aggregate weights on the server
    """


    """ Central part of the algorithm """
    # TODO implement this function. Below is an example of a simple but typical
    # central function.

    # get all organizations (ids) within the collaboration so you can send a
    # task to them.
    organizations = client.organization.list()
    org_ids = [organization.get("id") for organization in organizations]

    # Define input parameters for a subtask
    info("Defining input parameters")
    input_ = {
        "method": "partial",
        "kwargs": {
            # TODO add sensible values
            "arg1": "some_value",

        }
    }

    # create a subtask for all organizations in the collaboration.
    info("Creating subtask for all organizations in the collaboration")
    task = client.task.create(
        input_=input_,
        organizations=org_ids,
        name="My subtask",
        description="This is a very important subtask"
    )


    # wait for node to return results of the subtask.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Results obtained!")


    # Request execution of 'partial' to nodes:
        


    # TODO probably you want to aggregate or combine these results here.
    # For instance:
    # results = [sum(result) for result in results]

    # return the final results of the algorithm
    return results

# TODO Feel free to add more central functions here.


def aggregate_weights(client_weights):
    """"
    Two layers are asumed
    TODO generalize this
    """
    aggregated_weights1 = np.mean([weights[0] for weights in client_weights], axis=0)
    aggregated_weights2 = np.mean([weights[1] for weights in client_weights], axis=0)
    aggregated_bias1 = np.mean([weights[2] for weights in client_weights], axis=0)
    aggregated_bias2 = np.mean([weights[3] for weights in client_weights], axis=0)
    
    return aggregated_weights1, aggregated_weights2, aggregated_bias1, aggregated_bias2

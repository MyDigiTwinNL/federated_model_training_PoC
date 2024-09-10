"""
Run this script to test your algorithm locally (without building a Docker
image) using the mock client.

Run as:

    python test.py

Make sure to do so in an environment where `vantage6-algorithm-tools` is
installed. This can be done by running:

    pip install vantage6-algorithm-tools
"""
from vantage6.algorithm.tools.mock_client import MockAlgorithmClient
from pathlib import Path

# get path of current directory
current_path = Path(__file__).parent

sql_query_a = "SELECT VALUE FROM HEMOGLOBIN"
sql_query_b = """
SELECT 
    P.CVD_STATUS,
    P.STROKE_STATUS,
    P.MYOCARDIAL_INFARCTION_STATUS,
    P.HEART_FAILURE_STATUS,
    P.GENDER,
    P.T2D_STATUS,
    HDL.VALUE AS LAST_HDL,
    LDL.VALUE AS LAST_LDL,
    PA.VALUE AS LAST_PA,
    CA.VALUE AS LAST_CREATININE, -- Added line for Creatinine
    HBA.VALUE AS LAST_HBA1C, -- Added line for HbA1C
    HB.VALUE AS LAST_HEMOGLOBIN, -- Added line for Hemoglobin
    EGF.VALUE AS LAST_EGFR,-- Added line for EGFR
	BP.SYSTOLIC_VALUE AS LAST_SYSTOLIC, 
	BP.DIASTOLIC_VALUE AS LAST_DIASTOLIC
FROM 
    PATIENTS P
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE, 
            EFFECTIVE_DATE
        FROM 
            HDL_CHOLESTEROL
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    HDL_CHOLESTEROL
                GROUP BY 
                    PATIENTID
            )
    ) HDL ON P.ID = HDL.PATIENTID
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE, 
            EFFECTIVE_DATE
        FROM 
            LDL_CHOLESTEROL
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    LDL_CHOLESTEROL
                GROUP BY 
                    PATIENTID
            )
    ) LDL ON P.ID = LDL.PATIENTID
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE
        FROM 
            PLASMA_ALBUNIM
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    PLASMA_ALBUNIM
                GROUP BY 
                    PATIENTID
            )
    ) PA ON P.ID = PA.PATIENTID
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE
        FROM 
            CREATININE
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    CREATININE
                GROUP BY 
                    PATIENTID
            )
    ) CA ON P.ID = CA.PATIENTID -- Added join for Creatinine
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE
        FROM 
            HBA1C
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    HBA1C
                GROUP BY 
                    PATIENTID
            )
    ) HBA ON P.ID = HBA.PATIENTID -- Added join for HbA1C
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE
        FROM 
            HEMOGLOBIN
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    HEMOGLOBIN
                GROUP BY 
                    PATIENTID
            )
    ) HB ON P.ID = HB.PATIENTID -- Added join for Hemoglobin
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            VALUE
        FROM 
            EGFR
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    EGFR
                GROUP BY 
                    PATIENTID
            )
    ) EGF ON P.ID = EGF.PATIENTID -- Added join for EGFR
LEFT JOIN 
    (
        SELECT 
            PATIENTID, 
            SYSTOLIC_VALUE,
			DIASTOLIC_VALUE
        FROM 
            BLOODPRESSURE
        WHERE 
            EFFECTIVE_DATE IN (
                SELECT 
                    MAX(EFFECTIVE_DATE)
                FROM 
                    BLOODPRESSURE
                GROUP BY 
                    PATIENTID
            )
    ) BP ON P.ID = BP.PATIENTID -- Added join for Systolic Blood Pressure
"""

## Mock client
client = MockAlgorithmClient(
    datasets=[
        # Data for first organization
        [{
            "database": str(current_path / "dummydb-10k.db.sqlite"),
            "db_type": "sql",
            "query": sql_query_a,
        }],
        # Data for second organization
        [{
            "database": str(current_path / "dummydb-10k.db.sqlite"),
            "db_type": "sql",
            "query": sql_query_a,
        }]
    ],
    module="poc_model_training"
)

# list mock organizations
organizations = client.organization.list()
print(organizations)
org_ids = [organization["id"] for organization in organizations]

# Run the central method on 1 node and get the results
"""
central_task = client.task.create(
    input_={
        "method":"central",
        "kwargs": {
            # TODO add sensible values
            "arg1": "some_value",

        }
    },
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))
print(results)
"""


# Run the partial method for all organizations
task = client.task.create(
    input_={
        "method":"partial",
        "kwargs": {"colname":"VALUE"}
    },
    organizations=org_ids,
)
print(task)

# Get the results from the task
results = client.wait_for_results(task.get("id"))
print(results)

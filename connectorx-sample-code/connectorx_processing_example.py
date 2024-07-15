import sqlite3
import pandas as pd

db_path = './dummy-data/dummydb-10k.sqlite.db'                         # path to your SQLite database

con = sqlite3.connect(db_path)
cur = con.cursor()

query = f"""
SELECT 
    P.ID AS PatientID,
    P.GENDER,
    P.BIRTHDATE,
    P.T2D_STATUS,
    P.T2D_ONSET_DATE,
    P.STROKE_STATUS,
    HDL.VALUE AS HDL,
    LDL.VALUE AS LDL,
    PA.VALUE AS Plasma_Albumin,
    CA.VALUE AS Creatinine, 
    HBA.VALUE AS HbA1C, 
    HB.VALUE AS Hemoglobin, 
    EGF.VALUE AS EGFR,
       BP.SYSTOLIC_VALUE,
       BP.DIASTOLIC_VALUE
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
    ) CA ON P.ID = CA.PATIENTID 
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
    ) HBA ON P.ID = HBA.PATIENTID 
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
    ) HB ON P.ID = HB.PATIENTID 
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
    ) EGF ON P.ID = EGF.PATIENTID 
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
    ) BP ON P.ID = BP.PATIENTID 
"""


df = pd.read_sql_query(query,con)

print(df)

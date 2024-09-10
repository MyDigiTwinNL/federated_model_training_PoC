SELECT 
	P.CVD_STATUS,
	P.STROKE_STATUS,
	P.MYOCARDIAL_INFARCTION_STATUS,
	P.HEART_FAILURE_STATUS,
    P.GENDER,
    P.BIRTHDATE,
    P.T2D_STATUS,
    P.STROKE_STATUS,
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

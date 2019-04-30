/* Select all patients by cohort and count the number of DTI scans in each year
 * */

WITH PATCAT as ( /* Select enrolled and completed patients and their categories */
SELECT  PATNO, RECRUITMENT_CAT,  DESCRP_CAT, IMAGING_CAT FROM PATSTAT  
WHERE 
	ENROLL_STATUS in ("Complete", "Enrolled")  
ORDER BY RECRUITMENT_CAT ASC, DESCRP_CAT ASC, IMAGING_CAT ASC
),
MRI_DTI AS ( /* Select Patients with DTI Scans and put a 1 if they had a DTI scan in a particular year */
  select PATNO, EVENT_ID, COUNT(*) as DTI_COUNT,
	max(CASE WHEN EVENT_ID in ( 'BL', 'SC') THEN 1 ELSE 0 END) DTI_BL,
	max(CASE WHEN EVENT_ID = 'V04' THEN 1 ELSE null END) DTI_1YR,
	max(CASE WHEN EVENT_ID = 'V06' THEN 1 ELSE null END) DTI_2YR,
	max(CASE WHEN EVENT_ID = 'V08' THEN 1 ELSE null END) DTI_3YR,
	max(CASE WHEN EVENT_ID = 'V10' THEN 1 ELSE null END) DTI_4YR	 
 from MRI 
  WHERE MRIWDTI = 1
  group by PATNO, EVENT_ID 
  HAVING count(*) = 1
)
SELECT RECRUITMENT_CAT,  DESCRP_CAT, IMAGING_CAT, COUNT(*) as ENROLL_COUNT, 
    COUNT(MRI_DTI.DTI_BL) as DTI_BL,
    COUNT(MRI_DTI.DTI_1YR) as DTI_1YR,
    COUNT(MRI_DTI.DTI_2YR) as DTI_2YR,
    COUNT(MRI_DTI.DTI_3YR) as DTI_3YR,
    COUNT(MRI_DTI.DTI_4YR) as DTI_4YR	
	FROM PATCAT
LEFT JOIN MRI_DTI on PATCAT.PATNO = MRI_DTI.PATNO
GROUP BY  RECRUITMENT_CAT,  DESCRP_CAT, IMAGING_CAT

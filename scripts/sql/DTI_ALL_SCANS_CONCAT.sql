/* Create a comma separated string of subject ID's who have had 4 scans */

WITH A AS ( /* Patients and a count of their scans */
 SELECT PATNO, COUNT(PATNO) AS DTICNT FROM MRI
	WHERE 
	MRIWDTI = 1.0 AND  /* Had DTI scans */
	EVENT_ID IN ("BL", "V04", "V06", "V10")  /* Years 0, 1, 2, 4 */
	GROUP BY PATNO 
),
A4 as ( /* Only patients with all four scans */
SELECT * FROM A WHERE DTICNT=4 
)
/* Concatenate all the subject ID's with commas so that it can be pasted into PPMI */
SELECT GROUP_CONCAT(PATNO) from A4 

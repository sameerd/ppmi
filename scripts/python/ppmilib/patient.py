import numpy as np
import utils

class Patient(object):
    """ A patient object to capture all the data associated with an
        individual patient 
    """

    def __init__(self, patnum):
        self.patnum = patnum
        self.enroll_cat = None
        self.enroll_status = None
        self.education_years = None

    def is_enrolled(self):
        return self.enroll_status == "Enrolled"

    def is_pd(self):
        return self.enroll_cat == "PD"


class PatientDict(object):
    """ A dictionary of Patient objects keyed on patient number """
    
    def __init__(self):
        self.patientsd = {}

    def load(self, patients_df):
        for idx, row in patients_df.iterrows():
            p = Patient(row.PATNO)
            p.enroll_cat = row.ENROLL_CAT
            p.enroll_status = row.ENROLL_STATUS
            self.patientsd[p.patnum] = p

    def is_patient_enrolled(self, patnum):
        ret = False
        try:
            ret = self.patientsd[patnum].is_enrolled()
        except KeyError:
            pass
        return ret
    
    def is_patient_pd(self, patnum):
        ret = False
        try:
            ret = self.patientsd[patnum].is_pd()
        except KeyError:
            pass
        return ret

    def get_education_years(self, patnum_array):
        return np.asarray([self.patientsd[x].education_years 
                            for x in patnum_array])

    def get_enrolled_mask(self, patnum_array):
        return np.asarray([True if self.is_patient_enrolled(x) else False
                            for x in patnum_array])

    def get_pd_mask(self, patnum_array):
        return np.asarray([True if self.is_patient_pd(x) else False
                            for x in patnum_array])
 
    def add_socio_economics(self):
        socio_df = utils.fetch_ppmi_data_file("Socio-Economics.csv",
                "subject")
        for idx, row in socio_df.iterrows():
            # if there are duplicates we just take the last value
            try:
                self.patientsd[row.PATNO].education_years = row.EDUCYRS
            except KeyError: 
                # if a patient doesn't have a status don't put it in
                pass



    @staticmethod
    def create():
        patients_df = utils.fetch_ppmi_data_file("Patient_Status.csv",
                "subject")
        patientsd = PatientDict()
        patientsd.load(patients_df)
        return patientsd



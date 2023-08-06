from .parameter import Parameter
from datetime import date, datetime, time, timedelta
import logging
import pandas as pd

pd.options.mode.chained_assignment = None

class Patient:
    """Only a container for multiple Parameter objects with some additional
    patient-level information and some set-up logic.
    """

    # Instance creation

    def __init__(self, patientunitstayid, eicuVitalPeriodic, eicuPatient, eicuDiagnosis, eicuMedication):
        self.patientunitstayid = patientunitstayid

        self.statics = self.__extract_statics(eicuPatient)
        self.diagnoses = self.__extract_diagnoses(eicuDiagnosis)
        self.medications = self.__extract_medications(eicuMedication)

        vitals = self.__extract_vitals(eicuVitalPeriodic)
        self.parameters = {
            parameter: Parameter(self, parameter, vitals[parameter])
            for parameter in vitals.columns}

    def __extract_statics(self, eicuPatient):
        return self.__rectify_age({
            key: value
            for key, value
            in eicuPatient.loc[self.patientunitstayid].items()})

    def __rectify_age(self, statics):
        try:
            statics['age'] = int(statics['age'])
        except ValueError:
            age = statics['age']
            statics['age'] = 90
            logging.info(f"{self}: Converted age = '{age}' to age = {statics['age']}.")

        return statics

    def __extract_diagnoses(self, eicuDiagnosis):
        diagnoses = eicuDiagnosis[
            eicuDiagnosis.patientunitstayid == self.patientunitstayid]

        diagnoses['time'] = diagnoses.diagnosisoffset.apply(self.__datetime_for_offset)

        return (diagnoses
            .drop(['diagnosisoffset', 'patientunitstayid'], axis=1)
            .set_index('time')
            .sort_index())

    def __extract_medications(self, eicuMedication):
        medications = eicuMedication[
            eicuMedication.patientunitstayid == self.patientunitstayid]

        medications['drugordertime'] = medications.drugorderoffset.apply(self.__datetime_for_offset)
        medications['drugstarttime'] = medications.drugstartoffset.apply(self.__datetime_for_offset)
        medications['drugstoptime'] = medications.drugstopoffset.apply(self.__datetime_for_offset)

        return (medications
            .drop(
                ['drugorderoffset', 'drugstartoffset', 'drugstopoffset', 'patientunitstayid'],
                axis=1)
            .set_index('drugstarttime')
            .sort_index())

    def __extract_vitals(self, eicuVitalPeriodic):
        vitals = eicuVitalPeriodic[
            eicuVitalPeriodic.patientunitstayid == self.patientunitstayid]
        
        vitals['time'] = vitals.observationoffset.apply(self.__datetime_for_offset)

        return (vitals
            .drop(['observationoffset', 'patientunitstayid'], axis=1)
            .set_index('time')
            .sort_index())

    def __datetime_for_offset(self, offset):
        ref_date = date(1970, 1, 1)
        ref_time = time.fromisoformat(self.statics['unitadmittime24'])
        ref_datetime = datetime.combine(ref_date, ref_time)
        return ref_datetime + timedelta(minutes=offset)

    # Textual representation

    def __repr__(self):
        return f"Patient {self.patientunitstayid}"

    def __str__(self):
        return f"Patient {self.patientunitstayid}"

    # Public interface

    def diagnoses_at(self, index):
        return self.diagnoses.loc[:index]

    def medications_at(self, index):
        return self.medications.loc[:index]
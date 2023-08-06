from .patient import Patient
from .plotting import heatmap
from inspect import signature
from tqdm import tqdm

import logging
import numpy as np
import pandas as pd
import seaborn as sns

class Artemis:
    """Main class used mostly for database loading, data management and
    aggregations over multiple patients.
    """

    def __init__(self, path, virtuals={}, filter=None):
        self.patients = []
        self.path = path
        self.virtuals = virtuals
        self.filter = filter

        logging.basicConfig(filename='artemis.log', level=logging.INFO)

    def load(self):
        print("Loading database...", flush=True)

        eicuPatient = pd.read_csv(
            self.path + '/patient.csv', index_col='patientunitstayid',
            low_memory=False)

        if self.filter is not None:
            eicuPatient = eicuPatient[eicuPatient.apply(self.filter, axis=1)]

        eicuVitalPeriodic = self.load_table('vitalPeriodic', eicuPatient.index)
        eicuDiagnosis = self.load_table('diagnosis', eicuPatient.index)
        eicuMedications = self.load_table('medication', eicuPatient.index)

        for name, func in tqdm(self.virtuals.items(), desc="Computing virtual parameters"):
            eicuVitalPeriodic[name] = eicuVitalPeriodic.apply(func, axis=1)

        puids = eicuVitalPeriodic.patientunitstayid.value_counts().index

        self.patients = [
            Patient(
                patientunitstayid, eicuVitalPeriodic, eicuPatient,
                eicuDiagnosis, eicuMedications)
            for patientunitstayid in tqdm(puids, desc="Creating Patient objects")]

        return self

    def load_table(self, name, pusids=None):
        if pusids is None:
            return pd.read_csv(self.path + f'/{name}.csv', low_memory=False)

        iter = pd.read_csv(
            self.path + f'/{name}.csv',
            low_memory=False, iterator=True, chunksize=1000)

        return pd.concat([
            chunk[chunk.patientunitstayid.isin(pusids)]
            for chunk in iter])

    def grid(self, parameter, threshold_policy_factory, factory_params, event_policy):
        """Numerically compare parameter combinations for parametric alarm threshold policies."""
        return sum([
            patient.parameters[parameter].grid(
                threshold_policy_factory, factory_params, event_policy, verbose=False)
            for patient in tqdm(self.patients)])

    def heatmap(self, parameter, threshold_policy_factory, factory_params, event_policy):
        """Graphically compare parameter combinations for parametric alarm threshold policies."""
        table = self.grid(parameter, threshold_policy_factory, factory_params, event_policy)
        param_names = list(signature(threshold_policy_factory).parameters.keys())
        return heatmap(table,
        f"# Alarms for '{parameter}'\n"
        + f"with {threshold_policy_factory.__name__}({', '.join(param_names)})")

    def compare(self, parameter, configurations):
        return pd.concat([
            patient.parameters[parameter].compare(configurations)
            for patient in tqdm(self.patients)], ignore_index=True)
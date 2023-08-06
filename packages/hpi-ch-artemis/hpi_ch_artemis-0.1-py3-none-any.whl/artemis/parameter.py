from .plotting import heatmap, plot_alarms
from inspect import signature
from tqdm import tqdm
import pandas as pd

tqdm.pandas()

class Parameter:
    """This class handles a single parameters (heart rate, blood pressure) of a 
    single patient.
    """

    def __init__(self, patient, name, measurements):
        self.patient = patient
        self.name = name
        self.measurements = measurements.interpolate()

    def __repr__(self):
        return f"{self.patient} > {self.name}"

    def __str__(self):
        return f"{self.patient} > {self.name}"

    def measurements_at(self, index):
        return self.measurements.loc[:index]

    def thresholds(self, threshold_policy):
        """Runs the alarm threshold policy and generates high and low threshold
        time-series.
        """
        high_thresholds, low_thresholds = tuple(zip(*[
            threshold_policy(
                self.patient.statics,
                self.measurements_at(index),
                self.patient.diagnoses_at(index),
                self.patient.medications_at(index))
            for index in self.measurements.index]))

        return list(high_thresholds), list(low_thresholds)

    def alarms(self, event_policy, high_thresholds, low_thresholds):
        """Runs the alarm event policy and generates a pandas Series of
        violating measurements, i.e. alarm events.
        """
        is_high_alarm, is_low_alarm = tuple(zip(*[
            event_policy(
                self.patient,
                self.measurements.loc[:index],
                high_threshold, low_threshold)
            for index, measurement, high_threshold, low_threshold
            in zip(
                self.measurements.index,
                self.measurements,
                high_thresholds,
                low_thresholds)]))

        high_alarms = self.measurements[list(is_high_alarm)]
        low_alarms  = self.measurements[list(is_low_alarm)]

        return high_alarms, low_alarms

    # Plotting

    def plot_alarms(self, threshold_policy, event_policy):
        """Plot measurements, alarm thresholds, and alarm events."""
        high_thresholds, low_thresholds = self.thresholds(threshold_policy)
        high_alarms, low_alarms = self.alarms(event_policy, high_thresholds, low_thresholds)

        return plot_alarms(
            self.measurements,
            high_thresholds, low_thresholds,
            high_alarms, low_alarms,
            str(self.patient), self.name)

    # Grid comparison and heatmap

    def grid(self, threshold_policy_factory, factory_params, event_policy, verbose=True):
        """Numerically compare parameter combinations for parametric alarm
        threshold policies.
        """
        param_names = list(signature(threshold_policy_factory).parameters.keys())

        if len(param_names) != 2:
            raise ValueError(
                "Function threshold_policy_factory must accept exactly two parameters")

        if not all([param_name in factory_params for param_name in param_names]):
            raise ValueError(
                "All parameters of threshold_policy_factory must be in params dict")

        result = pd.merge(
            pd.Series(factory_params[param_names[0]], name=param_names[0]),
            pd.Series(factory_params[param_names[1]], name=param_names[1]),
            how='cross')
        
        def n_alarms(row):
            high_thresholds, low_thresholds = self.thresholds(
                threshold_policy_factory(**{
                    param_names[0]: row[param_names[0]],
                    param_names[1]: row[param_names[1]]}))
            high_alarms, low_alarms = self.alarms(event_policy, high_thresholds, low_thresholds)
            return len(high_alarms) + len(low_alarms)

        if verbose:
            result['# Alarms'] = result.progress_apply(n_alarms, axis=1)
        else:
            result['# Alarms'] = result.apply(n_alarms, axis=1)
            
        return result.set_index([param_names[0], param_names[1]])

    def heatmap(self, threshold_policy_factory, factory_params, event_policy):
        """Graphically compare parameter combinations for parametric alarm
        threshold policies.
        """
        table = self.grid(threshold_policy_factory, factory_params, event_policy)
        param_names = list(signature(threshold_policy_factory).parameters.keys())
        return heatmap(table, f"# Alarms for {self}\n"
        + f"with {threshold_policy_factory.__name__}({', '.join(param_names)})")

    # Side-by-side comparison

    def evaluate(self, threshold_policy, event_policy):
        """Determine number of alarms for a given combination of alarm threshold
        policy and alarm event policy.
        """
        high_thresholds, low_thresholds = self.thresholds(threshold_policy)
        high_alarms, low_alarms = self.alarms(event_policy, high_thresholds, low_thresholds)
        return len(high_alarms), len(low_alarms)

    def compare(self, configurations):
        """Compare multiple combinations of alarm threshold policies and alarm
        event policies.
        """
        n_high_alarms, n_low_alarms = tuple(zip(*[
                self.evaluate(threshold_policy, event_policy)
                for threshold_policy, event_policy in configurations]))
        
        n_alarms = [h+l for h, l in zip(n_high_alarms, n_low_alarms)]
        
        return pd.DataFrame({
            'Patient': str(self.patient),
            'Parameter': self.name,
            'Alarm Threshold Policy': [
                threshold_policy.__name__
                for threshold_policy, _ in configurations],
            'Alarm Event Policy': [
                event_policy.__name__
                for _, event_policy in configurations],
            '# High Alarms': n_high_alarms,
            '# Low Alarms': n_low_alarms,
            '# Alarms': n_alarms})
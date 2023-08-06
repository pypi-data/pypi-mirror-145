"""This is ARTEMIS's alarm event policy library providing ready-made,
adaptable alarm event policies.
"""

def every(patient, measurements, high_threshold, low_threshold):
    """Every measurement above the high threshold and below the low threshold
    causes an alarm.
    """
    is_high_alarm = measurements.iloc[-1] > high_threshold
    is_low_alarm  = measurements.iloc[-1] < low_threshold
    return is_high_alarm, is_low_alarm

def delayed(patient, measurements, high_threshold, low_threshold):
    """When the vital parameter crosses its respective threshold: Wait for one
    measurement (5 minutes) before an alarm goes off.
    """
    try:
        is_high_alarm = (
            measurements.iloc[-1] > high_threshold
            and measurements.iloc[-2] > high_threshold)
        is_low_alarm  = (
            measurements.iloc[-1] < low_threshold
            and measurements.iloc[-2] < low_threshold)
    except IndexError:
        is_high_alarm = False
        is_low_alarm  = False

    return is_high_alarm, is_low_alarm

def escalation(patient, measurements, high_threshold, low_threshold):
    """Alarm once when the measurement crosses the alarm threshold and re-alarm
    only when the measurement moves further away from the alarm threshold.
    """
    try:
        is_high_alarm = (
            measurements.iloc[-1] > high_threshold
            and measurements.iloc[-1] > measurements.iloc[-2])
        is_low_alarm  = (
            measurements.iloc[-1] < low_threshold
            and measurements.iloc[-1] < measurements.iloc[-2])
    except IndexError:
        is_high_alarm = measurements.iloc[-1] > high_threshold
        is_low_alarm  = measurements.iloc[-1] < low_threshold

    return is_high_alarm, is_low_alarm

def first(patient, measurements, high_threshold, low_threshold):
    """Only the first measurement that crosses high or low threshold causes
    an alarm.
    """
    try:
        is_high_alarm = (
            measurements.iloc[-1] > high_threshold
            and measurements.iloc[-2] <= high_threshold)
        is_low_alarm  = (
            measurements.iloc[-1] < low_threshold
            and measurements.iloc[-2] >= low_threshold)
    except IndexError:
        is_high_alarm = measurements.iloc[-1] > high_threshold
        is_low_alarm  = measurements.iloc[-1] < low_threshold

    return is_high_alarm, is_low_alarm

def second(patient, measurements, high_threshold, low_threshold):
    """Only the second measurement that crosses high or low threshold causes
    an alarm. This is a combination of delayed and first.
    """
    if len(measurements) >= 3:
        is_high_alarm = (
            measurements.iloc[-1] > high_threshold 
            and measurements.iloc[-2] > high_threshold
            and measurements.iloc[-3] <= high_threshold)
        is_low_alarm  = (
            measurements.iloc[-1] < low_threshold 
            and measurements.iloc[-2] < low_threshold
            and measurements.iloc[-3] >= low_threshold)
    
    if len(measurements) == 2:
        is_high_alarm = (
            measurements.iloc[-1] > high_threshold 
            and measurements.iloc[-2] > high_threshold)
        is_low_alarm  = (
            measurements.iloc[-1] < low_threshold 
            and measurements.iloc[-2] < low_threshold)

    if len(measurements) <= 1:
        is_high_alarm = False
        is_low_alarm  = False

    return is_high_alarm, is_low_alarm

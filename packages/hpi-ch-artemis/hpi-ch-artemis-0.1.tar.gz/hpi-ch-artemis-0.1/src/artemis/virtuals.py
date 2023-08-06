"""This is ARTEMIS's virtual parameter library."""

def shockindex(msmts):
    if msmts['systemicsystolic'] == 0:
        return np.nan
    return msmts['heartrate']/msmts['systemicsystolic']
import numpy.random as rdm
import math, os.path as path, os

tau = math.pi * 2
sin_multiplier = 10 # sample rate above sin freq to use
step_scale = 10 # mm/s speed of step function ramp (cannot be instantaneous)

# basically 3 main components to this code in a few variations
# 1. generator functions for signals that send out a time series list as well as
# the ms interval between samples (and a list of the time of each sample)
# 2. output functions that convert those lists into csv files and provides 
# helpful metadata to advise the process of converting that to shake table 
# trajectories (sample rate, initial displacement, etc.)
# 3. dispatcher code that provides a main routine that can be used to generate
# the data files used by the shake tables, prompting for relevant parameters and
# doing any necessary checks on the inputs provided by the user

def sin_gen(amp, freq, mins):
    # sin wave formula: -A * cos(2*pi*f*t)
    # we use this formula because it means that at 0
    # the wave is offset to its lowest point
    # thus the sensor can be homed to zero
    sampling = sin_multiplier * freq
    # derive sample rate, use it to get time step
    step = 1 / sampling
    ms_interval = step * 1000
    time = 0
    timestamps = []
    wave_series = []
    max_time = mins * 60; # conv. to seconds
    while time < max_time:
        timestamps.append(time)
        sin_eval = -amp * math.cos(tau*freq*time)
        wave_series.append(sin_eval)
        time += step
    return (ms_interval, timestamps, wave_series)

def sweep_gen(amp, f_bgn, f_end, mins):
    high_frq = max(f_bgn, f_end)
    sampling = sin_multiplier * high_frq
    step = 1 / sampling
    ms_interval = step * 1000
    time = 0
    timestamps = []
    wave_series = []
    max_time = mins * 60
    # number of points in the data
    samps = math.floor(max_time * sampling)
    # we use a linear sweep function, using these parameters
    # f1, f2 are normalized frequencies of start, stop
    f1 = f_bgn / sampling
    f2 = f_end / sampling
    k = (f2 - f1)
    a = tau * k / samps
    b = tau * f1
    idx = 0
    while time < max_time:
        timestamps.append(time)
        # frequency multipliers have been scaled, use index not actual time
        sin_eval = -amp * math.cos( a/2 * (idx**2) + b * idx  )
        wave_series.append(sin_eval)
        time += step
        idx += 1
    return (ms_interval, timestamps, wave_series)

def step_gen(amp, mins):
    sampling = 100.
    step = 1 / sampling
    ms_interval = step * 1000
    time = 0
    timestamps = []
    wave_series = []
    max_time = mins * 60 + 20 # add lead-in time
    scale = step_scale / sampling
    ramp_time = amp / scale # how long to increase speed
    step_start = 10
    step_end = max_time - 10
    current_pos = 0
    while time < max_time:
        if time > step_start and time < step_end and current_pos < AMP (mm):
            current_pos += scale
            if current_pos > AMP (mm):
                current_pos = amp
        elif time > step_end and current_pos > 0:
            current_pos -= scale
            if current_pos < 0:
                current_pos = 0
        timestamps.append(time)
        wave_series.append(current_pos)
        time += step
    return (ms_interval, timestamps, wave_series)    
    

def get_folder():
    home_folder = path.expanduser('~/Trajectories/')
    if not path.isdir(home_folder):
        os.mkdir(home_folder)
    return home_folder

def collect_data(times, wave):
    csv_data = ""
    for idx in range(1, len(wave)-1):
        time_now = times[idx]
        sample = wave[idx]
        line = ""
        line += str(sample)
        line += ", "
        line += str(time_now)
        line += "\n"
        csv_data += line
    # don't include newline after last line
    idx = len(wave)-1
    time_now = times[idx]
    sample = wave[idx]
    line = ""
    line += str(sample)
    line += ", "
    line += str(time_now)
    csv_data += line
    return csv_data

def sweep_out(amp, freq0, freq1, mins):
    (ms_itv, times, wave) = sweep_gen(amp, freq0, freq1, mins)
    home_folder = get_folder()
    file_prefix = home_folder
    file_prefix += "sweep_"
    file_prefix += str(float(freq0))
    file_prefix += "hz_to_"
    file_prefix += str(float(freq1))
    file_prefix += "hz_"
    file_prefix += str(int(amp))
    file_prefix += "amp_"
    file_prefix += str(int(mins))
    file_prefix += "mins"
    csv_name = file_prefix + ".csv"
    # used to inform of any additional data worth noting
    metadata_name = file_prefix+".metadata.txt"
    metadata = "Make sure input and output intervals"
    metadata += " are set to " + str(ms_itv) + " ms.\n"
    metadata += "The sweep wave should be able to be started"
    metadata += " from the home position.\n"
    metadata += "The timeseries is the CSV's first column.\n"
    metadata += "Don't forget to select the proper axis!"
    print metadata
    # collect the csv data
    csv_data = collect_data(times, wave)
    with open(csv_name, 'w') as csv_file:
        csv_file.write(csv_data)
    with open(metadata_name, 'w') as meta_file:
        meta_file.write(metadata)
    return

# output the sine wave
def sin_out(amp, freq, mins):
    (ms_itv, times, wave) = sin_gen(amp, freq, mins)
    home_folder = get_folder()
    file_prefix = home_folder
    file_prefix += "sin_"
    file_prefix += str(float(freq))
    file_prefix += "hz_"
    file_prefix += str(int(amp))
    file_prefix += "amp_"
    file_prefix += str(int(mins))
    file_prefix += "mins"
    csv_name = file_prefix + ".csv"
    # used to inform of any additional data worth noting
    metadata_name = file_prefix+".metadata.txt"
    metadata = "Make sure input and output intervals"
    metadata += " are set to " + str(ms_itv) + " ms.\n"
    metadata += "The sin wave should be able to be started"
    metadata += " from the home position.\n"
    metadata += "The timeseries is the CSV's first column.\n"
    metadata += "Don't forget to select the proper axis!"
    print metadata
    # collect the csv data
    csv_data = collect_data(times, wave)
    with open(csv_name, 'w') as csv_file:
        csv_file.write(csv_data)
    with open(metadata_name, 'w') as meta_file:
        meta_file.write(metadata)
    return

def step_out(amp, mins):
    (ms_itv, times, wave) = step_gen(amp, mins)
    home_folder = get_folder()
    file_prefix = home_folder
    file_prefix += "step_"
    file_prefix += str(int(amp))
    file_prefix += "amp_"
    file_prefix += str(int(mins))
    file_prefix += "mins"
    csv_name = file_prefix + ".csv"
    # used to inform of any additional data worth noting
    metadata_name = file_prefix+".metadata.txt"
    metadata = "Make sure input and output intervals"
    metadata += " are set to " + str(ms_itv) + " ms.\n"
    metadata += "The step function should be able to be started"
    metadata += " from the home position.\n"
    metadata += "The timeseries is the CSV's first column.\n"
    metadata += "Don't forget to select the proper axis!"
    print metadata
    # collect the csv data
    csv_data = collect_data(times, wave)
    with open(csv_name, 'w') as csv_file:
        csv_file.write(csv_data)
    with open(metadata_name, 'w') as meta_file:
        meta_file.write(metadata)
    return

def numeric(str):
    if len(str) <= 0:
        return False
    try:
        float(str)
        return True
    except ValueError:
        return False
    
def prompt_numeric(msg, data_fmt):
    num_string = ""
    while not numeric(num_string):
        if len(num_string) > 0:
            print "Cannot parse input as numeric [", num_string, "]"
        print msg
        num_string = raw_input(data_fmt)
        if len(num_string) == 0:
            num_string == " "
    return float(num_string)
    

def usr_prompts():
    msg = "Generate sine, sine chirp (sweep), or pulse (step) "
    msg += "pattern. "
    print msg
    char = ''
    valid = ['s','c','p']
    while char not in valid:
        if char != '':
            print "\nSorry, that input [", char, "] is invalid."
            print msg
        var = raw_input("(Input s, c, or p respectively to choose.) ")
        if len(var) == 0:
            var = ' '
        char = var.lower()[0]; # make lowercase, get first char
    if char == 's':
        print "Creating a sine wave."
        msg = "Please specify an amplitude."
        data = "AMP (mm): "
        amp = prompt_numeric(msg, data)
        msg = "Please specify a frequency."
        data = "FREQ (Hz): "
        freq = prompt_numeric(msg, data)
        msg = "Please specify a duration. (minutes)"
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        sin_out(amp, freq, mins)
    elif char == 'c':
        print "Creating a swept sine wave."
        msg = "Please specify an amplitude."
        data = "AMP (mm): "
        amp = prompt_numeric(msg, data)
        msg = "Please specify a starting frequency."
        data = "START FREQ (Hz): "
        freq0 = prompt_numeric(msg, data)
        msg = "Please specify a termination frequency."
        data = "END FREQ (Hz): "
        freq1 = prompt_numeric(msg, data)
        msg = "Please specify a duration. (minutes)"
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        sweep_out(amp, freq0, freq1, mins)
    elif char == 'p':
        print "Creating a step function."
        msg = "Please specify an amplitude (peak value of step)."
        data = "AMP (mm): "
        amp = prompt_numeric(msg, data)
        msg = "The step function has lead-in and out times of 10 seconds.\n"
        msg += "Please specify the duration of the step (minutes)."
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        step_out(amp, mins)

    print "Data has been saved in the folder labeled 'Trajectories',"
    print " under the current user's home directory."
    print "Please run again to generate a new function."

if __name__ == "__main__":
    usr_prompts()

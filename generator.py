import numpy.random as rdm
import math, os.path as path, os

tau = math.pi * 2

def sin_gen(amp, freq, mins):
    # sin wave formula: -A * cos(2*pi*f*t)
    # we use this formula because it means that at 0
    # the wave is offset to its lowest point
    # thus the sensor can be homed to zero
    sampling = 10 * freq
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
    sampling = 10 * high_frq
    step = 1 / sampling
    ms_interval = step * 1000
    time = 0
    timestamps = []
    wave_series = []
    max_time = mins * 60
    # we use a linear sweep function, this is the parameter
    k = (f_end - f_bgn) 
    while time < max_time:
        timestamps.append(time)
        sin_eval = -amp * math.cos(tau*(f_bgn*time + (k/2 * time**2)))
        wave_series.append(sin_eval)
        time += step
    return (ms_interval, timestamps, wave_series)

def noise_gen(amp, mins):
    sampling = 200. # samples per second
    step = 1 / sampling
    ms_interval = step * 1000
    time = 0
    timestamps = []
    wave_series = []
    max_time = mins * 60
    num_samples = sampling * max_time
    if num_samples - int(num_samples) > 0:
        num_samples = int(num_samples) + 1
    else:
        num_samples = int(num_samples)
    # use mean 0, st-dev = 1
    noise = rdm.standard_normal(size=num_samples)
    s = sum(noise)
    for i in range(0, num_samples):
        timestamps.append(step * i);
    wave_series = [amp*i/s for i in noise]
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
    file_prefix += str(int(freq0))
    file_prefix += "hz_to_"
    file_prefix += str(int(freq1))
    file_prefix += "_hz"
    file_prefix += str(int(amp))
    file_prefix += "amp_"
    file_prefix += str(int(mins))
    file_prefix += "mins"
    csv_name = file_prefix + ".csv"
    # used to inform of any additional data worth noting
    metadata_name = file_prefix+".metadata.txt"
    metadata_name = file_prefix+".metadata.txt"
    metadata = ""
    metadata += "Make sure input and output intervals"
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

def noise_out(amp, mins):
    (ms_itv, times, wave) = noise_gen(amp, mins)
    home_folder = get_folder()
    file_prefix = home_folder
    file_prefix += "noise_"
    file_prefix += str(int(amp))
    file_prefix += "amp_"
    file_prefix += str(int(mins))
    file_prefix += "mins"
    csv_name = file_prefix + ".csv"
    # used to inform of any additional data worth noting
    metadata_name = file_prefix+".metadata.txt"
    metadata_name = file_prefix+".metadata.txt"
    metadata = ""
    metadata += "Make sure input and output intervals"
    metadata += " are set to " + str(ms_itv) + " ms.\n"
    metadata += "You may need to adjust the starting position of the table.\n"
    metadata += "It is advised to set the table starting position to "
    metadata += str(amp)+" mm.\n"
    metadata += "(The shake table only allows positive-value positions.)\n"
    metadata += "The value of t to is " + str(amp) + "\n"
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
    file_prefix += str(int(freq))
    file_prefix += "_hz"
    file_prefix += str(int(amp))
    file_prefix += "amp_"
    file_prefix += str(int(mins))
    file_prefix += "mins"
    csv_name = file_prefix + ".csv"
    # used to inform of any additional data worth noting
    metadata_name = file_prefix+".metadata.txt"
    metadata = ""
    metadata += "Make sure input and output intervals"
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
    
def prompt_numeric(msg, data_fmt):
    num_string = unicode('')
    while not num_string.isnumeric():
        if len(num_string) > 0:
            print "Cannot parse input as numeric [", num_string, "]"
        print msg
        num_string = unicode(raw_input(data_fmt))
        if len(num_string) == 0:
            num_string == " "
    return float(num_string)
    

def usr_prompts():
    msg = "Generate sine, sine chirp (sweep), or white noise "
    msg += "pattern. "
    print msg
    valid = ['s','c','w']
    while char not in valid:
        if char != '':
            print "\nSorry, that input [", char, "] is invalid."
            print msg
        var = raw_input("(Input s, c, w, or p respectively to choose.) ")
        if len(var) == 0:
            var = ' '
        char = var.lower()[0]; # make lowercase, get first char
    if char == 's':
        print "Creating a sine wave."
        msg = "Please specify an amplitude."
        data = "AMP: "
        amp = prompt_numeric(msg, data)
        msg = "Please specify a frequency."
        data = "FREQ: "
        freq = prompt_numeric(msg, data)
        msg = "Please specify a duration (minutes)"
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        sin_out(amp, freq, mins)
    else if char == 'c':
        print "Creating a swept sine wave."
        msg = "Please specify an amplitude."
        data = "AMP: "
        amp = prompt_numeric(msg, data)
        msg = "Please specify a starting frequency."
        data = "START FREQ: "
        freq0 = prompt_numeric(msg, data)
        msg = "Please specify a termination frequency."
        data = "END FREQ: "
        freq1 = prompt_numeric(msg, data)
        msg = "Please specify a duration (minutes)"
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        sweep_out(amp, freq0, freq1, mins)
    else if char == 'w':
        print "Creating a white noise function."
        msg = "Please specify an amplitude (total range of noise function)."
        data = "AMP: "
        amp = prompt_numeric(msg, data)
        msg = "Please specify a duration (minutes)"
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        noise_out(amp, mins)
    """else if char == 'p':
        print "Creating a step function."
        msg = "Please specify an amplitude (peak value of step)."
        data = "AMP: "
        amp = prompt_numeric(msg, data)
        msg = "Please specify a duration (minutes)"
        data = "DUR: "
        mins = prompt_numeric(msg, data)
        step_out(amp, mins)"""

    print "Data has been saved in the folder labeled 'Trajectories',"
    print " under the current user's home directory."
    print "Please run again to generate a new function."

if __name__ == "__main__":
    usr_prompts()

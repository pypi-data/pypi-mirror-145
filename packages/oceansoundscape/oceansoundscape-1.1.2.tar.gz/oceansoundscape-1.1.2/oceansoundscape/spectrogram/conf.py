# Optimum spectrogram parameters for classification
PCEN_GAIN = 0.25
PCEN_BIAS = 2.0
PCEN_TIME_CONSTANT = 0.6
OVERLAP = 0.95
CONF_DICT = {}
IMAGE_SIZE = (224, 224)  # size the model expects
BLUE_A = dict(
    low_freq=70,
    high_freq=100,
    # duration in seconds for temporal window size centered around BLED detection
    # if zero, ignores and uses BLED start/end
    duration_secs=25,
    blur_axis='frequency',
    num_fft=1024,
    center=True, # call should be centered during training
    # padding in seconds to add to beginning/ending of wav files
    padding_secs=3,
    num_mels=30
)
BLUE_B = dict(
    low_freq=35,
    high_freq=55,
    duration_secs=0,
    blur_axis='time',
    num_fft=512,
    center=True, # call should be centered during training
    # padding in seconds to add to beginning/ending of wav files
    padding_secs=2
)
BLUE_D = dict(
    low_freq=20,
    high_freq=90,
    duration_secs=7,
    blur_axis='',
    num_fft=1024,
    center=True, # call should be centered during training
    padding_secs=2,
    num_mels=30
)
FIN_20 = dict(
    low_freq=10,
    high_freq=35,
    duration_secs=0,
    blur_axis='frequency',
    num_fft=4096,
    center=False, # call should not be centered during training
    # padding in seconds to add to beginning/ending of wav files
    padding_secs=3
)
CONF_DICT["blueA"] = BLUE_A
CONF_DICT["blueB"] = BLUE_B
CONF_DICT["blueD"] = BLUE_D
CONF_DICT["fin20"] = FIN_20

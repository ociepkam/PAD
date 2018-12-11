import atexit
from psychopy import visual, event, core, logging
import time

from os.path import join
import csv
import random

from sources.experiment_info import experiment_info
from sources.load_data import load_config
from sources.screen import get_screen_res, get_frame_rate
from sources.show_info import show_info, show_image
from sources.trail import Trial

part_id, part_sex, part_age, date = experiment_info()
NAME = "{}_{}_{}".format(part_id, part_sex, part_age)

RESULTS = list()
RESULTS.append(['TRIAL_NR', 'TASK_NR', 'EXPERIMENTAL', 'ACC', 'RT', 'ANSWER_TYPE', 'ANSWERS_ORDER'])

RAND = "" #str(random.randint(100, 999))

logging.LogFile(join('.', 'results', 'logging', NAME + '_' + RAND + '.log'), level=logging.INFO)


@atexit.register
def save_beh():
    logging.flush()
    with open(join('results', 'behavioral_data', 'beh_{}_{}.csv'.format(NAME, RAND)), 'w') as csvfile:
        beh_writer = csv.writer(csvfile)
        beh_writer.writerows(RESULTS)


config = load_config()

SCREEN_RES = get_screen_res()
win = visual.Window(SCREEN_RES, fullscr=True, monitor='testMonitor', units='pix',
                    screen=0, color='Gainsboro', winType='pygame')
FRAMES_PER_SEC = get_frame_rate(win)

clock_image = visual.ImageStim(win=win, image=join('images', 'clock.png'), interpolate=True,
                               size=config['CLOCK_SIZE'], pos=config['CLOCK_POS'])
mouse = event.Mouse()

response_clock = core.Clock()
trial_nr = 1

# TRAINING
show_info(win, join('.', 'messages', "instruction1.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])

# show_image(window, 'instruction.png', SCREEN_RES)
for item in config["TRAINING_TRIALS"]:
    trial = Trial(win=win, config=config, item=item)
    trial.run(config=config, win=win, response_clock=response_clock, clock_image=clock_image, mouse=mouse)
    RESULTS.append(trial.info(exp=False, trial_nr=trial_nr))
    trial_nr += 1
    if config["TRAINING_FEEDBACK"]:
        if trial.acc:
            show_info(win, join('.', 'messages', "feedback_positive.txt"), text_size=config['TEXT_SIZE'],
                      screen_width=SCREEN_RES[0], show_time=config["FEEDBACK_SHOW_TIME"])
        else:
            show_info(win, join('.', 'messages', "feedback_negative.txt"), text_size=config['TEXT_SIZE'],
                      screen_width=SCREEN_RES[0], show_time=config["FEEDBACK_SHOW_TIME"])
    time.sleep(config["WAIT_TIME"])

# EXPERIMENT
show_info(win, join('.', 'messages', "instruction2.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])

for item in config["EXPERIMENT_TRIALS"]:
    trial = Trial(win=win, config=config, item=item)
    trial.run(config=config, win=win, response_clock=response_clock, clock_image=clock_image, mouse=mouse)
    RESULTS.append(trial.info(exp=True, trial_nr=trial_nr))
    trial_nr += 1
    if config["EXPERIMENT_FEEDBACK"]:
        if trial.acc:
            show_info(win, join('.', 'messages', "feedback_positive.txt"), text_size=config['TEXT_SIZE'],
                      screen_width=SCREEN_RES[0], show_time=config["FEEDBACK_SHOW_TIME"])
        else:
            show_info(win, join('.', 'messages', "feedback_negative.txt"), text_size=config['TEXT_SIZE'],
                      screen_width=SCREEN_RES[0], show_time=config["FEEDBACK_SHOW_TIME"])
    time.sleep(config["WAIT_TIME"])

show_info(win, join('.', 'messages', "end.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])

import time
import random
from os import listdir
from os.path import join
from psychopy import visual, event, core, logging


class Trial:

    def __init__(self, win, config, item):
        images = [f for f in listdir(join("images", item))]

        task = [elem for elem in images if elem.split(".")[0] == item][0]
        task = visual.ImageStim(win=win, image=join('images', item, task), interpolate=True,
                                size=config['TASK_SIZE'], pos=config['TASK_POS'])

        answers = []
        for iter, elem in enumerate([elem for elem in images if elem.split(".")[0] != item]):

            pos_x = config['ANSWERS_POS'][0] - ((config["N_ANSWERS_IN_ROW"] - 1) / 2 - iter % config["N_ANSWERS_IN_ROW"]) * \
                                                (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][0])
            pos_y = config['ANSWERS_POS'][1] - iter//config["N_ANSWERS_IN_ROW"] * \
                                                (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][1])

            image = visual.ImageStim(win=win, image=join('images', item, elem), interpolate=True,
                                    size=config['ANSWERS_SIZE'], pos=[pos_x, pos_y])
            answers.append({"name": elem.split(".")[0], "image": image, "pos": [pos_x, pos_y]})
        random.shuffle(answers)

        self.name = item
        self.task = task
        self.answers = answers

    def setAutoDraw(self, draw, win):
        self.task.setAutoDraw(draw)
        for elem in self.answers:
            elem["image"].setAutoDraw(draw)
        win.flip()

    def run(self):
        pass



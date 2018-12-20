import time
import random
from os import listdir
from os.path import join
from psychopy import visual, event
from sources.check_exit import check_exit


class Trial:
    def __init__(self, win, config, item):
        images = [f for f in listdir(join("images", item))]

        task = [elem for elem in images if elem.split(".")[0] == item][0]
        task = visual.ImageStim(win=win, image=join('images', item, task), interpolate=True,
                                size=config['TASK_SIZE'], pos=config['TASK_POS'])

        answers = []
        for i, elem in enumerate([elem for elem in images if elem.split(".")[0] != item]):
            pos_x = config['ANSWERS_POS'][0] - ((config["N_ANSWERS_IN_ROW"] - 1) / 2 - i % config["N_ANSWERS_IN_ROW"]) \
                    * (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][0])
            pos_y = config['ANSWERS_POS'][1] - i//config["N_ANSWERS_IN_ROW"] \
                    * (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][1])

            image = visual.ImageStim(win=win, image=join('images', item, elem), interpolate=True,
                                     size=config['ANSWERS_SIZE'], pos=[pos_x, pos_y])

            frame = visual.Rect(win, width=config["ANSWERS_SIZE"], height=config["ANSWERS_SIZE"],
                                pos=[pos_x, pos_y], lineColor="red")
            answers.append({"name": elem.split(".")[0].split("_", 1)[1], "image": image, "frame": frame})
        random.shuffle(answers)

        self.name = item
        self.task = task
        self.answers = answers
        self.rt = None
        self.acc = None
        self.chosen_answer = None

    def setAutoDraw(self, draw, win):
        self.task.setAutoDraw(draw)
        for elem in self.answers:
            elem["image"].setAutoDraw(draw)
        win.flip()

    def run(self, config, win, response_clock, clock_image, mouse, accept_box):
        accept_box.set_start_colors()
        win.callOnFlip(response_clock.reset)
        event.clearEvents()

        accept_box.setAutoDraw(True)
        self.setAutoDraw(True, win)
        clock_is_shown = False

        while response_clock.getTime() < config["STIM_TIME"] and self.chosen_answer is None:
            for answer in self.answers:
                if mouse.isPressedIn(answer["frame"]):
                    for ans in self.answers:
                        ans["frame"].setAutoDraw(False)
                    self.acc = self.chosen_answer == "target"
                    answer["frame"].setAutoDraw(True)
                    accept_box.set_end_colors()
                    win.flip()
                    event.clearEvents()
                    break
                elif mouse.isPressedIn(accept_box.accept_box) and self.acc is not None:
                    for ans in self.answers:
                        ans["frame"].setAutoDraw(False)
                    self.rt = response_clock.getTime()
                    self.chosen_answer = answer["name"]
                    win.flip()
                    event.clearEvents()
                    break

            if not clock_is_shown and config["STIM_TIME"] - response_clock.getTime() < config["SHOW_CLOCK"]:
                clock_image.setAutoDraw(True)
                clock_is_shown = True
                win.flip()

            check_exit()
            win.flip()

        clock_image.setAutoDraw(False)
        accept_box.setAutoDraw(False)
        self.setAutoDraw(False, win)

    def info(self, exp, trial_nr):
        answers_order = [answer["name"] for answer in self.answers]
        #      ['TRIAL_NR', 'TASK_NR', 'EXPERIMENTAL', 'ACC',    'RT',     'ANSWER_TYPE',  'ANSWERS_ORDER']
        return [trial_nr,   self.name,      exp,      self.acc, self.rt, self.chosen_answer, answers_order]

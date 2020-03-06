import time
import random
from os import listdir
from os.path import join
from psychopy import visual, event
from sources.check_exit import check_exit


class Trial:
    def __init__(self, win, config, item):
        images = [f for f in listdir(join("images", item)) if not f.startswith(".")]

        task = [elem for elem in images if elem.split(".")[0] == item][0]
        task = visual.ImageStim(win=win, image=join('images', item, task), interpolate=True,
                                size=config['TASK_SIZE'], pos=config['TASK_POS'])

        answers = []
        elements = [elem for elem in images if elem.split(".")[0] != item]
        random.shuffle(elements)

        c = 0
        for n_row, number_of_elements in enumerate(config["N_ANSWERS_IN_ROW"]):
            row = elements[c:c+number_of_elements]
            c += number_of_elements
            for i, elem in enumerate(row):
                pos_x = config['ANSWERS_POS'][0] - ((number_of_elements - 1) / 2 - i % number_of_elements) \
                        * (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][0])
                pos_y = config['ANSWERS_POS'][1] - n_row * (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][1])

                image = visual.ImageStim(win=win, image=join('images', item, elem), interpolate=True,
                                         size=config['ANSWERS_SIZE'], pos=[pos_x, pos_y])

                frame = visual.Rect(win, width=config["ANSWERS_SIZE"], height=config["ANSWERS_SIZE"],
                                    pos=[pos_x, pos_y], lineColor=config["FRAME_COLOR"], lineWidth=config["FRAME_WIDTH"])
                answers.append({"name": elem.split(".")[0].split("_", 1)[1], "image": image, "frame": frame})

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

    def run(self, config, win, response_clock, clock_image, mouse, accept_box,
            feedback, feedback_positive, feedback_negative):
        accept_box.set_start_colors()
        win.callOnFlip(response_clock.reset)
        event.clearEvents()

        accept_box.setAutoDraw(True)
        self.setAutoDraw(True, win)
        clock_is_shown = False

        while response_clock.getTime() < config["STIM_TIME"]:
            for answer in self.answers:
                if mouse.isPressedIn(answer["frame"]):
                    for ans in self.answers:
                        ans["frame"].setAutoDraw(False)
                    answer["frame"].setAutoDraw(True)
                    self.chosen_answer = answer["name"]
                    self.acc = self.chosen_answer == "target"
                    accept_box.set_end_colors()
                    win.flip()
                    event.clearEvents()
                    break
            if mouse.isPressedIn(accept_box.accept_box) and self.chosen_answer is not None:
                self.rt = response_clock.getTime()
                break

            if not clock_is_shown and config["STIM_TIME"] - response_clock.getTime() < config["SHOW_CLOCK"]:
                clock_image.setAutoDraw(True)
                clock_is_shown = True
                win.flip()

            check_exit()
            win.flip()

        if feedback:
            time.sleep(config["WAIT_FOR_FEEDBACK"])
            true_answer = str(self.answers.index([a for a in self.answers if a["name"] == "target"][0]) + 1)

            feedback = feedback_positive if self.acc else feedback_negative
            print(feedback.text)
            feedback.text = feedback.text.replace("<insert>", true_answer)
            feedback.setAutoDraw(True)
            win.callOnFlip(response_clock.reset)
            accept_box.accept_label.text = config["ACCEPT_BOX_TEXT"]
            win.flip()

            while response_clock.getTime() < config["FEEDBACK_SHOW_TIME"]:
                event.clearEvents()
                if mouse.isPressedIn(accept_box.accept_box):
                    break
                check_exit()
            feedback.setAutoDraw(False)

        for ans in self.answers:
            ans["frame"].setAutoDraw(False)
        clock_image.setAutoDraw(False)
        accept_box.setAutoDraw(False)
        self.setAutoDraw(False, win)

    def info(self, exp, trial_nr):
        answers_order = [answer["name"] for answer in self.answers]
        #      ['TRIAL_NR', 'TASK_NR', 'EXPERIMENTAL', 'ACC',    'RT',     'ANSWER_TYPE',  'ANSWERS_ORDER']
        return [trial_nr,   self.name,      exp,      self.acc, self.rt, self.chosen_answer, answers_order]

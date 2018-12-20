from psychopy import visual


class AcceptBox:
    def __init__(self, win, pos, size, text, start_box_color, start_text_color, end_box_color, end_text_color):
        self.accept_box = visual.Rect(win, fillColor=start_box_color, width=size[0],
                                      height=size[1], lineColor=u'black', pos=pos)

        self.accept_label = visual.TextStim(win, text=text, height=size[1]*0.8,
                                            color=start_text_color, wrapWidth=900, pos=pos)

        self._start_box_color = start_box_color
        self._start_text_color = start_text_color
        self._end_box_color = end_box_color
        self._end_text_color = end_text_color

    def setAutoDraw(self, draw):
        self.accept_box.setAutoDraw(draw)
        self.accept_label.setAutoDraw(draw)

    def set_start_colors(self):
        self.accept_box.fillColor = self._start_box_color
        self.accept_label.fillColor = self._start_text_color

    def set_end_colors(self):
        self.accept_box.fillColor = self._end_box_color
        self.accept_label.fillColor = self._end_text_color

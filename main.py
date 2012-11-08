# -*- coding: utf-8 -*-

import os
import os.path
import sys
import GUI
import lesson
import config
import dictionary


class App(GUI.MainWindow):
	def __init__(self):
		GUI.MainWindow.__init__(self)
		self.lesson     = None
		self.practice   = None
		self.cfg        = config.Config("config.json")
		self.new_lesson()
		self.mainloop()

	def new_lesson(self):
		try:
			self.lesson = lesson.Lesson(self.cfg.reload())
		except dictionary.ErrDict as err:
			self.show_critical_error(err.loc_res_msg)
			sys.exit(0)

		self.practice = None
		self.new_practice()
		self.show()

	def end_lesson(self):
		try:
			self.lesson.end_lesson()
		except dictionary.ErrDict as err:
			self.show_critical_error(err.loc_res_msg)
			sys.exit(0)
		self.hide()
		retry_time = self.cfg.get_dict()["retry_time"] * 1000
		self.after(retry_time, self.new_lesson)

	def new_practice(self):
		if self.lesson.is_end_lesson():
			self.end_lesson()
		else:
			is_new = (self.practice == None or self.practice.is_end())
			if is_new:
				self.practice = self.lesson.get_next_practice()
			new_word = self.practice.source_data()
			self.set_stat(self.lesson.get_lesson_stat())
			self.set_word(new_word, is_new)

	def end_practice(self, user_answer):
		is_success, right_answer = self.practice.check(user_answer)
		self.set_practice_result(is_success, right_answer)

	def global_statistic(self):
		min_percent     = self.cfg.get_dict()["MinPercent"]
		min_success_cnt = self.cfg.get_dict()["MinSuccessCnt"]
		return self.lesson.get_dict().global_statistic(min_percent, min_success_cnt)


def run():
	import singleton
	singleton.SingleInstance()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	App()

if __name__ == "__main__":
	run()

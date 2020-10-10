from pprint import pprint
import nose
from nosetimer import plugin

test_results = []

plugin = plugin.TimerPlugin()
plugin.enabled = True
plugin.timer_ok = 1000
plugin.timer_warning = 2000
plugin.timer_no_color = False

with open("test_times_optimise_v_2.csv","a") as json_file:
   for i in range(10):

      nose.run(plugins=[plugin])
      result = plugin._timed_tests

      for test in result:
         test_split = test.split(".")
         test_class = test_split[1]
         test_func = test_split[2]
         print(f"{test_class},{test_func},{result[test]['time']}",file=json_file)

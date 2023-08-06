import json
import unittest

from walnut_agent.script.util_handle import route


class Test(unittest.TestCase):

    def test_get(self):
        log_txt = route.LOG_PATH / 'log.txt'
        with log_txt.open('r', encoding='utf8') as f:
            logs = f.read()
        for step in logs.splitlines():
            step = json.loads(step)
            if step['tag'] != 'function':
                continue

            print(step)


if __name__ == '__main__':
    unittest.main()

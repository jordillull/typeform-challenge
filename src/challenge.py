'''

Created on Jul 4, 2015

@author: Jordi Llull
'''

import requests

N_CHALLENGES = 20
GET_PROBLEM_URL = "http://aerial-valor-93012.appspot.com/challenge"
SOLVE_CHALLENGE_URL = "http://aerial-valor-93012.appspot.com/challenge/{token}/{answer}"

class Challenge(object):

    def __init__(self, token, values):
        self.token  = token
        self.values = values

    @property
    def answer(self):
        return sum(self.values)

    def __str__(self):
        string = ("Token: {c.token}\n"
                 "Values: {c.values}\n"
                 "Answer: {c.answer}")

        return string.format(c=self)

def get_challenge():
    r = requests.get(GET_PROBLEM_URL)
    if r.status_code != 200:
        raise IOError('Server returned an unexpected status code: {0}'.format(r.status_code))

    json = r.json()

    return Challenge(json['token'], json['values'])

def solve_challenge(challenge):
    url = SOLVE_CHALLENGE_URL.format(token=challenge.token, answer=challenge.answer)

    r = requests.get(url)
    if r.status_code != 200:
        raise IOError('Server returned an unexpected status code: {0}'.format(r.status_code))

    json = r.json()

    if 'error' in json.keys():
        return False
    elif 'answer' in json.keys():
        return True
    else:
        raise ValueError('Got an unexpected response from the server: {0}'.format(r.text()))

def main():
    for _ in range(N_CHALLENGES):
        c = get_challenge()
        if (solve_challenge(c)):
            print("Solved challenge {0}".format(c.token))
        else:
            print("Unable to solve a challenge!\n{0}\n".format(c))

if __name__ == '__main__':
    main()

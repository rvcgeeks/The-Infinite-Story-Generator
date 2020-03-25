#!/usr/bin/python3

# markov chain (with distribution) infinite text generator
# created by rvcgeeks
# <github.com/rvcgeeks>
# <linkedin.com/in/rvchavadekar>
# <rvchavadekar@gmail.com>
# works with python3

import queue
from re import sub
from os import write
from sys import argv
from time import sleep
from random import random, choice
from collections import defaultdict

def tokenise_text_files(file_names):
  tokens = []
  for file_name in file_names:
    try: 
      input_file = open(file_name, 'r')
      tokens += [sub(r'[^a-zA-Z0-9.,;?!\"\']+', '', lexeme) for lexeme in ' '.join(input_file).split()]
      input_file.close()
    except Exception as e:
      print(e, 'in file ' + file_name)
  return tokens

def get_next_state(markov_chain, state):
  next_state_items = list(markov_chain[state].items())
  next_states = [x[0] for x in next_state_items]
  next_state_counts = [x[1] for x in next_state_items]
  total_count = sum(next_state_counts)
  next_state_probabilities = []
  probability_total = 0
  for next_state_count in next_state_counts:
    probability = float(next_state_count) / total_count
    probability_total += probability
    next_state_probabilities.append(probability_total)
  sample = random()
  for index, next_state_probability in enumerate(next_state_probabilities):
    if sample <= next_state_probability:
      return next_states[index]
  return None

def create_markov_chain(tokens, order):
  if order > len(tokens):
    raise Exception('Order greater than number of tokens.')
  markov_chain = defaultdict(lambda: defaultdict(int))
  current_state_queue = queue.Queue()
  for index, token in enumerate(tokens):
    if index < order:
      current_state_queue.put(token)
      if index == order - 1:
        current_state = ' '.join(list(current_state_queue.queue))
    elif index < len(tokens):
      current_state_queue.get()
      current_state_queue.put(token)
      next_state = ' '.join(list(current_state_queue.queue))
      markov_chain[current_state][next_state] += 1
      current_state = next_state
  return markov_chain

def get_random_state(markov_chain):
  uppercase_states = [state for state in markov_chain.keys() if state[0].isupper()]
  if len(uppercase_states) == 0:
    return choice(list(markov_chain.keys()))
  return choice(uppercase_states)

def text_generator(markov_chain):
  state = get_random_state(markov_chain)  #random starting words
  try: yield state.split()[-1]
  except : yield ''
  while True:
    state = get_next_state(markov_chain, state)
    if state is None:
      state = get_random_state(markov_chain)  #again make a new start, maybe this path got ended
    try: yield ' ' + state.split()[-1]
    except: yield ''

if __name__ == '__main__':
  fnlist = argv[1: -2]
  print(' generating from files : %s\n\n\n' % fnlist)
  tokens = tokenise_text_files(fnlist)
  markov_chain = create_markov_chain(tokens, order=int(argv[-2]))
  if argv[-1] == 'p': # just to show the chain
    from json import dumps
    json_file = open('markov_chain.json', 'w')
    json_file.write(dumps(markov_chain, indent=4))
    json_file.close()
  len_cnt = 1
  for word in text_generator(markov_chain):
    write(1, word.encode())
    l = len(word)
    len_cnt += l + 1
    sleep(0.03 * len(word))
    if len_cnt > 100:
      write(1, b'\n')
      len_cnt = 0

DEBUG:root:Chapter 0
Traceback (most recent call last):
  File "main.py", line 107, in <module>
    generate_book(args.num_chaps)
  File "main.py", line 91, in generate_book
    r.simulate()
  File "/Users/sylvan/code/nanogenmo/relationship.py", line 541, in simulate
    meeting = self.simulate_meeting()
  File "/Users/sylvan/code/nanogenmo/relationship.py", line 334, in simulate_meeting
    logging.debug(
NameError: name 'logging' is not defined

"""
Should Include:
A class representing a log (for formatting in different places)
Buffer classes (for keeping logs locally before pushing online)
Log classes (for standardizing how logs are sent)
"""

import logging

## Logging levels are as follows:
# Note that commented definitions are default for the logging module anyway

# logging.NOTSET = 0
logging.RAW_DEBUG = 3
logging.USER_RAW_DEBUG = 4
# logging.DEBUG = 9
logging.STANDARD_DEBUG = 13
logging.HELPFUL_DEBUG = 14
# logging.INFO = 19
logging.STANDARD_INFO = 23
logging.HELPFUL_INFO = 24
# logging.WARNING = 29
logging.STANDARD_WARNING = 33
logging.HELPFUL_WARNING = 34
# logging.ERROR = 39
logging.STANDARD_ERROR = 43
logging.HELPFUL_ERROR = 44
logging.PRIVATE_ERROR = 48
# logging.CRITICAL = 49
logging.STANDARD_CRITICAL = 53
logging.HELPFUL_CRITICAL = 54
logging.PRIVATE_CRITICAL = 57
logging.FATAL_CRITICAL = 58
logging.CORRUPTED_CRITICAL = 59

# Which channels should I use?
# logging.NOTSET # for None (sentinel value)
logging.USER_RAW_DEBUG  # for raw debugging
logging.HELPFUL_DEBUG  # for debugging generally
logging.HELPFUL_INFO  # for logging info
logging.HELPFUL_WARNING  # for logging warnings
# for logging errors, specifically recoverable errors by reloading or some other specified method
logging.HELPFUL_ERROR
logging.HELPFUL_CRITICAL  # for logging critical, specifically fatal, error

# Logging levels practical documentation
"""
Where do my logs go?
  There are a few places, as listed below with their typically used names:

**Console** (stdout, print, terminal, debug console): This is pretty self explanatory, the environment this program is run in being python always has an stdout and stderr so 'Console' refers to this (stdout)
**Preset Logs** (/logs/presetlogfile.txt file, or other set place): A preset *hard coded* place to send logs to
**Private DM** (note: adds to buffer and sends as soon as possible): A private DM to the ***ADMIN*** user, this is useful for debugging and error reporting
**Online Server Handled Logs** (note: *not* the same as private DM, aka Server Handled Logs, Discord Server Logs e.t.c.): Logs that are sent (buffered technically) to the appropriate discord server depending on the server setup with the bot

NOTSET: Nowhere
Raw debug channels (< 9): Console only (raw printed)
Debug channels (9 <= n < 20): Console and preset logs (raw printed)
Info channels (19 <= n < 30): Console, preset logs, and Server Handled Logs
Warning channels (29 <= n < 40): Console, preset logs, and special Server Handled Logs
Error channels (39 <= n < 50): Console, preset logs, special Server Handled Logs and a general notification to the ***STEWARDS*** of the bot
Critical channels (49 <= n < 59): All of the above AND a private DM to the ***ADMIN*** user and a soft notification to all adjoining servers and channels (if possible)
FATAL channels (n == 59), note this channel group does not really exist I just sort of defined it, but it is useful for corrupted data that may mean a discord bot dies completely: ALL of the above + a ping to all adjoining servers and channels (if possible)
"""

# Complete non-user-friendly documentation for logging levels:
"""
**An actual description of logging levels are as follows:**
  # NOTSET = 0, this is a sentinel value representing a level that is not defined (not set)
  > RAW_DEBUG = 3, this is the lowest level of debug messages used internally by the bot
  > USER_RAW_DEBUG = 4, this is the lowest level of debug messages used by the user and is the encouraged lowest level of debug message for the user
  
  # DEBUG = 9, this is not a sentinel value but is the original value of debug for the logging module
  > STANDARD_DEBUG = 13, this is the normal level of debug used by the bot and will typically describe internal events
  > HELPFUL_DEBUG = 14, this is the recommended user debug level for most things just debugging
  
  # INFO = 19, this is not a sentinel value but is the original value of info for the logging module
  > STANDARD_INFO = 23, this is the normal level of info used by the bot and will typically describe internal actions with a meaningful timestamp
  > HELPFUL_INFO = 24, this is the recommended user info level for most things just informational, try to aim for something meaningful maybe with a timestamp?
  
  # WARNING = 29, this is not a sentinel value but is the original value of warning for the logging module
  > STANDARD_WARNING = 33, this is the normal level of warnings by the bot and will typically only include warnings of significance that inhibit actual functionality, implementation warnings are typically found in STANDARD_INFO
  > HELPFUL_WARNING = 34, this is the recommended user warning level for most warnings, although you can really use any arbitrary number logs >30 will be treated with slightly more 'respect' and are designed around being informative and meaningful

  # ERROR = 39, this is not a sentinel value but is the original value of error for the logging module
  > STANDARD_ERROR = 43, this is the normal level of error used by the bot and will typically describe internal events that are recoverably *only* with a restart / reloading process, concerning internal / implementation details
  > HELPFUL_ERROR = 44, this is the recommended user error level for most errors, although you can really use any arbitrary number logs >40 will be treated with slightly more 'oomph' and are designed around being informative, meaningful, and with a workaround or reload process to circumvent the issue / error. If this is not possible, i.e. recovery from the error, than put it into a *_CRITICAL logging level such as 50

  # CRITICAL = 49, this is not a sentinel value but is the original value of critical for the logging module
  > STANDARD_CRITICAL = 53, this is the normal level of critical used by the bot and will typically describe internal events that are irrecoverably period. This is the level that should be used when the bot is unable to recover from the error, or when the bot is unable to continue functioning.
  > HELPFUL_CRITICAL = 54, this is the recommended user critical level for most errors, although you can really use any arbitrary number logs >50 will be treated with slightly more 'oomph' and are designed around being informative, meaningful, but sadly un-recoverable. Restarting / reloading is probably not going to solve the problem
  > PRIVATE_CRITICAL = 57, this is a **private** logging level used to typically DM (if still possible) an admin (or myself) of the error and a basic error handle / code. Rigging this up is *NOT* an added feature (at time of writing) and used only as a failsafe
  > FATAL_CRITICAL = 58, this is a generic logging level used to indicate a, well, fatally critical error of any kind ONLY related to *the programming side*, so not something like a loss of internet or battery failure e.t.c.
  > CORRUPTED_CRITICAL = 59, this is a logging level dedicated to uncontrollable, fatal corruption of programming, or some other generic corruption. If a SEU (Single Event Upset) occurs, this is the level that should most of the time be 'raised' on :)

**Logging levels num summary:**
  1-4 = Raw debug
  4-10 = User Raw debug

  # CUTOFF for private data, all logs >9 should not contain any private data such as the discord bots token or any other sensitive data
  10-14 = Standard debug
  14-19 = Helpful debug

  19-24 = Standard info
  24-29 = Helpful info

  29-34 = Standard warning
  34-39 = Helpful warning

  39-44 = Standard error
  44-49 = Helpful error

  # CUTOFF for implementation-detail data, all logs >=39 should contain __user friendly__ text, so that a general user could understand the problem at least generally. Try not to include details related to the actual implementation of the bot
  50-54 = Standard critical
  54-57 = Helpful critical

  57-58 = Private critical # Think a personal DM message
  58-59 = Fatal critical
  59-60 = Corrupted critical # Think an impossible result such as corrupted data or a SEU
"""


class log():
  def __init__(self, msg, *, level=0):
    self.msg = msg


class loggerInterface():
  def __init__(self, logOutput=logging.getLogger(__name__)):
    self.logOutput = logOutput

  def pushLog(log):
    ...

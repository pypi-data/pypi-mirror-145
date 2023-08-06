"""
Should Include:
Basic error classes and their descriptors
"""

# Repeated code with __init__ and extra, will eventually be removed or multiple inheritance from CustomError but that


class UserErrorHandle():
  """
  Class that handles errors the user can identify / recover from
  """

  def __init__(self, msg, *msgs, **extra):
    self.msg = f"Message: {msg}\n{'\n'.join(msgs)}"
    self.extras = extra

  def __str__(self):
    return f"{self.msg}\n" + "\n".join(f"{k}: {v}" for k, v in self.extras.items())


class CustomError(Exception):
  """
  Exception class that is root of all custom exceptions
  """

  def __init__(self, msg, *msgs, **extra):
    self.msg = f"Message: {msg}\n{'\n'.join(msgs)}"
    self.extras = extra

  def __str__(self):
    return f"{self.msg}\n" + "\n".join(f"{k}: {v}" for k, v in self.extras.items())


class ProgrammerError(CustomError):
  """
  Exception class that is root of all programmer related exceptions
  """
  ...


class InappropriateRequest(ProgrammerError):
  """
  Exception class that is raised when a request on some programming object / function / property is inappropriate
  """
  ...

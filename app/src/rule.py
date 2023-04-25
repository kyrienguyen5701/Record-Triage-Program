from abc import ABC, abstractmethod

class Evaluable(ABC):
  
  @abstractmethod
  def evaluate(self):
    raise NotImplementedError('Subclass must implement evaluate method')

# Composite Design Pattern for easily extending 
# as many Conditions or Rules within a Rule
class Rule(Evaluable):
  def __init__(self, condition, priority=0):
    self.condition = condition
    self.next_conditions = []
    self.priority = priority

  def add_and(self, condition):
    self.next_conditions.append(('and', condition))

  def add_or(self, condition):
    self.next_conditions.append(('or', condition))

  def evaluate(self):
    result = self.condition.evaluate()
    for operator, condition in self.next_conditions:
      if operator == 'and':
        result &= condition.evaluate()
      elif operator == 'or':
        result |= condition.evaluate()
    return result
    
class Condition(Evaluable):
  def __init__(self, src, op, tgt):
    self.src = src
    self.op = op
    self.tgt = tgt
    
  def evaluate(self):
    return eval(f'"{self.src}" {self.op} "{self.tgt}"')
import git
import os


def getPercent(value):
  return f'{value * 100}%'

def get_jaccard_sim(text1, text2):
    a = set(text1)
    b = set(text2)
    c = a.intersection(b)

    return float(len(c)) / (len(a) + len(b) - len(c))

class UserTask:
  def __init__(self, userName, taskName, localPath):
    self.userName = userName
    self.taskName = taskName
    self.localPath = localPath

    self._cloneProject()
  
  def _cloneProject(self):
    self.path = os.path.join(self.localPath, self.userName)

    try:
      os.makedirs(self.path)
      git.Git(self.path).clone(f'https://github.com/{self.userName}/{self.taskName}.git')
    except OSError:
      print ("Creation of the directory %s failed" % self.path)

  def getText(self, path):
    with open (os.path.join(self.path, self.taskName, path), "r") as f:
      return f.read()

class UserList:
  def __init__(self, users, taskName, localPath, checkPaths):
    self.taskName = taskName
    self.localPath = localPath
    self.checkPaths = checkPaths
    self.usersTasks = {}
    
    self._createUserTasks(users)

  def _createUserTasks(self, users):
    for user in users:
      self.usersTasks[user] = UserTask(user, self.taskName, self.localPath)
  
  def compare(self, userNameA, userNameB, path):
    userA = self.usersTasks[userNameA]
    userB = self.usersTasks[userNameB]

    textA = userA.getText(path)
    textB = userB.getText(path)

    return get_jaccard_sim(textA, textB)  

  def cloneCheck(self, path, userA, userB, thresholdValue):
    res = self.compare(userA, userB, path)

    if res >= thresholdValue:
      return f'Clone: {getPercent(res)}\n'
    return ''


  def createResultRow(self, path, userA, userB, cloneCheckResult):
    return f'Task: {path}\tUser: {userA} -> {userB}\t{cloneCheckResult}'

  def crossCheck(self):
    for taskPath in self.checkPaths:
      for userA in self.usersTasks:
        for userB in self.usersTasks:
          
          res = self.cloneCheck(taskPath, userA, userB, 0.9)
          if res:
            print(self.createResultRow(taskPath, userA, userB, res))


  # Tests
  
  def _testPaths(self):
    for task in self.usersTasks:
      for path in self.checkPaths:
        print(task.getText(path))

if __name__ == "__main__":
  users = ['sovaz1997', 'hallovarvara', 'inq666', 'torchik-slava', 'alexeikravchuk']
  chechPaths = [
    os.path.join('src', 'carbon-dating.js')
  ]

  userList = UserList(users, 'basic-js', os.path.join('.', 'data'), chechPaths)
  userList.crossCheck()
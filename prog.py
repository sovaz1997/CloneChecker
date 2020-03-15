import git
import os

from bs4 import BeautifulSoup


DOWNLOAD_DATA = False
LIMIT = 1.0

def getPercent(value):
  return f'{value * 100}%'

def get_jaccard_sim(text1, text2):
    a = set(text1)
    b = set(text2)
    c = a.intersection(b)

    return float(len(c)) / (len(a) + len(b) - len(c))


def parseScores(path):
  pageText = open(path,'r').read()
  page = BeautifulSoup(pageText, 'html.parser')
  
  users = set()

  for user in page.find_all('tr'):
    if user.has_attr('data-row-key'):
      users.add(user.get('data-row-key'))

  return list(users)

class UserTask:
  def __init__(self, userName, taskName, localPath):
    self.userName = userName
    self.taskName = taskName
    self.localPath = localPath

    self.success = self._cloneProject()
  
  def _cloneProject(self):
    self.path = os.path.join(self.localPath, self.userName)
    self.fullPath = os.path.join(self.path, self.taskName)
    
    if not DOWNLOAD_DATA:
      return True

    try:
      os.makedirs(self.fullPath)
    except OSError:
      print ("Creation of the directory %s failed" % self.path)

    if not os.listdir(self.fullPath):
      try:
        git.Git(self.path).clone(f'https://github.com/{self.userName}/{self.taskName}.git')
      except git.exc.GitError:
        return False
    return True

  def getText(self, path):
    textPath = os.path.join(self.path, self.taskName, path)

    if not os.path.exists(textPath):
      return False
    with open (textPath, "r", encoding='utf-8', errors='ignore') as f:
      return f.read()

class UserList:
  def __init__(self, users, taskName, localPath, checkPaths):
    self.taskName = taskName
    self.localPath = localPath
    self.checkPaths = checkPaths
    self.usersTasks = {}
    
    self._createUserTasks(users)

  def _createUserTasks(self, users):
    i = 0
    for user in users:
      task = UserTask(user, self.taskName, self.localPath)
      
      if task.success:
        self.usersTasks[user] = task
      
        print(f'Downloaded: {i + 1}/{len(users)}')
        i += 1
  
  def compare(self, userNameA, userNameB, path):
    userA = self.usersTasks[userNameA]
    userB = self.usersTasks[userNameB]

    textA = userA.getText(path)
    textB = userB.getText(path)

    if not (textA and textB):
      return False

    return get_jaccard_sim(textA, textB)

  def cloneCheck(self, path, userA, userB, thresholdValue):
    res = self.compare(userA, userB, path)

    if not res:
      return False

    if res >= thresholdValue:
      return f'Clone: {getPercent(res)}\n'
    return ''


  def createResultRow(self, path, userA, userB, cloneCheckResult):
    return f'Task: {path}\tUser: {userA} -> {userB}\t{cloneCheckResult}'

  def crossCheck(self):
    for taskPath in self.checkPaths:
      for userA in self.usersTasks:
        for userB in self.usersTasks:
          if userA != userB:
            res = self.cloneCheck(taskPath, userA, userB, LIMIT)
            if res:
              print(self.createResultRow(taskPath, userA, userB, res))

if __name__ == "__main__":
  users = []

  for i in range(1, 23):
    users += parseScores(os.path.join('.', 'scores', f'{i}.html'))
  chechPaths = [
    os.path.join('index.html'),
    os.path.join('style.css'),
  ]

  #userList = UserList(users, 'basic-js', os.path.join('.', 'data'), chechPaths)

  userList = UserList(users, 'singolo', os.path.join('.', 'data'), chechPaths)
  userList.crossCheck()
import git
import os

from bs4 import BeautifulSoup


DOWNLOAD_DATA = False
LIMIT = .3


def detectComponents(graph, key, detected):
  for v in graph[key]:
    if not v in detected:
      detected.add(v)
      detectComponents(graph, v, detected)


def getPercent(value):
  return f'{value * 100}%'

def get_jaccard_sim(text1, text2):
    a = set(text1.split())
    b = set(text2.split())
    c = a.intersection(b)

    if len(a) + len(b) - len(c) == 0:
      return 0

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
      return False, 0

    if res >= thresholdValue:
      return f'Similarity: {getPercent(res)}', res * 100
    return '', 0


  def createResultRow(self, path, userA, userB, cloneCheckResult):
    return f'Path: {path}\tUser: {userA} <-> {userB}\t{cloneCheckResult}'

  def crossCheck(self):
    graph = dict()
    i = 1
    for userA in self.usersTasks:
      print(f'{i/len(self.usersTasks)*100}%')
      self.checkUser(userA, graph)
      i += 1
    
    self.printComponents(graph)
  
  def printComponents(self, graph):
    allComponents = set()


    for i in graph.keys():
      if not i in allComponents:
        localComponents = set()
        detectComponents(graph, i, localComponents)
        allComponents = allComponents.union(localComponents)
        print(localComponents)

  
  def checkUser(self, user, graph=None):
    nodes = set()

    hist = [0] * 101

    with open('crosscheck.txt', 'w') as f: 
      for taskPath in self.checkPaths:
        for userB in self.usersTasks:
          if user != userB:
            res, val = self.cloneCheck(taskPath, user, userB, LIMIT)
            hist[round(val)] += 1
            if res:
              line = self.createResultRow(taskPath, user, userB, res)

              if graph != None:
                if not user in graph.keys():
                  graph[user] = []
                
                if not userB in graph.keys():
                  graph[userB] = []

                graph[user].append(userB)
                graph[userB].append(user)

              print(line)
              f.write(line + '\n')
    
    index = 0
    for i in hist:
      print(f'{index}% similarity: {i}', end='; ')
      if index % 5 == 0:
        print()
      index += 1


if __name__ == "__main__":
  users = []

  for i in range(1, 23):
    users += parseScores(os.path.join('.', 'scores', f'{i}.html'))
  chechPaths = [
    os.path.join('script.js'),
  ]

  '''os.path.join('src', 'carbon-dating.js'),
    os.path.join('src', 'count-cats.js'),
    os.path.join('src', 'dream-team.js'),
    os.path.join('src', 'extended-repeater.js'),
    os.path.join('src', 'hanoi-tower.js'),
    os.path.join('src', 'recursive-depth.js'),
    os.path.join('src', 'transform-array.js'),
    os.path.join('src', 'vigenere-cipher.js'),
    os.path.join('src', 'what-season.js')'''

  userList = UserList(users, 'singolo', os.path.join('.', 'data'), chechPaths)
  
  # userList.crossCheck()
  userList.checkUser('sovaz1997')
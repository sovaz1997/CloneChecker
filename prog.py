import git
import os

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
  
  def get_jaccard_sim(self, text1, text2):
    print(text1)
    a = set(text1)
    b = set(text2)
    c = a.intersection(b)

    return float(len(c)) / (len(a) + len(b) - len(c))
  
  def compare(self, userNameA, userNameB, path):
    userA = self.usersTasks[userNameA]
    userB = self.usersTasks[userNameB]

    textA = userA.getText(path)
    textB = userB.getText(path)

    print(textA)
    print(textB)

    return self.get_jaccard_sim(textA, textB)  
  
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
  print(userList.compare('sovaz1997', 'alexeikravchuk', os.path.join('src', 'vigenere-cipher.js')))
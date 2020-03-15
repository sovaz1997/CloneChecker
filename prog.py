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
      return f.readlines()


class UserList:
  def __init__(self, users, taskName, localPath, checkPaths):
    self.users = users
    self.taskName = taskName
    self.localPath = localPath
    self.checkPaths = checkPaths
    self._createUserTasks()
    self._testPaths()

  def _createUserTasks(self):
    self.usersTasks = []
    for user in self.users:
      self.usersTasks.append(UserTask(user, self.taskName, self.localPath))
  
  def _testPaths(self):
    for task in self.usersTasks:
      for path in self.checkPaths:
        print(task.getText(path))

if __name__ == "__main__":
  users = ['sovaz1997', 'hallovarvara', 'inq666', 'torchik-slava']
  chechPaths = [
    os.path.join('src', 'carbon-dating.js')
  ]

  userList = UserList(users, 'basic-js', os.path.join('.', 'data'), chechPaths)
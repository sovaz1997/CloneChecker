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

def cloneProject(userName, taskName, localPath):
  path = os.path.join(localPath, userName)

  try:
    os.makedirs(path)
    git.Git(path).clone(f'https://github.com/{userName}/{taskName}.git')
  except OSError:
    print ("Creation of the directory %s failed" % path)


def createUserTasks(users, taskName, localPath):
  usersTasks = []
  for user in users:
    usersTasks.append(UserTask(user, taskName, localPath))
    cloneProject(user, taskName, localPath)

if __name__ == "__main__":
  users = ['sovaz1997', 'hallovarvara', 'inq666', 'torchik-slava']
  tasks = createUserTasks(users, 'basic-js', os.path.join('.', 'data'))
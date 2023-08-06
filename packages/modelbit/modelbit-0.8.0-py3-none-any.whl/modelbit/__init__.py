__version__ = "0.8.0"
__author__ = 'Modelbit'

import os, sys, zipimport
from typing import cast, Union, Callable, Any, Dict, List

from . import modelbit_core
from . import datasets
from . import warehouses
from . import runtime
from . import deployments
from . import training_jobs
from . import secure_storage
from . import utils
from . import helpers
from . import session
from . import model_wrappers

# Nicer UX for customers: from modelbit import Deployment
class Deployment(runtime.Deployment): ...
class TrainingJob(runtime.TrainingJob): ...

class _ClientSession:
  def _resetState(self):
    self._mbCore = modelbit_core.ModelbitCore(__version__)
    self._mbCore.performLogin()
    session.rememberSession(self)
  
  def __init__(self):
    self._resetState()

  # Interface for pickle. We don't currently _need_ to save anything, and explicitly don't want to save auth state
  def __getstate__(self):
    pickleState: Dict[str, str] = {}
    return pickleState # need to return something. Returning None won't call setstate

  def __setstate__(self, pickledState: Dict[str, str]):
    self._resetState()

  def __str__(self):
    return "modelbit.login()"

  def _objIsDeployment(self, obj: Any):
    try:
      if type(obj) in [Deployment, TrainingJob, runtime.Deployment, runtime.TrainingJob]: return True
      # catch modelbit._reload() class differences
      if obj.__class__.__name__ in ['Deployment', 'TrainingJob']: return True
    except:
      return False
    return False

  # Public mb.* API
  def isAuthenticated(self): return self._mbCore.isAuthenticated(True)
  
  def printAuthenticatedMsg(self): return self._mbCore.printAuthenticatedMsg()
  
  def datasets(self): return datasets.Datasets(self._mbCore)
  
  def get_dataset(self, dataset_name: str): return datasets.Datasets(self._mbCore).get(dataset_name)

  def get_training_job(self, training_job_name: str, version: Union[str, int, None] = None):
    return training_jobs.TrainingJobs(self._mbCore).get(training_job_name, version)
  
  def warehouses(self): return warehouses.Warehouses(self._mbCore)

  def Deployment(self, 
      name: Union[str, None] = None,
      deploy_function: Union[Callable[..., Any], None] = None,
      python_version: Union[str, None] = None,
      requirements_txt_filepath: Union[str, None] = None,
      requirements_txt_contents: Union[List[str], None] = None):
    return Deployment(name=name, deploy_function=deploy_function, python_version=python_version,
      requirements_txt_filepath=requirements_txt_filepath, requirements_txt_contents=requirements_txt_contents)

  def TrainingJob(self,
      name: Union[str, None] = None,
      train_function: Union[Callable[..., Any], None] = None,
      python_version: Union[str, None] = None,
      requirements_txt_filepath: Union[str, None] = None,
      requirements_txt_contents: Union[List[str], None] = None):
    return TrainingJob(name=name, train_function=train_function, python_version=python_version,
      requirements_txt_filepath=requirements_txt_filepath, requirements_txt_contents=requirements_txt_contents)
  
  def deployments(self): return deployments.Deployments(self._mbCore)

  def training_jobs(self): return training_jobs.TrainingJobs(self._mbCore)

  def _createRuntime(self,
      rtType: helpers.RuntimeType,
      deployableObj: Union[Callable[..., Any], runtime.Runtime, None],
      name: Union[str, None] = None,
      python_version: Union[str, None] = None):
    if not self.isAuthenticated():
      self._mbCore.performLogin()
      return
    if self._objIsDeployment(deployableObj):
      deployableObj = cast(runtime.Runtime, deployableObj)
      if deployableObj.rtType == helpers.RuntimeType.TrainingJob and rtType == helpers.RuntimeType.Deployment:
        return print("Error: Use .train(...) instead of .deploy(...) with this Training Job")
      elif deployableObj.rtType == helpers.RuntimeType.Deployment and rtType == helpers.RuntimeType.TrainingJob:
        return print("Error: Use .deploy(...) instead of .train(...) with this Deployment")
      return deployableObj.deploy(self._mbCore)
    if callable(deployableObj):
      if rtType == helpers.RuntimeType.Deployment:
        dep = self.Deployment(name=name, deploy_function=deployableObj, python_version=python_version)
        return dep.deploy(self._mbCore)
      elif rtType == helpers.RuntimeType.TrainingJob:
        tj = self.TrainingJob(name=name, train_function=deployableObj, python_version=python_version)
        return tj.deploy(self._mbCore)
    if hasattr(deployableObj, "__module__") and "sklearn" in deployableObj.__module__ and hasattr(deployableObj, "predict"):
      return model_wrappers.SklearnPredictor(deployableObj, name=name, python_version=python_version).makeDeployment().deploy()
    
    print("First argument doesn't looks like a deployable object.")

  def deploy(self,
      deployableObj: Union[Callable[..., Any], runtime.Deployment, None] = None,
      name: Union[str, None] = None,
      python_version: Union[str, None] = None,
      pycaret_classifier_name: Union[str, None] = None):
    if pycaret_classifier_name:
      return model_wrappers.PyCaretClassification(pycaret_classifier_name).makeDeployment(name=name).deploy()
    return self._createRuntime(helpers.RuntimeType.Deployment, deployableObj, name=name, python_version=python_version)

  def train(self,
      deployableObj: Union[Callable[..., Any], runtime.TrainingJob, None],
      name: Union[str, None] = None,
      python_version: Union[str, None] = None):
    return self._createRuntime(helpers.RuntimeType.TrainingJob, deployableObj, name=name, python_version=python_version)

def login():
  existingSession = cast(Union[_ClientSession, None], session.anyAuthenticatedSession())
  if existingSession:
    existingSession.printAuthenticatedMsg()
    return existingSession
  return _ClientSession()

def load_value(name: str):
  if "snowparkZip" in os.environ:
    zipPath = [p for p in sys.path if p.endswith(os.environ["snowparkZip"])][0]
    importer = zipimport.zipimporter(zipPath)
    # Typing thinks the response is a string, but we get bytes
    val64 = cast(bytes, importer.get_data(f"{name}.pkl")).decode()
    return secure_storage.unpickleObj(val64)
  extractPath = ""
  if 'MB_EXTRACT_PATH' in os.environ: extractPath = os.environ['MB_EXTRACT_PATH']
  f = open(f"{extractPath}/{name}.pkl", "r")
  val64 = f.read()
  f.close()
  return secure_storage.unpickleObj(val64)

def _reload(): # type: ignore
  import importlib
  importlib.reload(modelbit_core)
  importlib.reload(datasets)
  importlib.reload(warehouses)
  importlib.reload(runtime)
  importlib.reload(deployments)
  importlib.reload(training_jobs)
  importlib.reload(secure_storage)
  importlib.reload(utils)
  importlib.reload(helpers)
  importlib.reload(model_wrappers)
  importlib.reload(importlib.import_module("modelbit"))
  print("All modules reloaded, except session.")

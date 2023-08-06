from typing import Dict, Any, Union, List, cast
import pandas, numpy, inspect, re

from .utils import pandasTypeToPythonType, simplifyArgName, printMk
from .runtime import Deployment

class PyCaretClassification:
  _pickleArgs = ["modelName", "pickleFileData", "modelInputs"]

  def __init__(self, modelName: str):
    self.modelName = modelName
    self.loadedModel: Union[Any, None] = None
    self.droppedCols: List[str] = []

  def makeDeployment(self, name: Union[str, None] = None):
    if not name: name = self.modelName
    dep = Deployment(
      deploy_function=self.makeDeployFunc(),
      source_override=self.getDeployFuncSource(),
      python_version="3.8",
      requirements_txt_contents=["pycaret==2.3.6"],
      name=name
    )
    if self.droppedCols:
      printMk(f"Note: These columns were in training but are not needed for deployment: {', '.join(self.droppedCols) }")
    return dep

  def getDeployFuncSource(self):
    self._captureModelInfo()
    codeParts: List[str] = []
    funcArgs = ",\n    ".join([f"{simplifyArgName(k)}: {v}" for k, v in self.modelInputs.items()])
    dfArgs = ",\n      ".join([simplifyArgName(k) for k in self.modelInputs.keys()])
    globals()["pyc"] = self
    codeParts.append(f"def predict(\n    {funcArgs}) -> float:")
    codeParts.append(f"  return pyc.predict(\n      {dfArgs})")
    return "\n".join(codeParts)

  def makeDeployFunc(self):
    exec(self.getDeployFuncSource())
    return locals()["predict"]

  def __str__(self): return f'PyCaretClassification("{self.modelName}")'
  
  def __getstate__(self):
    pickleState: Dict[str, Any] = {}
    for pArg in self._pickleArgs:
      pickleState[pArg] = self.__getattribute__(pArg)
    return pickleState

  def __setstate__(self, pickledState: Dict[str, Any]):
    for pArg in self._pickleArgs:
      self.__setattr__(pArg, pickledState[pArg])
    self.writePickleFileToTmp()

  def _captureModelInfo(self):
    self.pickleFileData = self.readPickleFile()
    self.writePickleFileToTmp()
    self.modelInputs = self.getModelInputs()
    self.droppedCols = self.getDroppedCols()
  
  def loadModelFromTmp(self) -> Any:
    import pycaret.classification # type: ignore
    if not hasattr(self, "loadedModel") or self.loadedModel == None:
      self.loadedModel = pycaret.classification.load_model(f"/tmp/{self.modelName}", verbose=False) # type: ignore
    return self.loadedModel # type: ignore

  def readPickleFile(self):
    f = open(f"{self.modelName}.pkl", "rb")
    data = f.read()
    f.close()
    return data

  def writePickleFileToTmp(self):
    f = open(f"/tmp/{self.modelName}.pkl", "wb")
    f.write(self.pickleFileData)
    f.close()

  def getModelInputs(self):
    colTypes: Dict[str, str] = {}
    dTypes = self.loadModelFromTmp().named_steps.dtypes
    dtypeDict: Dict[str, str] = dTypes.learned_dtypes
    for argName, pandasType in dtypeDict.items():
      colTypes[argName] = pandasTypeToPythonType(pandasType)
    return colTypes

  def getDroppedCols(self):
    dCols: List[str] = []
    try:
      dTypes = self.loadModelFromTmp().named_steps.dtypes
      if dTypes.features_todrop and len(dTypes.features_todrop) > 0:
        for c in dTypes.features_todrop:
          dCols.append(c)
      if dTypes.target:
        dCols.append(dTypes.target)
    except Exception as err:
      printMk(f"Unable to detect dropped columns: {err}")
    return dCols

  def makeDfFromArgs(self, *args: Any):
    if len(args) != len(self.modelInputs):
      raise Exception(f"Expected {len(self.modelInputs)} arguments but received {len(args)}.")
    inputNames = [k for k in self.modelInputs.keys()]
    df = pandas.DataFrame(columns = inputNames)
    for i, name in enumerate(inputNames):
      dType = None
      if self.modelInputs[name] != "Any": dType = self.modelInputs[name]
      df[name] = numpy.array([args[i]], dtype=dType) # type: ignore
    return df

  def predict(self, *args: Any) -> float:
    import pycaret.classification # type: ignore
    model = self.loadModelFromTmp()
    df = self.makeDfFromArgs(*args)
    predictDf: pandas.DataFrame = pycaret.classification.predict_model(model, data=df, raw_score=True, verbose=False) # type: ignore
    prediction = cast(numpy.float64, predictDf[['Score_True']].iloc[0][0])
    return float(prediction)

class SklearnPredictor:
  def __init__(self, skpredictor: Any, name: Union[str, None] = None, python_version: Union[str, None] = None):
    self.skpredictor = skpredictor
    self.python_version = python_version
    if name:
      self.name = name
    else:
      self.name = self.guessModelName()

  def guessModelName(self):
    try:
      codeContexts = [f.code_context for f in inspect.stack()]
      for ccList in codeContexts:
        if not ccList: continue
        for cc in ccList:
          captures = re.search(r"\.(deploy|train)\(([^\s,)]+)", cc)
          if captures:
            return captures.group(2)
    except Exception as _:
      _ = 0 # do nothing
    return None

  def makeDeployment(self):
    skpredictor = self.skpredictor
    globals()["skpredictor"] = skpredictor # put the same value to globals so it acts more like a notebook cell

    def predict(*args: Any):
      return float(skpredictor.predict([args])[0])

    return Deployment(
      deploy_function=predict,
      python_version=self.python_version,
      name=self.name
    )

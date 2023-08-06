from typing import Union, Any, cast
import os, io, re
from IPython import display
from html.parser import HTMLParser
import time, markdown
from xml.etree import ElementTree

# From https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = io.StringIO()

    def handle_data(self, data: str):
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()

def _strip_tags(html: str):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def printMk(txt: str):
  txtMode = os.getenv('MB_TXT_MODE')
  if txtMode:
    dispText = _strip_tags(mdToHtml(txt.replace("<br/>", "\n")))
    display.display(display.TextDisplayObject(dispText)) # type: ignore
  else:
    display.display(display.HTML(mdToHtml(txt))) # type: ignore

def printError(txt: str):
  printMk(f'<span style="font-weight: bold; color: #E2548A;">Error:</span> {txt}')

# From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeOfFmt(num: Union[int, Any]):
  if type(num) != int: return ""
  numLeft: float = num
  for unit in ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
    if abs(numLeft) < 1000.0:
      return f"{numLeft:3.0f} {unit}"
    numLeft /= 1000.0
  return f"{numLeft:.1f} YB"

def formatImageTag(imageUrl: Union[str, None], imageAltText: Union[str, None]):
  imageUrl = imageUrl if imageUrl else "https://app.modelbit.com/images/profile-placeholder.png"
  return (
    f'<img src="{ imageUrl }" '
    f'alt="{ imageAltText }" '
    f'referrerPolicy="no-referrer" '
    f'height="32" width="32" ' # for hex.tech, they strip style tags
    f'style="display:inline-block;border-radius:9999px;width:2rem;height:2rem;background-color: rgb(229 231 235);" />'
  )

def pandasTypeToPythonType(pandasType: str):
  if pandasType in ['float32', 'float64']: return 'float'
  if pandasType in ['int32', 'int64']: return 'int'
  if pandasType == 'bool': return 'bool'
  return 'Any'

def simplifyArgName(argName: str):
    scrubbed = re.sub("\\W+", "_", argName.lower())
    scrubbed = re.sub('^(\\d+)', "c\\1", scrubbed)
    if scrubbed.endswith("_"): scrubbed = scrubbed[:-1]    
    return scrubbed

def unindent(source: str) -> str:
  leadingWhitespaces = len(source) - len(source.lstrip())
  if leadingWhitespaces == 0:
      return source
  newLines = [line[leadingWhitespaces:] for line in source.split("\n")]
  return "\n".join(newLines)

def timeago(pastDateMs: int):
    nowMs = time.time() * 1000
    options = [
        { "name": "second", "divide": 1000 },
        { "name": "minute", "divide": 60 },
        { "name": "hour",   "divide": 60 },
        { "name": "day",    "divide": 24 },
        { "name": "month",  "divide": 30.5 },
    ]
    currentDiff = nowMs - pastDateMs
    if currentDiff < 0: raise Exception("The future is NYI")
    resp = "Just now"
    for opt in options:
      currentDiff = round(currentDiff/cast(Union[float, int], opt["divide"]))
      if currentDiff <= 0: return resp
      pluralS = ""
      if currentDiff != 1: pluralS = "s"
      resp = f"{currentDiff} {opt['name']}{pluralS} ago"
    return resp

def mdToHtml(md: str) -> str:
  # the markdown library aligns table headers and cells text with the 'align="..."` attribute. This attribute is
  # overridden by a global jp-RenderedHTMLCommon class. So we need to apply inline styles to these elements so
  # they render correctly
  fontFamily = "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'"
  otherStyle = ""
  if 'HEX_DATA_SERVICE_URL' in os.environ: otherStyle = "margin: 8px;"
  htmlStr = f'<div style="{otherStyle} {fontFamily}">{markdown.markdown(md, extensions=["tables"])}</div>'
  etree = ElementTree.fromstring(htmlStr)
  for el in etree.iter():
    if el.get("align"):
      el.set("style", f'text-align: {el.get("align")};')
  return ElementTree.tostring(etree).decode()

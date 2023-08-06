from typing import List

from .helpers import GenericWarehouse
from .modelbit_core import ModelbitCore
from .utils import timeago, mdToHtml

class Warehouses:  
  def __init__(self, mbMain: ModelbitCore):
    self._mbMain = mbMain
    self._warehouses: List[GenericWarehouse] = []
    resp = self._mbMain.getJsonOrPrintError("jupyter/v1/warehouses/list")
    if resp and resp.warehouses:
      self._warehouses = resp.warehouses
  
  def _repr_html_(self):
    return mdToHtml(self._makeWarehousesMkTable())

  def _makeWarehousesMkTable(self):
    if len(self._warehouses) == 0: return ""
    formatStr = "| Name | Type | Connected | Deploy Status | \n" + \
      "|:-|:-|:-|:-|\n"
    for w in self._warehouses:
      connectedAgo = timeago(w.createdAtMs)
      formatStr += f'| { w.displayName } | { w.type } | { connectedAgo } | { w.deployStatusPretty } | \n'
    return formatStr

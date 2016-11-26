
from model.group import Group
import time
import clr

from TestStack.White.InputDevices import Keyboard
from TestStack.White.WindowsAPI import KeyboardInput
from TestStack.White.UIItems.Finders import *

clr.AddReferenceByName('UIAutomationTypes, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35')
from System.Windows.Automation import *


class GroupHelper(object):

    def __init__(self, app):
        self.app = app
        self.main_window = self.app.main_window

    def open_group_editor(self):
        self.main_window.Get(SearchCriteria.ByAutomationId("groupButton")).Click()
        modal = self.main_window.ModalWindow("Group editor")
        return modal

    def close_group_editor(self, modal):
        modal.Get(SearchCriteria.ByAutomationId("uxCloseAddressButton")).Click()

    def add_new_group(self, group):
        modal = self.open_group_editor()
        modal.Get(SearchCriteria.ByAutomationId("uxNewAddressButton")).Click()
        edit = modal.Get(SearchCriteria.ByControlType(ControlType.Edit))
        edit.BulkText = group.name
        Keyboard.Instance.PressSpecialKey(KeyboardInput.SpecialKeys.RETURN)
        self.close_group_editor(modal)

    def get_group_list(self):
        modal = self.open_group_editor()
        tree = modal.Get(SearchCriteria.ByAutomationId("uxAddressTreeView"))
        root = tree.Nodes[0]
        l = [Group(node.Text) for node in root.Nodes]
        self.close_group_editor(modal)
        return l

    def delete_group_by_index(self, index):
        modal = self.open_group_editor()
        tree = modal.Get(SearchCriteria.ByAutomationId("uxAddressTreeView"))
        root = tree.Nodes[0]
        root.Nodes[index].Select()
        modal.Get(SearchCriteria.ByAutomationId("uxDeleteAddressButton")).Click()
        del_modal = modal.ModalWindow("Delete group")
        del_modal.Get(SearchCriteria.ByAutomationId("uxOKAddressButton")).Click()
        self.close_group_editor(modal)
import clr
import os.path
project_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(os.path.join(project_dir, "..\\TestStack.White.0.13.3\\lib\\net40\\"))
sys.path.append(os.path.join(project_dir, "..\\Castle.Core.3.3.0\\lib\\net40-client\\"))
clr.AddReferenceByName("TestStack.White")

from TestStack.White import Application as WhiteApplication
from TestStack.White.UIItems.Finders import *

from fixture.group import GroupHelper

class Application(object):

    def __init__(self, app_path):
        self.app_path = app_path
        self.application = WhiteApplication.Launch(os.path.join(self.app_path, "AddressBook.exe"))
        self.main_window = self.application.GetWindow("Free Address Book")
        self.group = GroupHelper(self)

    def destroy(self):
        self.main_window.Get(SearchCriteria.ByAutomationId("uxExitAddressButton")).Click()
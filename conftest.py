import pytest
import os.path
import json
from fixture.application import Application
from fixture.group import Group

import clr
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        target_filename = file
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), target_filename) \
            if os.path.basename(target_filename) == target_filename else target_filename
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):
    global fixture
    config = load_config(request.config.getoption("--target"))
    if fixture is None:
        fixture = Application(app_path=config['app_path'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--target", action="store", default="target.json")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith('excel_'):
            testdata = load_from_excel(fixture[6:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_excel(file):
    res = []
    excel = Excel.ApplicationClass()
    excel.Visible = True
    workbook = excel.Workbooks.Open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data\\%s.xslx" % file))
    sheet = workbook.ActiveSheet
    last_row = sheet.Cells.SpecialCells(Excel.XlCellType.xlCellTypeLastCell).Row
    for i in range(last_row):
        name = sheet.Range["A%s" % (i + 1)].Value2
        res.append(Group(name=name if name is not None else ''))
    excel.Quit()
    return res
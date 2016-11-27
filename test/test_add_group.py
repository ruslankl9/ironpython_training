from model.group import Group


def test_add_group(app):
    old_list = app.group.get_group_list()
    new_group = Group(name="test group")
    app.group.add_new_group(new_group)
    new_list = app.group.get_group_list()
    old_list.append(new_group)
    assert sorted(old_list, key=Group.key) == sorted(new_list, key=Group.key)


def test_add_group_excel(app, excel_groups):
    group = excel_groups
    old_list = app.group.get_group_list()
    app.group.add_new_group(group)
    new_list = app.group.get_group_list()
    old_list.append(group)
    assert sorted(old_list, key=Group.key) == sorted(new_list, key=Group.key)
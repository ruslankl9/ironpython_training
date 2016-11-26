from model.group import Group


def test_add_group(app):
    old_list = app.group.get_group_list()
    new_group = Group(name="test group")
    app.group.add_new_group(new_group)
    new_list = app.group.get_group_list()
    old_list.append(new_group)
    assert sorted(old_list) == sorted(new_list)
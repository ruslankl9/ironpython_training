from model.group import Group
import random


def test_delete_some_group(app):
    if len(app.group.get_group_list()) <= 1:
        app.group.add_new_group(Group(name='test'))
    old_list = app.group.get_group_list()
    index = random.randrange(len(old_list))
    app.group.delete_group_by_index(index)
    new_list = app.group.get_group_list()
    assert len(old_list) - 1 == len(new_list)
    del old_list[index]
    assert old_list == new_list
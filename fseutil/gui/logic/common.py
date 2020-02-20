from PySide2 import QtWidgets


def filter_objects_by_name(
        object_parent_widget: QtWidgets.QWidget,
        object_types: list,
        names: list = None):

    list_objects = list()
    for i in object_types:
        for j in object_parent_widget.findChildren(i):
            if names:
                for k in names:
                    if k in j.objectName():
                        list_objects.append(j)
            else:
                list_objects.append(j)

    return list_objects
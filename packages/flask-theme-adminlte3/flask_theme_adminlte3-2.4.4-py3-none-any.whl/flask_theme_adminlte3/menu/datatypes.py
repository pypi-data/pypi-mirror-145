from collections import OrderedDict


class MenuItem(object):
    """Application menu item."""

    TYPE_LINK = "link"
    TYPE_HEADER = "header"
    TYPE_DROPDOWN_DIVIDER = "dropdown divider"
    TYPE_FORM = "form"

    __slots__ = (
        "_active",
        "_children",
        "id",
        "title",
        "url",
        "parent",
        "type",
        "icon",
        "help",
        "badge",
        "_class",
        "form",
    )

    def __init__(
        self,
        id_item,
        title,
        url,
        parent=None,
        item_type=TYPE_LINK,
        icon=False,
        help=None,
        badge=None,
        _class="",
        form=None,
    ):
        """
        Arguments:
            id_item (int|str): the unique identifier of the menu item.
            title (str): item title.
            url (str): the URL that the menu item refers to.
            parent (MenuItem): link to the parent menu item.
            item_type (str): type of menu item, see MenuItem.TYPE_ *.
            icon (str): CSS classes for the icon.
            help (str): hover hint.
            badge (tuple): text label, the first element is text, the second element is style.
        """
        self._active = False
        self._children = []

        self.id = id_item
        self.title = title
        self.url = url
        self.parent = parent
        self.type = item_type
        self.icon = icon
        self.help = help
        self.badge = badge
        self._class = _class
        self.form = form

    def __str__(self):
        return self.title

    def __iter__(self):
        for child in self.children:
            yield child

    def add_badge(self, text, color):
        """Adds a text label to a menu item."""
        self.badge = (text, color)

    def append_child(self, child):
        """Adds a child menu item."""
        child.parent = self
        self._children.append(child)

    @property
    def children(self):
        yield from self._children

    @children.setter
    def children(self, children):
        for child in children:
            self.append_child(child)

    def has_children(self):
        """Returns true if the menu item has a submenu."""
        return bool(self._children)

    def has_parent(self):
        """Returns true if the menu item is a child."""
        return self.parent is not None

    def is_active(self):
        """Returns true if the menu item is selected, otherwise false."""
        return self._active

    def remove_child(self, child):
        # fixme: родитель и исключение
        if child in self.children:
            self._children.remove(child)

    def set_active(self, state):
        """Sets the status of a menu item as active or not."""
        self._active = bool(state)

        if self.has_parent():
            self.parent.set_active(state)


class Menu(object):
    """Application menu."""

    __slots__ = ("_items", "title")

    def __init__(self, title=None):
        self._items = OrderedDict()
        self.title = title

    def __iter__(self):
        for id_item, item in self._items.items():
            if not item.has_parent():
                yield item

    def activate_by_path(self, path):
        """Makes active a menu item whose URL matches the one specified in the argument."""
        for item in self._items.values():
            if item.type == MenuItem.TYPE_LINK and item.url == path:
                item.set_active(True)
                return True
        return False

    def activate_by_function(self, is_active, all=False):
        """Makes active a menu item if the activate function returns True"""
        activated = False
        for item in self._items.values():
            if is_active(item):
                item.set_active(True)
                activated = True
                if not all:
                    return activated
        return activated

    def add_item(self, item: MenuItem):
        """Adds a new menu item."""
        if item.has_parent():
            item.parent.append_child(item)
        self._items[item.id] = item

    def get_item(self, id_item):
        """Returns a menu item with the specified unique identifier."""
        return self._items.get(id_item)

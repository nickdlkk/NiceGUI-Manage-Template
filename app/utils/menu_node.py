class MenuNode:
    def __init__(self, label, path, icon=None, caption=None, children=None, parent_path=None, title=None):
        self.label = label  # 侧边栏大标题
        self.path = path  # 路由
        self.icon = icon  # 图标
        self.title = title if title is not None else label  # 顶部标题, 默认等于label
        self.caption = caption  # 侧边栏小标题
        self.children = children if children is not None else []
        self.parent_path = parent_path  # 父节点路由

    @classmethod
    def create_root_node(cls, icon, label, caption=None):
        # 根节点没有 parent_path
        return cls(icon=icon, label=label, caption=caption, parent_path=None)

    @staticmethod
    def build_menu(menus):
        # 将根节点添加到结果列表中，根节点的 parent_path 应为 None
        roots = [menu for menu in menus if menu.parent_path is None]
        all_menus = {menu.label: menu for menu in menus}  # 所有菜单项的字典

        # 构建树结构
        for menu in menus:
            if menu.parent_path:  # 有 parent_path，说明不是根节点
                parent_label = menu.parent_path
                if parent_label in all_menus:
                    parent = all_menus[parent_label]
                    parent.children.append(menu)
                    # 构建当前节点的 path
                    menu.path = parent.path + [menu.label]
                else:
                    raise ValueError(f"Parent with label '{parent_label}' not found for menu '{menu.label}'.")
        return roots  # 返回根节点列表

    def to_dict(self):
        # 将节点转换为字典格式
        return {
            "path": self.path,
            "title": self.title,
            "icon": self.icon,
            "label": self.label,
            "caption": self.caption,
            "children": [child.to_dict() for child in self.children] if self.children else []
        }

    @staticmethod
    def menus_to_dict(menus):
        return [menu.to_dict() for menu in menus]


if __name__ == '__main__':
    # 示例用法
    try:
        # 创建根节点和子节点
        account_settings = MenuNode.create_root_node('perm_identity', 'Account settings')
        inbox = MenuNode('icon', 'Inbox', parent_path='Account settings')
        outbox = MenuNode('icon', 'Outbox', parent_path='Account settings')
        wifi_settings = MenuNode.create_root_node('signal_wifi_off', 'Wifi settings')

        # 将节点放入列表中
        menus = [account_settings, inbox, outbox, wifi_settings]

        # 构建菜单
        root_menus = MenuNode.build_menu(menus)

        # 打印结果
        for menu in root_menus:
            print(f"Menu: {menu.label}, Path: {menu.path}")

        # 将根节点转换为字典格式
        root_menu_dicts = [menu.to_dict() for menu in root_menus]

        # 打印结果
        for root_menu_dict in root_menu_dicts:
            print(root_menu_dict)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

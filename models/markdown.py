import os


class Markdown:

    FILE_BASE_PATH = "view/docs/public"

    @classmethod
    def create_md(cls, content, name):
        """
        根据 json_data 创建 md 文件，json_data 应包含 title 和 content 字段。
        文件保存在 FILE_BASE_PATH 下，文件名为 name.md。
        """
        try:
            file_path = os.path.join(cls.FILE_BASE_PATH, f"{name}.md")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"创建 md 文件失败: {e}")
            return False

    @classmethod
    def read_md(cls, name):
        """
        读取 FILE_BASE_PATH 下 name.md 文件内容。
        """
        try:
            file_path = os.path.join(cls.FILE_BASE_PATH, f"{name}.md")
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"读取 md 文件失败: {e}")
            return None


    @classmethod
    def delete_md(cls, name):
        """
        删除 FILE_BASE_PATH 下 name.md 文件。
        """
        try:
            file_path = os.path.join(cls.FILE_BASE_PATH, f"{name}.md")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                print(f"文件不存在: {file_path}")
                return False
        except Exception as e:
            print(f"删除 md 文件失败: {e}")
            return False

    @classmethod
    def read_all_md(cls):
        """
        读取 FILE_BASE_PATH 目录下所有 .md 文件内容，返回 {文件名: 内容} 字典。
        """
        result = {}
        try:
            if not os.path.exists(cls.FILE_BASE_PATH):
                return result
            for fname in os.listdir(cls.FILE_BASE_PATH):
                if fname.endswith(".md"):
                    file_path = os.path.join(cls.FILE_BASE_PATH, fname)
                    name = fname.replace(".md", "")
                    with open(file_path, "r", encoding="utf-8") as f:
                        result[name] = f.read()
            return result
        except Exception as e:
            print(f"读取所有 md 文件失败: {e}")
            return result

    @classmethod
    def get_all_md_name(cls):
        """
        读取 FILE_BASE_PATH 目录下所有 .md 文件名。
        """
        result_list = []
        try:
            if not os.path.exists(cls.FILE_BASE_PATH):
                return result_list
            for fname in os.listdir(cls.FILE_BASE_PATH):
                if fname.endswith(".md"):
                    name = fname.replace(".md", "")
                    result_list.append(name)
            return result_list
        except Exception as e:
            print(f"读取所有 md 文件名: {e}")
            return result_list


class PrivateMarkdown(Markdown):

    FILE_BASE_PATH = "view/docs/public/private"


if __name__ == "__main__":
    # 示例用法
    Markdown.create_md("# fff\n这是内容。", "test")
    print(Markdown.read_md("test"))
    print(Markdown.read_all_md())

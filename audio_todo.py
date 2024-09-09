import os
import unittest
import tempfile
import shutil


def listTodo(directory, extensions):
    todo = []
    done = []
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lstrip('.') in extensions:
            if os.path.exists(os.path.join(directory, name + '.txt')):
                done.append(filename)
            else:
                todo.append(filename)
    return list(sorted(todo))


class TestListTodo(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def populate_files(self, files):
        for file in files:
            with open(os.path.join(self.temp_dir, file), 'w') as f:
                f.write("")

    def test_two_ogg_files(self):
        self.populate_files(["file1.ogg", "file2.ogg"])
        result = listTodo(self.temp_dir, ['ogg'])
        self.assertEqual(result, ["file1.ogg", "file2.ogg"])

    def test_m4a_ogg_txt_files(self):
        self.populate_files(["file1.m4a", "file2.m4a", "file3.ogg", "file1.txt"])
        result = listTodo(self.temp_dir, ['m4a', 'ogg'])
        self.assertEqual(result, ["file2.m4a", "file3.ogg"])

    def test_empty_directory(self):
        result = listTodo(self.temp_dir, ['ogg', 'm4a'])
        self.assertEqual(result, [])

    def test_non_matching_extensions(self):
        self.populate_files(["file1.mp3", "file2.wav"])
        result = listTodo(self.temp_dir, ['ogg', 'm4a'])
        self.assertEqual(result, [])

    def test_txt_files_only(self):
        self.populate_files(["file1.txt", "file2.txt"])
        result = listTodo(self.temp_dir, ['ogg', 'm4a'])
        self.assertEqual(result, [])

    def test_mixed_extensions_with_txt(self):
        self.populate_files(["file1.ogg", "file2.m4a", "file3.wav", "file2.txt"])
        result = listTodo(self.temp_dir, ['ogg', 'm4a'])
        self.assertEqual(result, ["file1.ogg"])


if __name__ == "__main__":
    unittest.main()

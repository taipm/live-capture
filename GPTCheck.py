import ast
import collections
import os


# Định nghĩa visitor để duyệt AST
class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = collections.defaultdict(int)

    def visit_Call(self, node):
        # Nếu node đang tham chiếu đến một hàm
        if isinstance(node.func, ast.Name):
            # Tăng số lần xuất hiện của hàm này lên 1
            self.functions[node.func.id] += 1

# Đường dẫn đến tệp mã nguồn cần kiểm tra
#file_path = "/Users/taipm/Documents/GitHub/live-capture/Stock.py"

# Thư mục dự án Python
project_directory = '/Users/taipm/Documents/GitHub/live-capture/'

# Lấy danh sách các file trong thư mục dự án
files = os.listdir(project_directory)

# In danh sách các file
for file in files:
    print(file)
    try:
        # Phân tích cú pháp tệp mã nguồn và duyệt AST
        with open(file, "rb") as source_file:
            source = source_file.read()
            tree = ast.parse(source)
            visitor = FunctionVisitor()
            visitor.visit(tree)

        # In ra số lần xuất hiện của mỗi hàm
        for function_name, count in visitor.functions.items():
            print("\t - {}: {}".format(function_name, count))
    except:
        print(f'{file} - Lỗi')

import os
import ast

def get_function_usage(project_path):
    # Lấy danh sách các file trong thư mục dự án
    file_list = []
    for dirpath, dirnames, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith('.py'):
                file_list.append(os.path.join(dirpath, filename))

    # Đếm số lần xuất hiện của các hàm
    function_count = {}
    for file_path in file_list:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                tree = ast.parse(file.read())
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_name = node.name
                    if function_name in function_count:
                        function_count[function_name] += 1
                    else:
                        function_count[function_name] = 1

    # Sắp xếp các hàm theo số lần xuất hiện giảm dần
    sorted_functions = sorted(function_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_functions

import pandas as pd
data = get_function_usage(project_path=project_directory)
df = pd.DataFrame(data, columns=['FunctionName', 'N-Call'])

print(df)


import ast
import os
import pandas as pd

def analyze_python_project(folder_path):
    """Phân tích mã nguồn của dự án Python từ thư mục chỉ định.

    Args:
        folder_path (str): Đường dẫn đến thư mục chứa dự án Python.

    Returns:
        pandas.DataFrame: Kết quả phân tích mã nguồn, bao gồm tên hàm và số lần sử dụng.
    """
    function_calls = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        tree = ast.parse(f.read())
                    except:
                        print(f"Không thể phân tích mã nguồn từ tệp tin {file_path}")
                        continue
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Name):
                                function_name = node.func.id
                                if function_name in function_calls:
                                    function_calls[function_name] += 1
                                else:
                                    function_calls[function_name] = 1
    df = pd.DataFrame.from_dict(function_calls, orient="index", columns=["Số lần sử dụng"])
    df.index.name = "Tên hàm"
    df = df.sort_values(by="Số lần sử dụng", ascending=False)
    return df

df = analyze_python_project(folder_path=project_directory)

print(df)
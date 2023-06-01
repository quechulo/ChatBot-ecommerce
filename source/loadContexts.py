import os

dir_path = "context_files"
def load_file(filename):
    path = os.path.join(dir_path, filename)
    with open(path, 'r', encoding="utf-8") as file:
        data = file.read()
    return data


def load_all_files(input_filename):
    path = os.path.join(dir_path, input_filename)
    try:
        with open(path, "w", encoding="utf-8") as all_context:
            # Use the truncate() method to erase the contents
            all_context.truncate()
    except:
        print("An error occurred while clearing All Context file.")

    filenames = ['about.txt', 'complaint.txt', 'shoes.txt', 'clothes.txt']
    try:
        with open(path, 'a', encoding="utf-8") as all_context:
            for file in filenames:
                all_context.write(load_file(file))
            all_context.write('\n')
        print("All Context file created successfully.")
    except:
        print("An error occurred while creating All Context file.")

    all_context = load_file(input_filename)
    return all_context


if __name__ == '__main__':
    r = load_all_files('all_context.txt')
    print(r)
    # path = os.path.join("context_files", "all_context.txt")
    # print(path)
    # print(os.path.exists(path))



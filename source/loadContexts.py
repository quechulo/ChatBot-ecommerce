def load_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        data = file.read().replace('\n', ' ')
    return data


def load_all_files(input_files):
    filenames = ['about.txt', 'complaint.txt', 'shoes.txt', 'clothes.txt']
    result_filename = 'all_context.txt'
    try:
        with open(result_filename, "w") as all_context:
            # Use the truncate() method to erase the contents
            all_context.truncate()
        with open(result_filename, 'a') as all_context:
            for file in input_files:
                all_context.write(load_file(file))
            all_context.write('\n')
        print("All Context file created successfully.")

        all_context = load_file(result_filename)
        return all_context

    except:
        print("An error occurred while creating All Context file.")

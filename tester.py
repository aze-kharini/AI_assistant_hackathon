def data_format(data):
    answer = "Here are the results for your question:\n"
    col_lens = longest_words_per_col(data)
    for row in data:
        line = ""
        for index, info in enumerate(row):
            formatted_string = "{:<" + str(col_lens[index]) +"} | "
            line += formatted_string.format(str(info))
        answer += str(line)[:-3] + "\n"
    return "\tBot:\n" + answer

def longest_words_per_col(data):
    max_lengths_per_col = []
    num_cols = len(data[0])

    for col_index in range(num_cols):
        column_data = []
        for row in data:
            column_data.append(row[col_index])
        longest_word = max(column_data, key=len)
        max_lengths_per_col.append(len(longest_word))

    return max_lengths_per_col



data = [('Gesha','s'), ('Typica','s'), ('Bourbon','s'), ('Caturra','s'), ('Maragogipe','s'), ('Mundo Nuovo','s'), ('SL-28','s')]

print(data_format(data))

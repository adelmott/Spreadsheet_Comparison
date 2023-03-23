import pandas as pd


def compare_files(file1, file2, columns):
    
    # Read the spreadsheet into a dataframe
    if ".xlsx" in file1:
        df1 = pd.read_excel(file1)
    elif ".csv" in file1:
        df1 = pd.read_csv(file1)
    if ".xlsx" in file2:
        df2 = pd.read_excel(file2)
    elif ".csv" in file2:
        df2 = pd.read_csv(file2)

    # Extract specified columns from both dataframes
    df1 = df1[columns]
    df2 = df2[columns]

    # Get the difference between the two dataframes
    df1_merged = df1.merge(df2, indicator=True, how="outer")
    diff = df1_merged[df1_merged["_merge"] == "left_only"]
    diff = diff.drop(["_merge"], axis=1)

    df2_merged = df2.merge(df1, indicator=True, how="outer")
    diff2 = df2_merged[df2_merged["_merge"] == "left_only"]
    diff2 = diff2.drop(["_merge"], axis=1)

    return diff, diff2


if __name__ == "__main__":
    print('Files must be in the same directory as the program, or else include the file path as part of the file name.')
    file1 = input("Enter the name and extension of the first file: ")
    file2 = input("Enter the name and extension of the second file: ")
    columns = []
    while True:
        column_name = input(
            'What is the name of the column you want to compare? (type "done" if done): '
        )
        if column_name.lower() != "done":
            columns.append(column_name)
        else:
            break

    writer = pd.ExcelWriter("diff.xlsx")
    diff, diff2 = compare_files(file1, file2, columns)
    diff2.to_excel(writer, index=False, sheet_name="Missing_F1")
    diff.to_excel(writer, index=False, sheet_name="Missing_F2")
    writer.save()
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

filename = "Base general whatsApp.xlsx"
filename1 = "Confirmacion de WhatsApp UIO.xlsx"
sheetname = "Base Socio CN "
sheetname1 = "Sheet1"
filter_by = ["guayaquil"]
filter_by_not_in = ["quito", "guayaquil"]
conventional = False
max_cellphone = 1

df = pd.read_excel(filename, sheet_name=sheetname, na_values="")
df_send = pd.read_excel(filename1, sheet_name=sheetname1, na_values="", skiprows=6)

print("Column headings:")
print(df.columns)
print("Column headings:")
print(df_send.columns)


def split(x):
    return str(x).split("-")


def filter(x):
    dat = str(x).strip().lower()
    if dat in filter_by:
        return True
    return False


def exclude(x):
    dat = str(x).strip().lower()
    if dat not in filter_by_not_in:
        return True

    return False


def is_not_conventional(x):
    for number in x:
        if "09" in number:
            return False
    return True


def has_more_numbers(x):
    telephones = []
    for number in x:
        if "09" == number[:2] or "+5939" in number[:5]:
            if len(telephones) < max_cellphone:
                telephones.append(number)
    return telephones
    # if len(telephones) != 0:
    #     return telephones[0]
    # else:
    #     return ""


def has_more_numbers(x):
    telephones = []
    for number in x:
        if "09" == number[:2] or "+5939" in number[:5]:
            if len(telephones) < max_cellphone:
                telephones.append(number)
    return telephones
    # if len(telephones) != 0:
    #     return telephones[0]
    # else:
    #     return ""


def not_empty(x):
    if len(x) != 0:
        return True
    return False


df_send['Telefono '] = df_send['Telefono '].map(lambda x: str(x).strip())
df_send['Telefono '] = df_send['Telefono '].map(lambda x: "0" + x if x[0] == "9" else x)

sent_numbers = df_send['Telefono '].to_list()


def check_sent(x, sent=sent_numbers):
    if len(x) == 0:
        return False
    for value in x:
        if value in sent:
            return True
    return False


def check_not_sent(x):
    return not check_sent(x, sent_numbers)


df['Telefono '] = df['Telefono '].map(split)
df['Telefono '] = df['Telefono '].map(has_more_numbers)

df3 = df['Ciudad '].map(filter)
df4 = df['Telefono '].map(not_empty)
df5 = df['Telefono '].map(check_not_sent)

df7 = df3 & df4 & df5
df = df[df7]

df['Telefono '] = df['Telefono '].map(lambda x: x[0])

print(df.shape)

# df['Telefono '] = df['Telefono '].append(df_send['Telefono '], ignore_index=True)
# df5 = df['Telefono '].map(check_sent)

# df6 = df3 & df4 & df5
print(df.shape)

# df2 = df.drop_duplicates(["Telefono "], keep=False)

# print(df2.shape)
print(df[df3].shape)
print(df[df7].shape)
# print(df[df6].head())

# filename_output = "".join([filename.split(".")[0], "output", ".xlsx"])
# writer = pd.ExcelWriter("output.xlsx")
df.to_excel("output_2.xlsx")
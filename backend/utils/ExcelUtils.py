# Tools for exporting data into excel table
import datetime
import os
import pandas as pd

OUTPUT_DIR = os.getcwd()


def get_col_widths(dataframe):
    # First we find the maximum length of the index column   
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

def createExcelFileFromData(data, sheet_name):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("OrderPad {0}.xlsx".format(datetime.datetime.now().strftime("%I%M%p on %B %d %Y")), engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object. Turn off the default
    # header and index and skip one row to allow us to insert a user defined
    # header.
    data.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    worksheet = writer.sheets[sheet_name]
    workbook = writer.book

    # Light red fill with dark red text.
    light_red = workbook.add_format({'bg_color':   '#FFC7CE',
                                'font_color': '#9C0006'})

    # Light yellow fill with dark yellow text.
    light_yellow = workbook.add_format({'bg_color':   '#FFEB9C',
                                'font_color': '#9C6500'})

    # Green fill with dark green text.
    light_green = workbook.add_format({'bg_color':   '#C6EFCE',
                                'font_color': '#006100'})

    # Get the dimensions of the dataframe.
    (max_row, max_col) = data.shape

    # Create a list of column headers, to use in add_table().
    column_settings = []
    for header in data.columns:
        column_settings.append({'header': header})

    # Add the table.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)
    worksheet.set_column(2, 2, 5)
    worksheet.set_column(3, 3, 5)

    worksheet.conditional_format( 1, 1, max_row, 2,
        {'type':     'formula',
        'criteria': '=$B2="Buy"',
        'format':   light_yellow}
    )

    worksheet.conditional_format( 1, 9, max_row, 9,
        {'type':     'formula',
        'criteria': '=$B2="Buy"',
        'format':   light_yellow}
    )

    worksheet.conditional_format( 1, 1, max_row, 2,
        {'type':     'formula',
        'criteria': '=$B2="Sell"',
        'format':   light_green}
    )

    worksheet.conditional_format( 1, 9, max_row, 9,
        {'type':     'formula',
        'criteria': '=$B2="Sell"',
        'format':   light_green}
    )

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    # data.to_excel("OrderPad {0}.xlsx".format(datetime.datetime.now().strftime("%I%M%p on %B %d %Y")), sheet_name=sheet_name, index=False)
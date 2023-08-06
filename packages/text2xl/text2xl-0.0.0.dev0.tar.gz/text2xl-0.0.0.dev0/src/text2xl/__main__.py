
import os
import xlsxwriter

def main():
    path = input("Enter Path Name: ") + '/'
    prefix = input("Enter Prefix (you may leave blank)")
    suffix = '.txt'

    start_row = "Data Points"
    include_start = False
    stop_row = "ample"
    include_stop = False
    section_header = ''
    include_section_header = True

    files = os.listdir(path)
    files = [file[3:-4] for file in files if file[-4:].lower() == suffix]

    workbook = xlsxwriter.Workbook('spectroscopy data.xlsx')
    worksheet = workbook.add_worksheet()

    col = 0
    row = 0
    for name in files:
        section_header = name
        with open(path + prefix + name + suffix) as file:
            lines = file.readlines()
            file_length = len(lines)
            data_vals = False
            width = 0
            for num in range(file_length):
                line = lines[num]
                if stop_row in line:
                    data_vals = False
                    col += width
                if data_vals:
                    line = line.split()
                    if line:
                        for i in range(len(line)):
                            worksheet.write(row, col + i, line[i])
                        row += 1
                        width = len(line)
                if num == file_length - 1:
                    data_vals = False
                    col += width
                if start_row in line:
                    data_vals = True
                    row = 0
                    worksheet.write(row, col, section_header)
                    row += 1

    workbook.close()

if __name__ == '__main__':
    main()

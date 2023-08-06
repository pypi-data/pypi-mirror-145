
def csv_printer(filepath):
    import csv
    import sys
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                print(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, reader.line_num, e))
            
def csv_reader(filepath):
    import csv
    import sys
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                yield row
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, reader.line_num, e))
            
def csv_reader_dict(filepath):
    import csv
    import sys
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                yield row
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, reader.line_num, e))
            
def csv_writer(filepath, data):
    import csv
    import sys
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        try:
            writer.writerows(data)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, writer.line_num, e))
            
def csv_writer_append(filepath, data):
    import csv
    import sys
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        try:
            writer.writerows(data)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, writer.line_num, e))
            
def csv_writer_append_dict(filepath, data):
    import csv
    import sys
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, data[0].keys())
        try:
            writer.writerows(data)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, writer.line_num, e))
            
def csv_writer_append_dict_header(filepath, data):
    import csv
    import sys
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, data[0].keys())
        try:
            writer.writeheader()
            writer.writerows(data)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, writer.line_num, e))
            
def csv_writer_append_dict_header_if_not_exist(filepath, data):
    import csv
    import sys
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, data[0].keys())
        try:
            if not writer.has_header():
                writer.writeheader()
            writer.writerows(data)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filepath, writer.line_num, e))


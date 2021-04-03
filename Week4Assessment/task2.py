import sys
import csv

# csv file names
BOOKLOANSFILE = 'bookloans.csv'
BOOKSFILE = 'books.csv'
REPORTFILETASK2 = 'Task_2_report.csv'


def open_file(file_in, skip_header=False):
    """Open a file and returns the data.

        Wraps a basic file open in a function to allow this
        to be reused.  When I was examining the books and
        bookloans files I noticed that when reading the
        files, I always ended up with a very random
        "\ufeff1" appearing right at the begning of the data
        from the file.  Further examination with VS Code
        showed that the encoding of the file was "utf-8 with
        BOM" and that this random sequence was a symptom.
        To corrrect this, the file had to be opened with
        "utf-8-sig" encoding.  I did consider if the
        encoding should also be made a parameter, but
        ultimately for these tasks kept this hard coded
        as both files share the same encoding.

        I also try to catch errors using a try/except
        block, I have one specific error "FileNotFoundError"
        and a generic catch all.  Error messages for both
        these occasions make use of string formatting to pass
        the fileIn parameter, which futher enhances re-usability.
        I fruther call sys.exit(1) which stops the execution
        and allows the OS to know there was a problem.

        I have checked the FileNotFound exception by passing
        in the name of a non-existing file.

        Keyword arguments:
            fileIn -- the file object whi chwill be opened
            skipHeader -- some files have "Headers" in the
            first row, if this is true we ignore these
            (defaults to False) Ultimatley, I never used
            this parameter

        Returns:
            data -- a list of tuples
    """
    # setup a variable to hold the data from the file
    data = ''
    try:
        with open(file_in, encoding='utf-8-sig', mode='r') as file:
            reader = csv.reader(file)
            if skip_header is True:
                # if skip_header is true, then skip to the next line
                next(reader, None)
            # make each row in the input file into a tuple and add
            # this to a list to be returned.
            data = [tuple(row) for row in reader]
    # handle file not found errors with a nice error message
    except FileNotFoundError:
        print('File {} does not exist.'.format(file_in))
        sys.exit(1)
    except:  # generic catch all error message
        print(
            'Trying to open {} failed.  No further information was available'
            .format(file_in))
        sys.exit(1)
    # return the data variable (the file contents)
    return data


def create_report(file_name, headers, content):
    """Creates a report file (currently a CSV)

    Keyword arguments:
        file_name -- the file we wish to create
        headers -- a list containing the header columns for the report
        content -- a list with the data to be populated in the file.
    """
    try:
        with open(file_name, 'w', newline="") as out_file:
            csvwriter = csv.writer(out_file)
            csvwriter.writerow(headers)
            csvwriter.writerows(content)
    except:
        print(
            'Trying to create {} failed.  No further information was available'
            .format(file_name)
        )
        sys.exit(1)


def build_task2_details(loans):
    """Generate the content for the report.

    Keyword arguments:
    loans -- the list of data on the loans
    """
    report_dict = {}
    genre_dict = {}
    sub_genre_dict = {}
    genreCount = 0
    sub_genre_count = 0
    for row in loans:
        # get the booknumber from the bookloans list
        book_number = row[0]
        book_number = int(book_number)
        genre = ""  # books[book_number][3]
        sub_genre = ""  # books[book_number][4]

        for book in books:
            book_ref = book[0]
            # bit sucky, to keep code working I had to bring in the headers.
            if book_ref != 'Number':
                book_ref = int(book_ref)
                if book_ref == book_number:
                    book_found = True
                    genre = books[book_number][3]
                    sub_genre = books[book_number][4]
                    break
        if book_found:
            # here we cycle through the loans and update counters
            # in 2 dictionaries depending on the genre and subgenre
            if genre not in genre_dict:
                if genre != "":
                    genre_dict[genre] = {}
                    genreCount = 0
                    genre_dict[genre] = 1
            else:
                genreCount = genre_dict[genre]
                genreCount = int(genreCount)  # not needed as we control this
                genreCount += 1
                genre_dict[genre] = genreCount

            if sub_genre not in sub_genre_dict:
                if sub_genre != "":
                    sub_genre_dict[sub_genre] = {}
                    sub_genre_count = 0
                    sub_genre_dict[sub_genre] = 1
            else:
                sub_genre_count = sub_genre_dict[sub_genre]
                sub_genre_count = int(sub_genre_count)
                sub_genre_count += 1
                sub_genre_dict[sub_genre] = sub_genre_count

        report_dict = tuple([genre_dict, sub_genre_dict])

    return report_dict


def sort_and_generate_task2_content(data_in, task_num):
    """For task 2 this converts the dictionary to a list and sorts at
    the same time.

    Keyword arguments:
        dataIn --  the dictionary which was built up in the
        buildTask2Details function.
        sorts on the field timesOutIn2019 and then converts this to a list for use with the CSV writer import.
    """
    report_out = []
    if task_num == "Genre":
        print("{:<20} {:<10}".format('Genre', 'Count'))
        for k, v in sorted(data_in.items(), key=lambda e: e[1], reverse=True):
            item = [k, v]
            report_out.append(item)
            print("{:<20} {:<10}".format(k, v))
        return report_out
    elif task_num == "SubGenre":
        print("{:<20} {:<10}".format('Sub-Genre', 'Count'))
        for k, v in sorted(data_in.items(), key=lambda e: e[1], reverse=True):
            item = [k, v]
            report_out.append(item)
            print("{:<20} {:<10}".format(k, v))
        return report_out
    else:
        print("incorrect task number.  please try again")
        sys.exit(1)


books = open_file(BOOKSFILE)
loans = open_file(BOOKLOANSFILE)
temp = build_task2_details(loans)

# temp is a tulpe of two lists, we can split them int
(genre_list, sub_genre_list) = temp

genre_report_headers = ['Genre', 'Count']
sub_genre_report_headers = ['Sub-Genre', 'Count']

list_genre = sort_and_generate_task2_content(genre_list, "Genre")
list_sub_genre = sort_and_generate_task2_content(sub_genre_list, "SubGenre")

create_report(REPORTFILETASK2, genre_report_headers, list_genre)
create_report(REPORTFILETASK2, sub_genre_report_headers, list_sub_genre)

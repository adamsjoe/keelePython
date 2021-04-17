def do_loan():
    member = input("enter member card number : ")
    real_member = validate_member(member, members)

    book_to_take = input("enter book number : ")
    real_book = validate_book(book_to_take, books)

    # print book stats
    real_book.printDetails()

    real_book.assign_to_user(real_member.scan())

    real_book.printDetails()

    # works but uses global stuff
    data = {}
    data["Book_id"] = real_book.scan()
    data["Member_id"] = real_member.scan()
    data["Date_loaned"] = str(get_current_days_excel_epoch())
    data["Date_returned"] = "0"
    jdata.append(data)

    # then save this
    replace_json_file(CURRENT_BOOKLOANSFILE_JSON, jdata)

    # once this is done we should reload the json - this way we have the right
    # data available


def do_apply():
    new_f_name = input("Please enter first name    : ")
    new_l_name = input("Please enter last name     : ")
    new_gender = input("Please enter gender        : ")
    new_email = input("Please enter email address : ")

    # we need to check that this person does not exist

    # then we need to add him to the users list

    members.append(LibraryMember(
                            None,
                            new_f_name,
                            new_l_name,
                            new_gender,
                            new_email,
                            "0"
                            ))

    for row in members:
        print(row.printDetails())

    # not right yet
    # replace_json_file(MEMBERSFILE_JSON, members)


do_loan()
print(currently_loaned_books)


# do_apply()

# for row in members:
#     row.printDetails()
#     print("")


def do_return(book):
    pass


def do_reserve_book(book, member):
    # will need to check the book is not available before proceeding
    pass


def do_startup_check():
    # if the json files are present then no need to regenerate them
    # just load the data
    pass
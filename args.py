import sys

try:
    azstorage_user = sys.argv[1]
    azstorage_password = sys.argv[2]
    azstorage_dir = sys.argv[3]
except IndexError:
    print "{} needs three arguments!".format(sys.argv[0])
    sys.exit(1)

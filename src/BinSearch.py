# ASSUMPTION:  input data is already sorted in ascending order

# CASE 1: empty list, input 1
# - return exception, invalid input data file
# CASE 2: one element 3; input matches 3
# - return 0
# CASE 3: one element 4; input 5
# - return -1 for not found
# CASE 4: three elements; 1 3 4; input 2
# - return -1 for not
# CASE 5: three elements; 1 2 4; input 4
# - return 2

# ATTENTION:  use INDEXES, NOT length on params

# NOTE:  RUN ON CMD LINE as 'python MyProgram.py NumToFind ../data/InputFilename'
# using the sys import to retrieve cmd-line args!
import sys

def loadInputDataFile(inputfile):

    inputInts = []

    try:
        # efficient, streaming API
        with open(inputfile) as f:
            for line in f:
                # ATTENTION:  striping lead-ending whitespace!
                linestr = line.strip()
                if linestr:
                   inputInts.append(int(linestr))
    except IOError:
        print "The file does not exist, exiting gracefully"

    return inputInts

# ATTENTION:  do NOT expose as public API, with recursive storage and index parameters!
#             returns -1 if not found!
def binSearch(numToFind, dataList):
    # foundLocation, recursionLevel = _linearSearch(numToFind, dataList, 0, (len(dataList) - 1), 0)
    foundLocation, recursionLevel = _recurseBinarySearch(numToFind, dataList, 0, (len(dataList) - 1), 0)
    return foundLocation

# ATTENTION:  use origDataList, and INDEX into START, END
#             MID is a calculated variable and therefore NOT a method parameter!
def linearSearch(numToFind, dataList):

    print "ENTERING linearSearch"

    # initialize to not found value
    foundIdx = -1

    # ERROR:  when input list is of size 0
    if (len(dataList) == 0):
        # throwing exception in Python
        # http://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
        raise ValueError('Illegal Argument Exception.  DataList must not be empty.')

    # CAREFUL:  - SINGLE while exit condition
    #           - END increment
    #           - BREAK when FOUND, BEFORE incrementing too far
    scanIdx = 0
    while (scanIdx <= (len(dataList) - 1)):

        # ATTENTION: increment index IFF NO MATCH;
        #            otherwise if found element at END, then may do unecessary increment!
        # if (dataList[scanIdx] != numToFind):
        #    print "{0} != {1}\n".format(dataList[scanIdx], numToFind)
        # CAREFUL ---- TYPING BUG WHOA!!!:  need to CONVERT String @ INPUT to integer, otherwise downstream comparisons against integers will FAIL due to type mismatch!
        # DEEP comparison in Python is ==; but in Java is SHALLOW comparison!!
        # http://stackoverflow.com/questions/11060506/is-there-a-not-equal-operator-in-python
        # http://stackoverflow.com/questions/1634352/what-is-the-difference-between-is-and-in-python
        if (dataList[scanIdx] == numToFind):
            foundIdx = scanIdx
            break

        scanIdx += 1

    # ATTENTION:  EXIT CASES given by DEFAULT without break!
    # (scanIdx > endIdx);  if falling off array, numToFind is LARGER THAN ALL elements of this segment, so match NOT found
    # if not equal values;  numToFind is LESS THAN ALL, OR BETWEEN elements in segment, so match NOT FOUND

    return foundIdx

 # ATTENTION! Use Indexes NOT length to index into ORIGINAL dataList!
def _recurseBinarySearch(numToFind, dataList, startIdx, endIdx, recursionLevel):

    # DEBUG
    print "ENTERING recurseBinarySearch with startIdx, endIdx, recursionLevel:  {0}, {1}, {2}".format(startIdx, endIdx, recursionLevel)

    # initialize to not found value
    foundIdx = -1

    # ERROR:  when input list is of size 0 or negative
    if (endIdx < startIdx):
        # throwing exception in Python
        # http://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
        raise ValueError('Illegal Argument Exception, EndIndex less than StartIndex for range to search in dataList.')

    # ATTENTION! calculate MID value to compare against RELATIVE to startIdx;
    # thereby SKIPPING comparisons in HALF!
    midIdx = startIdx + (endIdx - startIdx)/2

    # DEBUG
    print("MID index:  {0}".format(midIdx))
    print "PIVOT value to compare against:  {0}".format(dataList[midIdx])

    # EXIT recursion if EQUAL!
    if (numToFind == dataList[midIdx]):
        # DEBUG
        # ATTENTION:  HERE is the DEEPEST level, so OUTPUT the recursionLevel for that!
        print '===== FOUND MATCH at recursionLevel:  '
        print ':  '.join(str(recursionLevel))
        return (midIdx, recursionLevel)
    # ATTENTION:  check for index bounds prior to increment!
    elif ((numToFind > dataList[midIdx]) and ((midIdx + 1) < len(dataList))):
        recursionLevel += 1
        foundIdx, recursionLevel = _recurseBinarySearch(numToFind, dataList, (midIdx + 1), endIdx, recursionLevel)
    # ATTENTION:  check for index bounds prior to decrement!
    elif ((numToFind < dataList[midIdx]) and (midIdx >= 1)):
        recursionLevel += 1
        foundIdx, recursionLevel =_recurseBinarySearch(numToFind, dataList, startIdx, (midIdx - 1), recursionLevel)

    return foundIdx, recursionLevel


"""
   TEST CASES:

    4 ../data/three FOUND 2
    2 ../data/three FOUND 1
    0 ../data/three NOT FOUND -1
    6 ../data/three NOT FOUND -1

"""
def main(args):

    print("\n\nWELCOME!  Finding line position of number:  {0} within file with name:  {1}\n".format(args[1], args[2]))

    # if no filename supplied, enter it here
    if (len(args) < 3):
        # ATTENTION, PYTHON EXCEPTIONS:  https://docs.python.org/2/tutorial/errors.html
        raise ValueError('Required arguments are:  an integer value, and then the file path/name of text file containing unsorted integers on separate lines.')
    else:
        inputfile = args[2]

    print '***** Input Num TO FIND *****'
    numToFind = args[1]
    print numToFind
    # CAREFUL ---- TYPING BUG WHOA!!!:  need to CONVERT String @ INPUT to integer, otherwise downstream comparisons against integers will FAIL due to type mismatch!
    # DEEP comparison in Python is ==; but in Java is SHALLOW comparison!!
    # http://stackoverflow.com/questions/11060506/is-there-a-not-equal-operator-in-python
    # http://stackoverflow.com/questions/1634352/what-is-the-difference-between-is-and-in-python
    print type(numToFind)
    numToFind = int(args[1])
    print type(numToFind)
    print '\n'

    dataList = loadInputDataFile(inputfile)

    if (len(dataList) > 0):

        print '***** Input numbers Inorder TO SEARCH into *****'
        print ','.join(str(x) for x in dataList)
        print '\n'

        # invoking search operation
        # foundLocationIdx = linearSearch(numToFind, dataList)
        foundLocationIdx = binSearch(numToFind, dataList)


        print '***** FOUND index location; -1 if not found *****'
        print foundLocationIdx
        print '\n'

# ATTENTION:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)


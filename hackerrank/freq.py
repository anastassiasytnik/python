def freqQuery(queries):
    """ given array of queries return output for check queries.

        query is a tuple of 2 integers. First integer is an operation and Second integer is the operand
        Operation can be 1, 2 or 3.
        If operation is "1" - you "add" the operand to your "array" (data structure) as a number
        If operation is "2" - you "delete" one occurence of the operand from your "array" (data structure) if it's there
        If operation is "3" - you check whether you have ANY number in your structure that occurs exactly as many times
        as the operand. If you have - then you append 1 to your output list, otherwise you append 0 to your output list
        Exaple:
            queries = [(1, 1), (2, 2), (3, 2), (1, 1), (1, 1), (2, 1), (3, 2)]
            First query (1, 1) = 'add number 1 to your "array"' - Your "array" becomes [1]
            Second query (2, 2) = 'remove one occurence of 2 from your "array" 
                                        - we don't have any 2s, so our "array" still [1]
            Third query (3, 2) = 'check if you have ANY number twice in your "array"' 
                                        - we don't, so we add 0 to output and our output is now [0]
            Forth and Fifth query (1, 1) = 'add number 1 to your "array" - so our "array" becomes [1, 1, 1]
            Sixth query (2, 1) = 'delete one occurence of 1 from your "array"'
                                        - our array is now [1, 1]
            Seventh query (3, 2) = "check if ANY number appears in your "array" twice.
                                        - number 1 appears in our "array" twice, so we add 1 to output ([0, 1])
    """
    # keys = numbers that were added to "array", values = how many times they occur in the "array"
    freq = {}

    # keys = occurences of numbers in our "array", values - how many DIFFERENT numbers in our "array" have that occurence.
    rev = {} # rev for reverse lookup

    # Example: if our "array" as a result of queries becomes [3, 20, 7, 1, 3, 3, 21, 7, 5, 5, 0]
    # then the freq dictionary will look like {3: 3, 20: 1, 7: 2, 1: 1, 21: 1, 5: 2, 0: 1}
    # and the rev dictionary will look like {1: 4, 2: 2, 3: 1}
    # 1: 4 because four different numbers - 20, 1, 21 and 0 appear only once
    # 2: 2 because two different numbers appear twice: number 7 and number 5
    # 3: 1 because only one number appears 3 times in our "array" - it's number 3

    # in here we will accumulate the result of queries with operation "3"
    result = []
    # go through queries and update all the data structures
    for operation, number in queries:
        if 1 == operation:
            # need to insert number v into "array"
            prevFrequency = freq.get(number, 0)
            if (prevFrequency > 0):
                # if we already had it before - the amount of different numbers of 2 frequencies change
                amount = rev[prevFrequency]
                if amount > 1:
                    # if we had other numbers with that frequency - we only need to reduce the amount
                    rev[prevFrequency] = amount - 1
                else:
                    # if it was the ONLY number with that frequency - we need to delete the entry
                    rev.pop(prevFrequency)
            # now this number occurs 1 more time
            freq[number] = prevFrequency + 1
            # update the amount of different numbers for the new frequency - as our freshly added number is now there
            rev[prevFrequency + 1] = rev.get(prevFrequency + 1, 0) + 1
        elif 2 == operation and freq.get(number, 0) > 0:
            # only here if we have the number we need to delete
            count = freq[number] - 1
            freq[number] = count
            # if after the deletion the number still present in our "array" 
            if count > 0:
                # then we need to update the smaller occurence amount
                rev[count] = rev.get(count, 0) + 1
            # we definitely need to update the OLD occurence 
            amount = rev[count + 1]
            if amount == 1:
                # if our number was THE ONLY number that occured previous amount of times - then we delete the entry
                rev.pop(count + 1)
            else:
                # otherwise reduce the number
                rev[count + 1] = amount - 1
        elif 3 == operation:
            output = 0
            amount = rev.get(number, 0)
            if amount > 0:
                # we have numbers that occur that many times
                output = 1
            result.append(output)
    # all done
    return result

# simple test
print(freqQuery([(3, 4), (2, 1003), (1, 16), (3, 1)]))

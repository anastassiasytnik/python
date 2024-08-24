def countTripletsSlow(arr, r):
    info = {}
    rSqua = r * r
    for i in range(len(arr)):
        idxList = info.get(arr[i])
        if idxList is None:
            idxList = []
        idxList.append(i)
        info[arr[i]] = idxList
    #now all numbers are there
    tripCount = 0
    for num in sorted(info):
        current = info[num]
        next = info.get(num * r, None)
        last = info.get(num * rSqua, None)
        if next is not None and last is not None:
            # try to get all triplets
            # get all doubles
            doubles = []
            for ci in current:
                for ni in next:
                    if (ni > ci):
                        doubles.append(ni)
            # now add third?
            for ni in doubles:
                for li in last:
                    if (li > ni):
                        tripCount += 1
    return tripCount
        
def countTriplets(arr, r, debug = False):
    singles = {}
    doubles = {}
    tripCount = 0
    idx = 0
    for num in arr:
        if (num % (r * r) == 0):
            # means it might be third number in triplets - check if there's doubles
            doublesNum = doubles.get(int(num // r), 0)
            if doublesNum > 0:
                tripCount += doublesNum
        if (num % r == 0):
            prev = int(num // r)
            exist = singles.get(prev, 0)
            if (exist > 0):
                # means we found AT LEAST second member of the progression
                doubles[num] = doubles.get(num, 0) + exist

        # update first number occurences
        singles[num] = singles.get(num, 0) + 1

        idx += 1
        if (debug):
            print("Processed: ", idx)
            print("SINGLES NOW: ", singles)
            print("DOUBLES NOW: ", doubles)
            print("TRIPLE COUNT NOW: ", tripCount)
    return tripCount

print(countTriplets([1, 2, 2, 4], 2))
print(countTriplets([1, 3, 9, 9, 27, 81], 3))
print(countTriplets([1, 5, 5, 25, 125], 5))
print(countTriplets([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 1, True))

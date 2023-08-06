from random import shuffle
from time import perf_counter
from typing import List


def bubblesort(test_case):
    for j in range(len(test_case), 2, -1):
        for i in range(0, j - 1):
            if test_case[i] > test_case[i + 1]:
                test_case[i], test_case[i + 1] = test_case[i + 1], test_case[i]


def insertionsort(test_case):
    for i in range(1, len(test_case)):
        value = test_case[i]
        j = i
        while j > 0 and test_case[j - 1] > value:
            test_case[j] = test_case[j - 1]
            j -= 1
        test_case[j] = value


def mergesort(test_case):
    def merge(llist: List[int], rlist: List[int]):
        mlist = []
        while llist and rlist:
            if llist[0] <= rlist[0]:
                mlist.append(llist.pop(0))
            else:
                mlist.append(rlist.pop(0))
        mlist.extend(llist)
        llist.clear()
        mlist.extend(rlist)
        rlist.clear()
        return mlist

    if len(test_case) <= 1:
        return test_case
    else:
        half = len(test_case) // 2
        llist = mergesort(test_case[:half])
        rlist = mergesort(test_case[half:])
        return merge(llist, rlist)


BPERCENT = 1
IPERCENT = 1
MPERCENT = 1
COUNT = 150
SIZE = 1000

test_case = list(range(SIZE))

stats = {"Bubblesort": [], "Insertionsort": [], "Mergesort": []}

print(f"\n{SIZE = }\nCOUNT = {COUNT} ({BPERCENT} | {IPERCENT} | {MPERCENT})")
print(
    "\n===================================Starting=====================================\n"
)

for n in range(COUNT):
    if n < int(COUNT * BPERCENT):
        # Bubblesort
        shuffle(test_case)
        t1 = perf_counter()

        bubblesort(test_case)

        t2 = perf_counter()
        stats["Bubblesort"].append(t2 - t1)
    if n < int(COUNT * IPERCENT):
        # Inserion sort
        shuffle(test_case)
        t1 = perf_counter()

        insertionsort(test_case)

        t2 = perf_counter()
        stats["Insertionsort"].append(t2 - t1)
    if n < int(COUNT * MPERCENT):
        # Mergesort
        shuffle(test_case)
        t1 = perf_counter()

        test_case = mergesort(test_case)

        t2 = perf_counter()
        stats["Mergesort"].append(t2 - t1)
    print(
        f"Test Case #{n+1} ({sum(stats['Bubblesort'])+sum(stats['Insertionsort'])+sum(stats['Mergesort']):.3f})\tBs: {stats['Bubblesort'][-1]:.3f} ({sum(stats['Bubblesort']):.3f}); Is: {stats['Insertionsort'][-1]:.3f} ({sum(stats['Insertionsort']):.3f}); Ms: {stats['Mergesort'][-1]:.3f} ({sum(stats['Mergesort']):.3f}) {'.'*(n%4)+' '*(3-(n%4))}",
        end="\r",
    )

print(
    "\n\n===================================Finished=====================================\n"
)

print(
    f"Bubblesort in {sum(stats['Bubblesort'])/COUNT:.3f} ({min(stats['Bubblesort']):.4f})"
)
print(
    f"Insertionsort in {sum(stats['Insertionsort'])/COUNT:.3f} ({min(stats['Insertionsort']):.4f})"
)
print(
    f"Mergesort in {sum(stats['Mergesort'])/COUNT:.3f} ({min(stats['Mergesort']):.4f})"
)

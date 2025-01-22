## Part 1
---
An easy start and a fairly trivial solution. We're given a list that looks like this:
```
3   4
4   3
2   5
1   3
3   9
3   3
```

We're asked to calculate the distance score which is the absolute difference between the smallest number in both lists. For the example it would be $abs(1-3)=2$.

To get the smallest number and since we won't need it after, this is very obviously best done using a min-heap.
```python
def get_distance(lists: tuple[list, list]) -> int:

    h1: list[int] = copy.deepcopy(lists[0])
    h2: list[int] = copy.deepcopy(lists[1])

    heapify(h1)
    heapify(h2)

    distance: int = 0

    for _ in range(len(h1)):
        distance += abs(heappop(h1) - heappop(h2))

    return distance
```

## Part 2
---
For the second part, we have to calculate the similarity score. You calculate this by taking the **summing up the product of a number in the first list and the number of it's occurrences in the second list.**

This is fairly trivial by just using `collections.Counter` from the standard library.
```python
def get_similarity_score(lists: tuple[list, list]) -> int:
    l1: list[int]
    l2: list[int]

    l1, l2 = lists

    cnt: Counter = Counter(l2)
    similarity_score: int = 0

    for n in l1:
        if n in cnt:
            similarity_score += n * cnt[n]

    return similarity_score
```

## Conclusion
---
A fairly easy start and a fun way to get the brain cooking. Hope this helps. Cheers.
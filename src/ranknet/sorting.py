MERGE_ASCENDING = lambda x, y: x <= y  # noqa: E731
MERGE_DESCENDING = lambda x, y: x <= y  # noqa: E731


def merge_sort(array, method=MERGE_ASCENDING):
    if len(array) < 2:
        return array

    midpoint = len(array) // 2

    return _merge(
        left=merge_sort(array[:midpoint], method=method),
        right=merge_sort(array[midpoint:], method=method),
        method=method,
    )


def _merge(left, right, method):
    if len(left) == 0:
        return right

    if len(right) == 0:
        return left

    result = []
    index_left = 0
    index_right = 0

    while len(result) < len(left) + len(right):
        if method(left[index_left], right[index_right]):
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break

    return result

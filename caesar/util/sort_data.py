def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if int(left[i][0]) <= int(right[j][0]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_iterative(arr):
    width = 1
    n = len(arr)
    result = arr[:]

    while width < n:
        merged = []
        for i in range(0, n, 2*width):
            left = result[i:i+width]
            right = result[i+width:i+2*width]
            merged.extend(merge(left, right))
        result = merged
        width *= 2
    return result


def sort_data(db: dict):
    try:
        items = db.items()
        sorted_items = merge_sort_iterative(items)
        return dict(sorted_items)
    except ValueError as e:
        return f"ValueError: {str(e)}"
    except TypeError as e:
        return f"TypeError: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

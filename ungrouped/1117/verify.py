def count_inserts_merge_sorted_lists(list1, list2):
    merged_list = []
    i, j = 0, 0
    insert_count = 0

    while i < len(list1) and j < len(list2):
        insert_count += 1  # Count the comparison
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    # Append remaining elements (if any)
    while i < len(list1):
        insert_count += 1  # Count the insert
        merged_list.append(list1[i])
        i += 1

    while j < len(list2):
        insert_count += 1  # Count the insert
        merged_list.append(list2[j])
        j += 1
        
    return merged_list, insert_count


def optimal_pairwise_merge(lists):
    insert_count = 0
    while len(lists) > 1:
        new_lists = []
        for i in range(0, len(lists), 2):
            if i + 1 < len(lists):
                merged, count = count_inserts_merge_sorted_lists(lists[i], lists[i + 1])
                insert_count += count
                new_lists.append(merged)
            else:
                new_lists.append(lists[i])
        lists = new_lists
    return lists[0], insert_count


def less_structured_merge(lists):
    total_insert_count = 0
    # Merge lists sequentially
    merged_list = lists[0]
    
    for i in range(1, len(lists)):
        merged_list, insert_count = count_inserts_merge_sorted_lists(merged_list, lists[i])
        total_insert_count += insert_count
    
    return merged_list, total_insert_count


# Sample sorted lists
lists = [
    [1, 5, 9],
    [2, 6, 10],
    [3, 7, 11],
    [4, 8, 12]
]z

# Run both merging methods
optimal_result, optimal_inserts = optimal_pairwise_merge(lists)
less_structured_result, less_structured_inserts = less_structured_merge(lists)

# Print results
print("Optimal Pairwise Merge Result:", optimal_result)
print("Optimal Pairwise Merge Insert Counts:", optimal_inserts)

print("Less Structured Merge Result:", less_structured_result)
print("Less Structured Merge Insert Counts:", less_structured_inserts)

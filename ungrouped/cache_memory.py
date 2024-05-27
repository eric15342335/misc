def add_cache(cache:list[dict], block:int, history:int, miss:int)->tuple:
    address = block % 4
    if cache[address].get(block):
            cache[address][block] = history
            return cache, miss;
    if len(cache[address]) < 2:
        cache[address][block] = history
        miss += 1
        return cache, miss;
    assert len(cache[address]) < 3
    for data in cache[address]:
        # least recently used
        if cache[address][data] == min(cache[address].values()):
            del cache[address][data]
            cache[address][block] = history
            miss += 1
            return cache, miss;


def direct_map_add_cache(cache:list[dict], block:int, history:int, miss:int)->tuple:
    address = block % 8
    if cache[address].get(block):
        cache[address][block] = history
        return cache, miss;
    else:
        cache[address] = {block:history}
        miss += 1
        return cache, miss;



counter = 1
miss = 0
cache = [{},{},{},{},{},{},{},{}]
for i in ['1', '2', '3', '5', '6', '2', '3', '4', '9', '10', '11', '6', '3', '6', '1', '7', '8', '4', '5', '9', '11', '1', '2', '4', '5', '12', '13', '14', '15', '13', '14']:
    cache, miss = direct_map_add_cache(cache, int(i), counter, miss)
    counter += 1
    print(i, cache, miss)

counter = 1
miss = 0
cache = [{},{},{},{}]
for i in ['1', '2', '3', '5', '6', '2', '3', '4', '9', '10', '11', '6', '3', '6', '1', '7', '8', '4', '5', '9', '11', '1', '2', '4', '5', '12', '13', '14', '15', '13', '14']:
    cache, miss = add_cache(cache, int(i), counter, miss)
    counter += 1
    print(i, cache, miss)

physical_memory = []
page_table = []
tlb = []
oldest_tlb_entry = 0


def load_page(page_no):
    n = len(page_table)
    start = n * 256
    page_table.append((page_no, start))
    with open('BACKING_STORE.bin', 'rb') as f:
        f.seek(page_no * 256)
        physical_memory[start:start + 256] = f.read(256)
    return start


def to_signed_byte(b):
    if b > 127:
        return (256 - b) * (-1)
    else:
        return b


def search_page_table(page_no):
    for pn, page_start in page_table:
        if pn == page_no:
            return page_start
    return -1


def search_tlb(page_no):
    for pn, page_start in tlb:
        if pn == page_no:
            return page_start
    return -1


def update_tlb(page_no, page_start):
    global oldest_tlb_entry
    if len(tlb) < 16:
        tlb.append((page_no, page_start))
    else:
        tlb[oldest_tlb_entry] = (page_no, page_start)
        oldest_tlb_entry = (oldest_tlb_entry + 1) % 16


if __name__ == '__main__':
    correct_outputs = open('correct.txt', 'r').readlines()

    addresses = open('addresses.txt', 'r').readlines()

    for i in range(len(addresses)):
        n = int(addresses[i])
        offset = n & 255
        page_no = (n >> 8) & 255
        page_start = search_tlb(page_no)
        if page_start == -1:
            page_start = search_page_table(page_no)
            if page_start == -1:
                page_start = load_page(page_no)
            update_tlb(page_no, page_start)

        physical_addr = page_start + offset
        output = f'Virtual address: {n} Physical address: {physical_addr} Value: {to_signed_byte(physical_memory[physical_addr])}'
        print(output)
        assert output == correct_outputs[i][:-1]



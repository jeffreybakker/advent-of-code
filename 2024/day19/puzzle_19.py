import functools

stock: set[str]
orders: list[str]
with open("input_19.txt", "r") as f:
    lines = iter(line.strip() for line in f.readlines())
    stock = set(next(lines).split(", "))
    orders = [line for line in lines if line]


max_stock_len = max(len(stock) for stock in stock)


def order_possible(order: str) -> bool:
    @functools.cache
    def recurse(substr: str) -> bool:
        if len(substr) == 0:
            return True

        for i in range(max_stock_len):
            match = substr[:max_stock_len - i]
            if match not in stock:
                continue

            res = recurse(substr[max_stock_len - i:])
            if res:
                return True

        return False

    return recurse(order)


print("Part A:", sum(map(order_possible, orders)))


# ##
# # Part 2
# ##
def order_options(order: str) -> int:
    @functools.cache
    def recurse(substr: str) -> int:
        if len(substr) == 0:
            return 1

        res = 0
        max_len = min(max_stock_len, len(substr))
        for i in range(max_len):
            match = substr[:max_len - i]
            if match not in stock:
                continue

            res += recurse(substr[max_len - i:])

        return res

    return recurse(order)


print("Part B:", sum(map(order_options, orders)))

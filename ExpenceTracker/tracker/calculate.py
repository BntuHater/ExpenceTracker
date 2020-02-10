from datetime import datetime


def calc_all_time_stats(products):
    stats = dict()
    categories = list()
    total = 0

    for product in products:
        categories.append(product.category)

    for category in categories:
        expences = 0
        for product in products:
            if product.category == category:
                price = product.product_price
                expences += price
                stats[category] = expences  

    for category, expences in stats.items():
        total += expences
    return (stats, total)


def calc_current_month_stats(products):
    today = datetime.today()
    m_products = list()
    categories = list()
    stats = dict()
    total = 0

    for product in products:
        date = product.purchase_date
        if date.year == today.year and date.month == today.month:
            m_products.append(product)
            categories.append(product.category)

    for category in categories:
        expences = 0
        for product in m_products:
            if product.category == category:
                price = product.product_price
                expences += price
                stats[category] = expences

    for category, expences in stats.items():
        total += expences
    return (stats, total)


def calc_previous_month_stats(products):
    today = datetime.today()
    if today.month != 1:
        month = today.month - 1
        year = today.year
    else:
        month = 12
        year = today.year - 1

    m_products = list()
    categories = list()
    stats = dict()
    total = 0

    for product in products:
        date = product.purchase_date
        if date.year == year and date.month == month:
            m_products.append(product)
            categories.append(product.category)

    for category in categories:
        expences = 0
        for product in m_products:
            if product.category == category:
                price = product.product_price
                expences += price
                stats[category] = expences
    
    for category, expences in stats.items():
        total += expences
    return (stats, total)


def calc_ranged_stats(products, start, end):
    product_list = list()
    categories = list()
    stats = dict()
    total = 0

    if start > end:
        start, end = end, start

    for product in products:
        date = product.purchase_date
        if date.day >= start.day and date.day <= end.day:
            if date.month >= start.month and date.month <= end.month:
                if date.year >= start.year and date.year <= end.year:
                    product_list.append(product)
                    categories.append(product.category)
    
    for category in categories:
        expences = 0
        for product in product_list:
            if product.category == category:
                price = product.product_price
                expences += price
                stats[category] = expences

    for category, expences in stats.items():
        total += expences
    print(product_list)
    return (stats, total)

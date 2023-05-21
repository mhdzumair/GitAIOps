def paginate_content(data, page, per_page):
    """
    Paginates a data string.

    Takes the data, the desired page number, and the number of items per page as input.
    Calculates the start and end indices for the desired page and returns the corresponding slice of the data.
    Also returns a dictionary with pagination details, including the current page, items per page, and total pages.

    Args:
        data (str): The data string to be paginated.
        page (int): The desired page number.
        per_page (int): The number of items per page.

    Returns:
        tuple: A tuple containing the paginated data string and a dictionary with pagination details.
    """
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]
    return paginated_data, {
        "page": page,
        "per_page": per_page,
        "total_pages": len(data) // per_page + (1 if len(data) % per_page else 0),
    }

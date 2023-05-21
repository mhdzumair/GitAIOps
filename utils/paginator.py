def paginate_content(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]
    return paginated_data, {
        "page": page,
        "per_page": per_page,
        "total_pages": len(data) // per_page + (1 if len(data) % per_page else 0),
    }

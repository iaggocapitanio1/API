query_without_city = "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?)" \
                     "and (daily >=  ? and daily <= ?)  LIMIT ?  OFFSET ?"

query_with_city = "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?) and (daily >=  ? and daily <= ?)" \
                  " and city = ? LIMIT ?  OFFSET ? "


def normalize_path_args(city=None,
                        stars_min=0,
                        stars_max=5,
                        daily_min=0,
                        daily_max=10e3,
                        limit=20,
                        offset=0,
                        **kwargs):
    if city:
        return {
            'stars_min': stars_min,
            'stars_max': stars_max,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'city': city,
            'limit': limit,
            'offset': offset
        }
    return {
        'stars_min': stars_min,
        'stars_max': stars_max,
        'daily_min': daily_min,
        'daily_max': daily_max,
        'limit': limit,
        'offset': offset
    }

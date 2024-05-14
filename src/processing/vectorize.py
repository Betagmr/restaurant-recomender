from src.processing.classify_reviews import add_class_reviews
from src.processing.dist import add_direction_location
from src.processing.extract_features import add_extra_features, add_restaurant_types
from src.processing.price_range import add_price_range


def transform_to_vector_df(df):
    data = df.copy()
    data = add_direction_location(data)
    data = add_restaurant_types(data)
    data = add_extra_features(data)
    data = add_price_range(data)
    data = add_class_reviews(data)

    return data.drop(columns=data.columns[1:11])

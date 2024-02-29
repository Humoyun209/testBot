from datetime import datetime, timedelta
from typing import Literal
import pymongo
from bson.son import SON


mongo_url = "mongodb+srv://humoyun209:Mq7uqpPetSXZuMML@cluster0.sllmawu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_url)
collection = client.xz.net


def get_format(type_format: str):
    match type_format:
        case "month":
            return "%Y-%m-01T00:00:00"
        case "day":
            return "%Y-%m-%dT00:00:00"
        case "hour":
            return "%Y-%m-%dT%H:00:00"
    return None


def get_result(dt_from: str, dt_to: str, type_format):
    start_date = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    end_date = datetime.strptime(dt_to, "%Y-%m-%dT%H:%M:%S")

    if not type_format:
        return None

    format = get_format(type_format)

    pipeline = [
        {
            "$group": {
                "_id": {"year": {"$year": "$dt"}, "month": {"$month": "$dt"}},
                "total_value": {"$sum": "$value"},
            }
        },
    ]

    pipeline = [
        {"$match": {"dt": {"$gte": start_date, "$lte": end_date}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": format,
                        "date": "$dt",
                        "timezone": "+00:00",
                    }
                },
                "total_value": {"$sum": "$value"},
            }
        },
        {"$sort": SON([("_id", 1)])},
    ]

    result = list(collection.aggregate(pipeline))

    dataset = [entry["total_value"] for entry in result]
    labels = [entry["_id"] for entry in result]

    if type_format != "month":

        all_labels = []
        current_date = start_date

        while current_date <= end_date:
            all_labels.append(current_date.strftime(format))
            current_date += (
                timedelta(days=1) if type_format == "day" else timedelta(hours=1)
            )
        filled_dataset = []
        for label in all_labels:
            if label in labels:
                index = labels.index(label)
                filled_dataset.append(dataset[index])
            else:
                filled_dataset.append(0)

        return {"dataset": filled_dataset, "labels": all_labels}
    return {"dataset": dataset, "labels": labels}


timedelta()

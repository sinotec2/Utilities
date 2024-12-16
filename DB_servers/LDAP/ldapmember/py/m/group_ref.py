## module m
## FreeIPA group相關物件

def getdict():
    """
    組別中文對應groupname dict
    如："空品組": "Air"
    """
    group_dict = {
        "環評組": "EIA",
        "風機組": "Wind",
        "空品組": "Air",
        "碳管組": "Carbon",
        "管線組": "Pipeline",
        "廠站組": "Water",
        "廢棄物組": "Waste",
        "土水組": "Soil",
        "場廠組(興建)": "Construction",
        "場廠組(營管)": "Operation",
        "產業輔導組": "Counseling",
        "研發及資訊部": "ICT",
        "行政及支援部": "Admin",
    }
    return group_dict


def gerTuple():
    """
    Groupname Tuple
    """
    group_Tuple = (
        "EIA",
        "Wind",
        "Air",
        "Carbon",
        "Pipeline",
        "Water",
        "Waste",
        "Soil",
        "Construction",
        "Operation",
        "Counseling",
        "ICT",
        "Admin",
    )
    return group_Tuple

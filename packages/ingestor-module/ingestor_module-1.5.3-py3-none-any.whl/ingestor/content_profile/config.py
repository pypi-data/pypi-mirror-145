from ingestor.common.constants import (
    CONTENT_ID,
    YEAR,
    DURATION_MINUTE,
    TITLE,
    STATUS,
    IS_GEO_BLOCK,
    IS_FREE,
    IS_ORIGINAL,
    IS_BRANDED,
    IS_EXCLUSIVE,
    SYNOPSIS,
    SYNOPSIS_EN,
    START_DATE,
    END_DATE,
    MODIFIED_ON,
    TYPE,
    RATING,
)


# Content Node Properties


def content_node_properties(property_value):
    node_property = {CONTENT_ID: property_value[CONTENT_ID],
                     YEAR: property_value[YEAR],
                     DURATION_MINUTE: property_value[DURATION_MINUTE],
                     TITLE: property_value[TITLE],
                     STATUS: property_value[STATUS],
                     IS_GEO_BLOCK: property_value[IS_GEO_BLOCK],
                     IS_FREE: property_value[IS_FREE],
                     IS_ORIGINAL: property_value[IS_ORIGINAL],
                     IS_BRANDED: property_value[IS_BRANDED],
                     IS_EXCLUSIVE: property_value[IS_EXCLUSIVE],
                     SYNOPSIS: property_value[SYNOPSIS],
                     SYNOPSIS_EN: property_value[SYNOPSIS_EN],
                     START_DATE: str(property_value[START_DATE]),
                     END_DATE: str(property_value[END_DATE]),
                     MODIFIED_ON: str(property_value[MODIFIED_ON]),
                     TYPE: property_value[TYPE],
                     RATING: property_value[RATING]
                     }
    return node_property


"""DEFINING RELATIONSHIP NAMES"""
HAS_CATEGORY = "HAS_CATEGORY"
HAS_SUBCATEGORY = "HAS_SUBCATEGORY"
HAS_COUNTRY = "HAS_COUNTRY"
HAS_TAG = "HAS_TAG"
HAS_ACTOR = "HAS_ACTOR"
HAS_CONTENT_CORE = "HAS_CONTENT_CORE"
HAS_PRODUCT = "HAS_PRODUCT"
HAS_PACKAGE = "HAS_PACKAGE"
HAS_HOMEPAGE = "HAS_HOMEPAGE"

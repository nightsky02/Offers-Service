
class ExcelParsingError(Exception):
    pass

class UniqueOfferException(ExcelParsingError):
    """Raises when two same offer id were found during parsing excel file"""
    def __init__(self, offer_id: int, offer_name: str):
        self.offer_id = offer_id
        self.offer_name = offer_name

class FileStructureError(ExcelParsingError):
    """Raises when the excel file contains the wrong count of cells"""

    def __init__(self, message: str):
        self.msg = message

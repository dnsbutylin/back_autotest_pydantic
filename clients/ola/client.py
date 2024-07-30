"""OLA API клиент"""

from .._meta import category
from .._session import Session
from .category import Comments, Companies, Complaints, DataFields, Entities, Negatives


class OlaClient(Session):
    """OLA API Client"""

    @category(Entities)
    def entities(self) -> Entities:
        """Раздел entities"""

    @category(Companies)
    def companies(self) -> Companies:
        """Раздел companies"""

    @category(DataFields)
    def data_fields(self) -> DataFields:
        """Раздел data-fields"""

    @category(Comments)
    def comments(self) -> Comments:
        """Раздел comments"""

    @category(Negatives)
    def negatives(self) -> Negatives:
        """Раздел negatives"""

    @category(Complaints)
    def complaints(self) -> Complaints:
        """Раздел complaints"""

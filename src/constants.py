"""Наборы констант"""

from typing import Final

from .user_types import Constant

DATE_FORMAT: Final[str] = "%Y-%m-%d"

# Символы разрешенные для использования в ФИО
ALLOWED_CHARACTERS: Final[tuple[str, ...]] = ("-", " ")


class LEType(Constant):
    """Типы ЮЛ"""

    COMP: Final[str] = "ЮЛ"
    IP: Final[str] = "ИП"


class FieldsLength:
    """Ограничения на длину строк"""

    MAX_LENGTH: Final[int] = 200
    MIN_LENGTH: Final[int] = 1


class ErrorText(Constant):
    """Тексты ошибок"""

    VALIDATION_ERROR: Final[str] = "validation error"
    REQUIRED: Final[str] = "required"
    MUST_NOT_BE_EMPTY: Final[str] = "must not be empty"
    MORE_THAN_MAX_LEN: Final[str] = "more than max len {length}"
    INVALID_FORMAT: Final[str] = "invalid format"
    EXPECTED_TYPE_STRING: Final[str] = "expected type string"
    EXPECTED_TYPE_MAP: Final[str] = "expected type map"
    INVALID_BIRTHDATE: Final[str] = "must be format: 2006-01-02"
    MUST_NOT_BE_IN_THE_FUTURE: Final[str] = "must not be in the future"
    MISSING: Final[str] = "missing"
    MISSING_ENTITY: Final[str] = "missing entity"
    MUST_BE_ONE_OF_ALLOWED_LEASING_OBJECT_TYPES: Final[str] = "must be one of allowed leasing object types"
    MUST_NOT_START_WITH_SYMBOL: Final[str] = 'must not start with symbol "{symbol}"'
    MUST_NOT_END_WITH_SYMBOL: Final[str] = 'must not end with symbol "{symbol}"'
    TOO_MANY: Final[str] = "too_many"
    TOO_MANY_PERSONS_FOUND: Final[str] = "too many persons found"


class CardType(Constant):
    """Типы карточек"""

    LEGAL_ENTITY: Final[str] = "legal-entity"  # Юрик
    PERSON: Final[str] = "person"  # Физик
    LEASING_OBJECT: Final[str] = "leasing-object"  # Объект лизинга


class PersonCardRequiredField(Constant):
    """Обязательные поля для создания ФЛ"""

    LASTNAME: Final[str] = "lastname"
    FIRSTNAME: Final[str] = "firstname"
    RUSSIAN_PASSPORT: Final[str] = "russian_passport"
    BIRTHDATE: Final[str] = "birthdate"


class LegalEntityCardRequiredField(Constant):
    """Обязательные поля для создания ЮЛ"""

    INN: Final[str] = "inn"


class LeasingObjectCardRequiredField(Constant):
    """Обязательные поля для создания ОЛ"""

    TITLE: Final[str] = "title"
    IDENTIFIER: Final[str] = "identifier"


class LeasingObjectCardIdentifierRequiredField(Constant):
    """Обязательные поля для создания ОЛ объекта identifier"""

    VALUE: Final[str] = "value"
    TYPE: Final[str] = "type"


class SearchLeasingObjectCardRequiredField(Constant):
    """Обязательные поля для поиска ОЛ"""

    IDENTIFIER: Final[str] = "identifier"
    IDENTIFIER_TYPE: Final[str] = "identifier_type"


class LeasingObjectType(Constant):
    """Типы объектов лизинга"""

    # 1 Недвижимость, за исключением судов и космических объектов.
    # 1.1 Здание.
    REALTY_BUILDING = "REALTY_BUILDING"
    # 1.2 Сооружение.
    REALTY_STRUCTURE = "REALTY_STRUCTURE"
    # 1.3 Помещение.
    REALTY_PREMISES = "REALTY_PREMISES"
    # 1.4 Машино-место.
    REALTY_PARKING_SPOT = "REALTY_PARKING_SPOT"
    # 1.5 Объект незавершенного строительства.
    REALTY_INCOMPLETE_CONSTRUCTION = "REALTY_INCOMPLETE_CONSTRUCTION"
    # 1.6 Земельный участок.
    REALTY_LAND_PLOT = "REALTY_LAND_PLOT"
    # 1.7 Единый недвижимый комплекс.
    REALTY_REAL_ESTATE_COMPLEX = "REALTY_REAL_ESTATE_COMPLEX"
    # 1.8 Имущественный комплекс.
    REALTY_PROPERTY_COMPLEX = "REALTY_PROPERTY_COMPLEX"

    # 2 Транспортные средства.
    # 2.1 Самоходная машина.
    TRANSPORTATION_VEHICLE_SELF_PROPELLED_MACHINE = "TRANSPORTATION_VEHICLE_SELF_PROPELLED_MACHINE"
    # 2.2 Иное транспортное средство.
    TRANSPORTATION_VEHICLE_OTHER = "TRANSPORTATION_VEHICLE_OTHER"

    # 3 Машины и оборудование.
    # 3.1 Сельскохозяйственное оборудование.
    MACHINERY_AND_EQUIPMENT_AGRICULTURAL_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_AGRICULTURAL_EQUIPMENT"
    # 3.2 Оборудование для строительства.
    MACHINERY_AND_EQUIPMENT_CONSTRUCTION_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_CONSTRUCTION_EQUIPMENT"
    # 3.3 Оборудование для добычи полезных ископаемых.
    MACHINERY_AND_EQUIPMENT_MINING_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_MINING_EQUIPMENT"
    # 3.4 Оборудование нефтеперерабатывающей и нефтехимической промышленности.
    MACHINERY_AND_EQUIPMENT_OIL_PROCESSING_AND_PETROCHEMICAL_EQUIPMENT = (
        "MACHINERY_AND_EQUIPMENT_OIL_PROCESSING_AND_PETROCHEMICAL_EQUIPMENT"
    )
    # 3.5 Оборудование черной и цветной металлургии.
    MACHINERY_AND_EQUIPMENT_METALLURGICAL_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_METALLURGICAL_EQUIPMENT"
    # 3.6 Оборудование металлообрабатывающее.
    MACHINERY_AND_EQUIPMENT_METALWORKING_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_METALWORKING_EQUIPMENT"
    # 3.7 Оборудование деревообрабатывающее и целлюлозно-бумажной промышленности.
    MACHINERY_AND_EQUIPMENT_WOODWORKING_AND_PULP_PAPER_INDUSTRY_EQUIPMENT = (
        "MACHINERY_AND_EQUIPMENT_WOODWORKING_AND_PULP_PAPER_INDUSTRY_EQUIPMENT"
    )
    # 3.8 Энергетическое оборудование.
    MACHINERY_AND_EQUIPMENT_POWER_ENGINEERING_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_POWER_ENGINEERING_EQUIPMENT"
    # 3.9 Оборудование легкой промышленности.
    MACHINERY_AND_EQUIPMENT_LIGHT_INDUSTRY_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_LIGHT_INDUSTRY_EQUIPMENT"
    # 3.10 Оборудование пищевой промышленности.
    MACHINERY_AND_EQUIPMENT_FOOD_INDUSTRY_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_FOOD_INDUSTRY_EQUIPMENT"
    # 3.11 Медицинское оборудование.
    MACHINERY_AND_EQUIPMENT_MEDICAL_EQUIPMENT = "MACHINERY_AND_EQUIPMENT_MEDICAL_EQUIPMENT"
    # 3.12 Вычислительное и телекоммуникационное оборудование.
    MACHINERY_AND_EQUIPMENT_COMPUTER_AND_TELECOMMUNICATION_EQUIPMENT = (
        "MACHINERY_AND_EQUIPMENT_COMPUTER_AND_TELECOMMUNICATION_EQUIPMENT"
    )
    # 3.99 Иное.
    MACHINERY_AND_EQUIPMENT_OTHER = "MACHINERY_AND_EQUIPMENT_OTHER"

    # 4 Воздушные суда.
    # 4.1 Самолет.
    AIRCRAFT_AIRPLANE = "AIRCRAFT_AIRPLANE"
    # 4.2 Вертолет.
    AIRCRAFT_HELICOPTER = "AIRCRAFT_HELICOPTER"
    # 4.99 Иное.
    AIRCRAFT_OTHER = "AIRCRAFT_OTHER"

    # 5 Плавучие сооружения.
    # 5.1 Судно для перевозки пассажиров и их багажа.
    FLOATING_STRUCTURES_PASSENGER_AND_LUGGAGE_VESSEL = "FLOATING_STRUCTURES_PASSENGER_AND_LUGGAGE_VESSEL"
    # 5.2 Судно для перевозки грузов или буксировки, а также для хранения грузов.
    FLOATING_STRUCTURES_CARGO_OR_TOWING_VESSEL = "FLOATING_STRUCTURES_CARGO_OR_TOWING_VESSEL"
    # 5.3 Судно для рыболовства.
    FLOATING_STRUCTURES_FISHING_VESSEL = "FLOATING_STRUCTURES_FISHING_VESSEL"
    # 5.4 Судно для иных целей.
    FLOATING_STRUCTURES_OTHER_PURPOSE_VESSEL = "FLOATING_STRUCTURES_OTHER_PURPOSE_VESSEL"
    # 5.5 Плавучее сооружение, не являющееся судном.
    FLOATING_STRUCTURES_NON_VESSEL_FLOATING_STRUCTURE = "FLOATING_STRUCTURES_NON_VESSEL_FLOATING_STRUCTURE"

    # 6 Железнодорожный подвижной состав.
    # 6.1 Локомотив.
    RAILWAY_ROLLING_STOCK_LOCOMOTIVE = "RAILWAY_ROLLING_STOCK_LOCOMOTIVE"
    # 6.2 Самоходная единица специального железнодорожного подвижного состава.
    RAILWAY_ROLLING_STOCK_SELF_PROPELLED_SPECIAL_RAILWAY_ROLLING_STOCK = (
        "RAILWAY_ROLLING_STOCK_SELF_PROPELLED_SPECIAL_RAILWAY_ROLLING_STOCK"
    )
    # 6.3 Вагон моторвагонного подвижного состава.
    RAILWAY_ROLLING_STOCK_MOTOR_RAILCAR = "RAILWAY_ROLLING_STOCK_MOTOR_RAILCAR"
    # 6.4 Грузовой вагон.
    RAILWAY_ROLLING_STOCK_FREIGHT_WAGON = "RAILWAY_ROLLING_STOCK_FREIGHT_WAGON"
    # 6.5 Пассажирский вагон локомотивной тяги.
    RAILWAY_ROLLING_STOCK_LOCOMOTIVE_HAULED_PASSENGER_CAR = "RAILWAY_ROLLING_STOCK_LOCOMOTIVE_HAULED_PASSENGER_CAR"
    # 6.6 Вагон высокоскоростного железнодорожного подвижного состава.
    RAILWAY_ROLLING_STOCK_HIGH_SPEED_RAILWAY_ROLLING_STOCK = "RAILWAY_ROLLING_STOCK_HIGH_SPEED_RAILWAY_ROLLING_STOCK"
    # 6.7 Несамоходная единица специального железнодорожного подвижного состава.
    RAILWAY_ROLLING_STOCK_NON_SELF_PROPELLED_SPECIAL_RAILWAY_ROLLING_STOCK = (
        "RAILWAY_ROLLING_STOCK_NON_SELF_PROPELLED_SPECIAL_RAILWAY_ROLLING_STOCK"
    )

    # 7 Космические объекты.
    # 7.1 Космический объект.
    SPACE_OBJECTS_SPACE_OBJECT = "SPACE_OBJECTS_SPACE_OBJECT"

    # 8 Товары в обороте.
    # 8.1 Сельскохозяйственная продукция, в том числе продукты растениеводства.
    GOODS_IN_CIRCULATION_AGRICULTURAL_PRODUCTS = "GOODS_IN_CIRCULATION_AGRICULTURAL_PRODUCTS"
    # 8.2 Животные заменимые.
    GOODS_IN_CIRCULATION_REPLACEABLE_ANIMALS = "GOODS_IN_CIRCULATION_REPLACEABLE_ANIMALS"
    # 8.3 Продукты пищевые, напитки, изделия табачные.
    GOODS_IN_CIRCULATION_FOOD_PRODUCTS_BEVERAGES_TOBACCO_PRODUCTS = (
        "GOODS_IN_CIRCULATION_FOOD_PRODUCTS_BEVERAGES_TOBACCO_PRODUCTS"
    )
    # 8.4 Драгоценные металлы и драгоценные камни.
    GOODS_IN_CIRCULATION_PRECIOUS_METALS_AND_GEMSTONES = "GOODS_IN_CIRCULATION_PRECIOUS_METALS_AND_GEMSTONES"
    # 8.5 Ювелирные и другие изделия из драгоценных металлов или драгоценных камней.
    GOODS_IN_CIRCULATION_JEWELRY_AND_OTHER_PRODUCTS_OF_PRECIOUS_METALS_OR_STONES = (
        "GOODS_IN_CIRCULATION_JEWELRY_AND_OTHER_PRODUCTS_OF_PRECIOUS_METALS_OR_STONES"
    )
    # 8.6 Строительные и отделочные материалы, металлопродукция.
    GOODS_IN_CIRCULATION_BUILDING_AND_FINISHING_MATERIALS_METAL_PRODUCTS = (
        "GOODS_IN_CIRCULATION_BUILDING_AND_FINISHING_MATERIALS_METAL_PRODUCTS"
    )
    # 8.7 Транспортные средства, оборудование, комплектующие и запасные части к ним.
    GOODS_IN_CIRCULATION_VEHICLES_EQUIPMENT_COMPONENTS_AND_SPARE_PARTS = (
        "GOODS_IN_CIRCULATION_VEHICLES_EQUIPMENT_COMPONENTS_AND_SPARE_PARTS"
    )
    # 8.8 Текстиль и изделия текстильные.
    GOODS_IN_CIRCULATION_TEXTILE_AND_TEXTILE_PRODUCTS = "GOODS_IN_CIRCULATION_TEXTILE_AND_TEXTILE_PRODUCTS"
    # 8.9 Топливно-энергетические ресурсы.
    GOODS_IN_CIRCULATION_FUEL_AND_ENERGY_RESOURCES = "GOODS_IN_CIRCULATION_FUEL_AND_ENERGY_RESOURCES"
    # 8.10 Вещества химические и продукты химические.
    GOODS_IN_CIRCULATION_CHEMICAL_SUBSTANCES_AND_CHEMICAL_PRODUCTS = (
        "GOODS_IN_CIRCULATION_CHEMICAL_SUBSTANCES_AND_CHEMICAL_PRODUCTS"
    )
    # 8.11 Средства лекарственные и материалы, применяемые в медицинских целях.
    GOODS_IN_CIRCULATION_MEDICINES_AND_MATERIALS_USED_FOR_MEDICAL_PURPOSES = (
        "GOODS_IN_CIRCULATION_MEDICINES_AND_MATERIALS_USED_FOR_MEDICAL_PURPOSES"
    )
    # 8.99 Иное.
    GOODS_IN_CIRCULATION_OTHER = "GOODS_IN_CIRCULATION_OTHER"

    # 9 Будущие урожаи.
    # 9.1 Зерновые культуры.
    FUTURE_CROPS_GRAIN_CROPS = "FUTURE_CROPS_GRAIN_CROPS"
    # 9.2 Зернобобовые культуры.
    FUTURE_CROPS_LEGUMINOUS_CROPS = "FUTURE_CROPS_LEGUMINOUS_CROPS"
    # 9.3 Масличные культуры.
    FUTURE_CROPS_OIL_CROPS = "FUTURE_CROPS_OIL_CROPS"
    # 9.4 Технические культуры.
    FUTURE_CROPS_INDUSTRIAL_CROPS = "FUTURE_CROPS_INDUSTRIAL_CROPS"
    # 9.5 Кормовые культуры.
    FUTURE_CROPS_FEED_CROPS = "FUTURE_CROPS_FEED_CROPS"
    # 9.6 Бахчевые культуры.
    FUTURE_CROPS_VEGETABLE_CROPS = "FUTURE_CROPS_VEGETABLE_CROPS"
    # 9.7 Картофель.
    FUTURE_CROPS_POTATO = "FUTURE_CROPS_POTATO"
    # 9.8 Овощи.
    FUTURE_CROPS_VEGETABLES = "FUTURE_CROPS_VEGETABLES"
    # 9.9 Многолетние насаждения.
    FUTURE_CROPS_PERENNIAL_PLANTINGS = "FUTURE_CROPS_PERENNIAL_PLANTINGS"
    # 9.99 Иное.
    FUTURE_CROPS_OTHER = "FUTURE_CROPS_OTHER"

    # 10 Аффинированные драгоценные металлы в слитках.
    # 10.1 Золото.
    REFINED_PRECIOUS_METAL_BARS_GOLD = "REFINED_PRECIOUS_METAL_BARS_GOLD"
    # 10.2 Серебро.
    REFINED_PRECIOUS_METAL_BARS_SILVER = "REFINED_PRECIOUS_METAL_BARS_SILVER"
    # 10.3 Платина.
    REFINED_PRECIOUS_METAL_BARS_PLATINUM = "REFINED_PRECIOUS_METAL_BARS_PLATINUM"
    # 10.4 Палладий.
    REFINED_PRECIOUS_METAL_BARS_PALLADIUM = "REFINED_PRECIOUS_METAL_BARS_PALLADIUM"

    # 11 Исключительные права на результат интеллектуальной деятельности.
    # 11.1 Произведение науки, литературы или искусства.
    INTELLECTUAL_PROPERTY_RIGHTS_SCIENCE_LITERATURE_OR_ART_WORK = (
        "INTELLECTUAL_PROPERTY_RIGHTS_SCIENCE_LITERATURE_OR_ART_WORK"
    )
    # 11.2 Программа для электронных вычислительных машин (ЭВМ).
    INTELLECTUAL_PROPERTY_RIGHTS_COMPUTER_PROGRAM_FOR_ELECTRONIC_COMPUTING_MACHINES = (
        "INTELLECTUAL_PROPERTY_RIGHTS_COMPUTER_PROGRAM_FOR_ELECTRONIC_COMPUTING_MACHINES"
    )
    # 11.3 База данных.
    INTELLECTUAL_PROPERTY_RIGHTS_DATABASE = "INTELLECTUAL_PROPERTY_RIGHTS_DATABASE"
    # 11.4 Изобретение.
    INTELLECTUAL_PROPERTY_RIGHTS_INVENTION = "INTELLECTUAL_PROPERTY_RIGHTS_INVENTION"
    # 11.5 Секрет производства (ноу-хау).
    INTELLECTUAL_PROPERTY_RIGHTS_TRADE_SECRET_KNOW_HOW = (
        "INTELLECTUAL_PROPERTY_RIGHTS_TRADE_SECRET_KNOW_HOW"  # nosec: B105
    )
    # 11.6 Товарный знак или знак обслуживания.
    INTELLECTUAL_PROPERTY_RIGHTS_TRADEMARK_OR_SERVICE_MARK = "INTELLECTUAL_PROPERTY_RIGHTS_TRADEMARK_OR_SERVICE_MARK"
    # 11.99 Иное.
    INTELLECTUAL_PROPERTY_RIGHTS_OTHER = "INTELLECTUAL_PROPERTY_RIGHTS_OTHER"

    # 12 Права по договору банковского счета.
    # 12.1 Права в отношении всей денежной суммы на залоговом счете в любой момент в течение времени действия
    # договора залога.
    BANK_ACCOUNT_CONTRACTUAL_RIGHTS_RIGHTS_TO_THE_ENTIRE_AMOUNT_ON_THE_PLEDGE_ACCOUNT = (
        "BANK_ACCOUNT_CONTRACTUAL_RIGHTS_RIGHTS_TO_THE_ENTIRE_AMOUNT_ON_THE_PLEDGE_ACCOUNT"
    )
    # 12.2 Права в отношении денежной суммы, размер которой указан в договоре залога.
    BANK_ACCOUNT_CONTRACTUAL_RIGHTS_RIGHTS_TO_THE_SPECIFIED_AMOUNT_ON_THE_PLEDGE_ACCOUNT = (
        "BANK_ACCOUNT_CONTRACTUAL_RIGHTS_RIGHTS_TO_THE_SPECIFIED_AMOUNT_ON_THE_PLEDGE_ACCOUNT"
    )

    # 13 Доля в уставном капитале общества с ограниченной ответственностью.
    # 13.1 Доля в уставном капитале общества с ограниченной ответственностью.
    SHARE_IN_THE_CHARTER_CAPITAL_OF_LIMITED_LIABILITY_COMPANY = (
        "SHARE_IN_THE_CHARTER_CAPITAL_OF_LIMITED_LIABILITY_COMPANY"
    )

    # 14 Векселя.
    # 14.1 Вексель.
    BILLS_OF_EXCHANGE_PROMISSORY_NOTE = "BILLS_OF_EXCHANGE_PROMISSORY_NOTE"

    # 15 Эмиссионные ценные бумаги.
    # 15.1 Акция.
    DEBT_INSTRUMENTS_STOCK = "DEBT_INSTRUMENTS_STOCK"
    # 15.2 Облигация.
    DEBT_INSTRUMENTS_BOND = "DEBT_INSTRUMENTS_BOND"
    # 15.3 Опцион эмитента.
    DEBT_INSTRUMENTS_ISSUER_OPTION = "DEBT_INSTRUMENTS_ISSUER_OPTION"
    # 15.4 Депозитарная расписка.
    DEBT_INSTRUMENTS_CERTIFICATE_OF_DEPOSIT = "DEBT_INSTRUMENTS_CERTIFICATE_OF_DEPOSIT"
    # 15.99 Иное.
    DEBT_INSTRUMENTS_OTHER = "DEBT_INSTRUMENTS_OTHER"

    # 16 Инвестиционные паи.
    # 16.1 Инвестиционный пай.
    INVESTMENT_UNITS_INVESTMENT_UNIT = "INVESTMENT_UNITS_INVESTMENT_UNIT"

    # 17 Ипотечные сертификаты участия.
    # 17.1 Ипотечный сертификат участия.
    MORTGAGE_CERTIFICATES_OF_PARTICIPATION_MORTGAGE_CERTIFICATE_OF_PARTICIPATION = (
        "MORTGAGE_CERTIFICATES_OF_PARTICIPATION_MORTGAGE_CERTIFICATE_OF_PARTICIPATION"
    )

    # 18 Прочие ценные бумаги.
    # 18.1 Закладная.
    OTHER_SECURITIES_MORTGAGE_CERTIFICATE = "OTHER_SECURITIES_MORTGAGE_CERTIFICATE"
    # 18.2 Депозитный сертификат.
    OTHER_SECURITIES_DEPOSIT_CERTIFICATE = "OTHER_SECURITIES_DEPOSIT_CERTIFICATE"
    # 18.3 Сберегательный сертификат.
    OTHER_SECURITIES_SAVINGS_CERTIFICATE = "OTHER_SECURITIES_SAVINGS_CERTIFICATE"
    # 18.99 Иное.
    OTHER_SECURITIES_OTHER = "OTHER_SECURITIES_OTHER"

    # 19 Прочие имущественные права.
    # 19.1 Право аренды или пользования.
    OTHER_PROPERTY_RIGHTS_LEASE_OR_USE_RIGHT = "OTHER_PROPERTY_RIGHTS_LEASE_OR_USE_RIGHT"
    # 19.2 Права участника долевого строительства.
    OTHER_PROPERTY_RIGHTS_RIGHTS_OF_DISTRIBUTED_DEVELOPMENT_PARTICIPANT = (
        "OTHER_PROPERTY_RIGHTS_RIGHTS_OF_DISTRIBUTED_DEVELOPMENT_PARTICIPANT"
    )
    # 19.3 Имущественные права на недвижимое имущество.
    OTHER_PROPERTY_RIGHTS_PROPERTY_RIGHTS_TO_REAL_ESTATE = "OTHER_PROPERTY_RIGHTS_PROPERTY_RIGHTS_TO_REAL_ESTATE"
    # 19.4 Право требования.
    OTHER_PROPERTY_RIGHTS_CLAIM_RIGHT = "OTHER_PROPERTY_RIGHTS_CLAIM_RIGHT"
    # 19.99 Иное.
    OTHER_PROPERTY_RIGHTS_OTHER = "OTHER_PROPERTY_RIGHTS_OTHER"

    # 20 Прочие движимые вещи.
    # 20.1 Животное, индивидуально определенное.
    OTHER_MOVABLE_OBJECTS_INDIVIDUALLY_DEFINED_ANIMAL = "OTHER_MOVABLE_OBJECTS_INDIVIDUALLY_DEFINED_ANIMAL"
    # 20.2 Монета, содержащая драгоценные металлы.
    OTHER_MOVABLE_OBJECTS_PRECIOUS_METAL_CONTENT_COIN = "OTHER_MOVABLE_OBJECTS_PRECIOUS_METAL_CONTENT_COIN"
    # 20.3 Предмет бытового использования (бытовая техника, мебель и другое).
    OTHER_MOVABLE_OBJECTS_HOUSEHOLD_USE_ITEM = "OTHER_MOVABLE_OBJECTS_HOUSEHOLD_USE_ITEM"
    # 20.99 Иное.
    OTHER_MOVABLE_OBJECTS_OTHER = "OTHER_MOVABLE_OBJECTS_OTHER"

    # 21 Все имущество залогодателя.
    ALL_PROPERTY_OF_THE_PLEDGER = "ALL_PROPERTY_OF_THE_PLEDGER"


class LegalJsonField(Constant):
    """Поля компаний в json"""

    INN: Final[str] = "i"
    OGRN: Final[str] = "o"
    FULL_NAME: Final[str] = "n"
    SHORT_NAME: Final[str] = "c"
    REGISTRATION_DATE: Final[str] = "r"

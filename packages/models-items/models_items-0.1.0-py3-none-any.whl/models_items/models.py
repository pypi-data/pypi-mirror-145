import yaml
from flask_login import UserMixin
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    Numeric,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

cfg = yaml.safe_load(open("config.yaml"))

Base = declarative_base()


def db_connect():
    """Performs database connection using database settings from config.yaml
    Returns sqlalchemy engine instance
    """
    engine = create_engine(cfg["db_connection_string"])
    Base.metadata.bind = engine
    return engine


def create_table(engine):
    Base.metadata.create_all(engine, checkfirst=True)


def get_session():
    """Initializes database connection and sessionmaker

    Returns:
        session: Instantiated Session object for database
    """
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


"""**************************************************************************
Brand Tables
**************************************************************************"""


class NLBrand(Base):
    __tablename__ = "nl_brand"
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    url = Column("url", String(150))
    wm_id = Column(Integer, ForeignKey("wm_brand.id"), nullable=True)
    ff_id = Column(Integer, ForeignKey("ff_brand.id"), nullable=True)
    gm_id = Column(Integer, ForeignKey("gm_brand.id"), nullable=True)
    products = relationship(
        "NLProduct", backref="nl_brand"
    )  # One brand to many products


class FFBrand(Base):
    __tablename__ = "ff_brand"
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    url = Column("url", String(150))
    wm_id = Column(Integer, ForeignKey("wm_brand.id"), nullable=True)
    nl_id = Column(Integer, ForeignKey("nl_brand.id"), nullable=True)
    gm_id = Column(Integer, ForeignKey("gm_brand.id"), nullable=True)
    products = relationship(
        "FFProduct", backref="ff_brand"
    )  # One brand to many products


class GMBrand(Base):
    __tablename__ = "gm_brand"
    id = Column(Integer, primary_key=True)
    name = Column("name", String(60))
    url = Column("url", String(150))
    nl_id = Column(Integer, ForeignKey("nl_brand.id"), nullable=True)
    ff_id = Column(Integer, ForeignKey("ff_brand.id"), nullable=True)
    wm_id = Column(Integer, ForeignKey("wm_brand.id"), nullable=True)
    products = relationship(
        "GMProduct", backref="gm_brand"
    )  # One brand to many products


class WMBrand(Base):
    __tablename__ = "wm_brand"
    id = Column(Integer, primary_key=True)
    name = Column("name", String(60))
    url = Column("url", String(150))
    nl_id = Column(Integer, ForeignKey("nl_brand.id"), nullable=True)
    ff_id = Column(Integer, ForeignKey("ff_brand.id"), nullable=True)
    gm_id = Column(Integer, ForeignKey("gm_brand.id"), nullable=True)
    products = relationship(
        "WMProduct", backref="wm_brand"
    )  # One brand to many products


"""**************************************************************************
Product Tables
**************************************************************************"""


class NLProduct(Base):
    __tablename__ = "nl_product"
    id = Column(Integer, primary_key=True)
    code = Column("code", String(30), unique=True)
    name = Column("name", String(150))
    brand_id = Column(Integer, ForeignKey("nl_brand.id"))  # Many products to one brand
    variant = Column("variant", String(60))
    # base_product_id = Column(Integer)
    url = Column("url", String(200))
    ff_id = Column(Integer, ForeignKey("ff_product.id"), nullable=True)
    wm_id = Column(Integer, ForeignKey("wm_product.id"), nullable=True)
    gm_id = Column(Integer, ForeignKey("gm_product.id"), nullable=True)
    historical_prices = relationship(
        "NLHistoricalPrice", backref="nl_product"
    )  # One product to many historical prices


class FFProduct(Base):
    __tablename__ = "ff_product"
    id = Column(Integer, primary_key=True)
    code = Column("code", String(30), unique=True)
    name = Column("name", String(150))
    brand_id = Column(Integer, ForeignKey("ff_brand.id"))  # Many products to one brand
    variant = Column("variant", String(60))
    url = Column("url", String(200))
    nl_id = Column(Integer, ForeignKey("nl_product.id"), nullable=True)
    wm_id = Column(Integer, ForeignKey("wm_product.id"), nullable=True)
    gm_id = Column(Integer, ForeignKey("gm_product.id"), nullable=True)
    historical_prices = relationship(
        "FFHistoricalPrice", backref="ff_product"
    )  # One product to many historical prices


class GMProduct(Base):
    __tablename__ = "gm_product"
    id = Column(Integer, primary_key=True)
    code = Column("code", String(30), unique=True)
    name = Column("name", String(150))
    brand_id = Column(Integer, ForeignKey("gm_brand.id"))  # Many products to one brand
    variant = Column("variant", String(60))
    url = Column("url", String(200))
    nl_id = Column(Integer, ForeignKey("nl_product.id"), nullable=True)
    ff_id = Column(Integer, ForeignKey("ff_product.id"), nullable=True)
    wm_id = Column(Integer, ForeignKey("wm_product.id"), nullable=True)
    historical_prices = relationship(
        "GMHistoricalPrice", backref="gm_product"
    )  # One product to many historical prices


class WMProduct(Base):
    __tablename__ = "wm_product"
    id = Column(Integer, primary_key=True)
    code = Column("code", String(30), unique=True)
    name = Column("name", String(150))
    brand_id = Column(Integer, ForeignKey("wm_brand.id"))  # Many products to one brand
    variant = Column("variant", String(50))
    url = Column("url", String(200))
    nl_id = Column(Integer, ForeignKey("nl_product.id"), nullable=True)
    ff_id = Column(Integer, ForeignKey("ff_product.id"), nullable=True)
    gm_id = Column(Integer, ForeignKey("gm_product.id"), nullable=True)
    historical_prices = relationship(
        "WMHistoricalPrice", backref="wm_product"
    )  # One product to many historical prices


"""**************************************************************************
Current Price Tables
**************************************************************************"""


class NLCurrentPrice(Base):
    __tablename__ = "nl_current_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("nl_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


class FFCurrentPrice(Base):
    __tablename__ = "ff_current_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("ff_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


class GMCurrentPrice(Base):
    __tablename__ = "gm_current_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("gm_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


class WMCurrentPrice(Base):
    __tablename__ = "wm_current_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("wm_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


"""**************************************************************************
Historical Price Tables
**************************************************************************"""


class NLHistoricalPrice(Base):
    __tablename__ = "nl_historical_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("nl_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


class FFHistoricalPrice(Base):
    __tablename__ = "ff_historical_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("ff_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


class GMHistoricalPrice(Base):
    __tablename__ = "gm_historical_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("gm_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


class WMHistoricalPrice(Base):
    __tablename__ = "wm_historical_price"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("wm_product.id"))
    time_stamp = Column("time_stamp", DateTime)
    retail_price = Column("retail_price", Numeric(scale=2, asdecimal=True))
    on_sale = Column("on_sale", Boolean)
    current_price = Column("current_price", Numeric(scale=2, asdecimal=True))
    in_stock = Column("in_stock", Boolean)


"""**************************************************************************
Best Selling Tables
**************************************************************************"""


class NLBestSelling(Base):
    __tablename__ = "nl_best_selling"
    id = Column(Integer, primary_key=True)
    product_id = Column("product_id", ForeignKey("nl_product.id"))
    category = Column("category", String(50))
    ranking = Column("ranking", Integer)
    time_stamp = Column("time_stamp", DateTime)


class FFBestSelling(Base):
    __tablename__ = "ff_best_selling"
    id = Column(Integer, primary_key=True)
    product_id = Column("product_id", ForeignKey("ff_product.id"))
    category = Column("category", String(50))
    ranking = Column("ranking", Integer)
    time_stamp = Column("time_stamp", DateTime)


"""**************************************************************************
Highest Rated Tables
**************************************************************************"""


class NLHighestRated(Base):
    __tablename__ = "nl_highest_rated"
    id = Column(Integer, primary_key=True)
    product_id = Column("product_id", ForeignKey("nl_product.id"))
    category = Column("category", String(50))
    ranking = Column("ranking", Integer)
    rating = Column("rating", Float)
    review_count = Column("review_count", Integer)
    time_stamp = Column("time_stamp", DateTime)


class FFHighestRated(Base):
    __tablename__ = "ff_highest_rated"
    id = Column(Integer, primary_key=True)
    product_id = Column("product_id", ForeignKey("ff_product.id"))
    category = Column("category", String(50))
    ranking = Column("ranking", Integer)
    rating = Column("rating", Float)
    review_count = Column("review_count", Integer)
    time_stamp = Column("time_stamp", DateTime)


# TODO: Normalise wm_product table to use time_stamp from this table?
class WMPriceFileInfo(Base):
    """Table containing wm price file related information to only update wm
    tables when the file has been updated"""

    __tablename__ = "wm_price_file_info"
    id = Column(Integer, primary_key=True)
    hash = Column("hash", LargeBinary(16), unique=True)
    total_products = Column(Integer)
    time_stamp = Column("time_stamp", DateTime)


class BrandUrlDict(Base):
    """Table containing Json of brand:url key value pairs
    Used by product spiders to store brands"""

    __tablename__ = "brand_url_dict"
    id = Column(Integer, primary_key=True)
    website = Column("website", String(30))
    data = Column(JSON)


class RegisteredUser(UserMixin, Base):
    """Table used to store registered users for authentication
    with username and password hash"""

    __tablename__ = "registered_user"
    id = Column(Integer, primary_key=True)
    username = Column("username", String(15), unique=True, nullable=False)
    password = Column("password", String(128))


# class ScrapeHistory(Base):
#         """Table containing date records of each scraping run"""

#     __tablename__ = "scrape_history"
#     id = Column(Integer, primary_key=True)
#     time_stamp = Column("time_stamp", DateTime)

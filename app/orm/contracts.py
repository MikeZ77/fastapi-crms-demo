from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

import app.domain.contracts as model

mapper_registry = registry()

contracts = Table(
    "contracts",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version", Integer, nullable=False, default=1),
)

licenses = Table(
    "licenses",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("contract_id", ForeignKey("contracts.id")),
    Column("studio", String(255), nullable=False),
    Column("start_date", Date, nullable=False),
    Column("end_date", Date, nullable=False),
)

offers = Table(
    "offers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(25), nullable=False, unique=True, index=True),
    Column("price", Float, nullable=False),
    Column("start_date", Date, nullable=False),
    Column("end_date", Date, nullable=False),
)


assigned_offers = Table(
    "assingned_offers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("license_id", ForeignKey("licenses.id")),
    Column("offer_id", ForeignKey("offers.id")),
)


# Resources:
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship


def start_mappers():
    # Maps our domain models to our database tables using the imperative approach

    # Maps our Offers domain model 1:1 with our offers table
    offer_map = mapper_registry.map_imperatively(model.Offers, offers)
    # When we use a FK, we need to define the type of relationship
    # licenses and offers have a N:N relationship
    license_map = mapper_registry.map_imperatively(
        model.Licenses,
        licenses,
        properties={
            # licenses has the attribute _offers which holds a set of Offers
            # secondary is the association table that holds the relationship between licenses and offers
            # if we wanted offers to have a set of Licenses, we would pass back_populates
            "_offers": relationship(
                offer_map, secondary=assigned_offers, collection_class=set
            )
        },
    )
    # contracts has a 1:N relationship with licenses
    mapper_registry.map_imperatively(
        model.Contracts,
        contracts,
        properties={"licenses": relationship(license_map, collection_class=list)},
    )

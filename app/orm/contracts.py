from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

import app.domain.contracts as model
from app.orm import mapper_registry

contracts = Table(
    "contracts",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("contract_id", UUID(as_uuid=True), unique=True, nullable=False),
    Column("version", Integer, nullable=False, default=1),
    Column("a_new_column", String, nullable=True),
    Index("ix_contracts_contract_id", "contract_id"),
)

licenses = Table(
    "licenses",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("license_id", UUID(as_uuid=True), unique=True, nullable=False),
    Column("contract_id", ForeignKey("contracts.contract_id")),
    Column("studio", String(255), nullable=False),
    Column("start_date", DateTime(timezone=True), nullable=False),
    Column("end_date", DateTime(timezone=True), nullable=False),
    Index("ix_licenses_license_id", "license_id"),
)

offers = Table(
    "offers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(25), nullable=False, unique=True, index=True),
    Column("price", Float, nullable=False),
    Column("start_date", DateTime(timezone=True), nullable=False),
    Column("end_date", DateTime(timezone=True), nullable=False),
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
    offer_map = mapper_registry.map_imperatively(model.Offer, offers)
    # When we use a FK, we need to define the type of relationship
    # licenses and offers have a N:N relationship
    license_map = mapper_registry.map_imperatively(
        model.License,
        licenses,
        properties={
            # licenses has the attribute _offers which holds a set of Offers
            # secondary is the association table that holds the relationship between licenses and offers
            # if we wanted offers to have a set of Licenses, we would pass back_populates
            "end_date_": licenses.columns.end_date,
            "_offers": relationship(
                offer_map, secondary=assigned_offers, collection_class=set
            ),
        },
    )
    # contracts has a 1:N relationship with licenses
    mapper_registry.map_imperatively(
        model.Contract,
        contracts,
        properties={"licenses": relationship(license_map, collection_class=list)},
    )


# NOTE:
# Because we are doing imperative mapping and not declarative mapping, we create the uuid
# inside the class.
#
# as_uuid=True means that sqlalchemy will convert the uuid back to a python uuid object
#
# With the declarative approach, you would probably do something like this:
# Column("contract_id", UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
#
# If you wanted the database to generate the uuid, would would use server_default

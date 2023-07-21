import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create the SQLite database file
db_file = "beer_inventory.db"
if os.path.exists(db_file):
    os.remove(db_file)

# Create SQLAlchemy engine and base
engine = create_engine(f"sqlite:///{db_file}", echo=False)
Base = declarative_base()

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    beer_id = Column(Integer, ForeignKey('beers.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    name = Column(String)

class Beers(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    style = Column(String)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    stores = relationship("Store", back_populates="beer")

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    beers = relationship("Beers", back_populates="brand")

Base.metadata.create_all(engine)

# Define the CLI application
class BeerInventoryApp:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def display_all_stores(self):
        print("All Stores:")
        for store in self.session.query(Store).all():
            print(f"{store.id}: {store.name}")

        store_id = int(input("Select a store ID to see its inventory (or enter 0 to go back): "))
        if store_id == 0:
            return

        store = self.session.query(Store).filter_by(id=store_id).first()
        if store:
            print(f"\nInventory for {store.name}:")
            for beer in store.beer:
                print(f"{beer.name} - {beer.brand.name}")
        else:
            print("Invalid store ID.")

    def display_all_beers(self):
        print("All Beers:")
        for beer in self.session.query(Beers).all():
            print(f"{beer.name} - {beer.brand.name}")
            for store in beer.stores:
                print(f"  Found in store: {store.name}")

    def display_all_brands(self):
        print("All Brands:")
        for brand in self.session.query(Brand).all():
            print(f"{brand.id}: {brand.name}")

        brand_id = int(input("Select a brand ID to see its beers and stores (or enter 0 to go back): "))
        if brand_id == 0:
            return

        brand = self.session.query(Brand).filter_by(id=brand_id).first()
        if brand:
            print(f"\nBeers of {brand.name}:")
            for beer in brand.beers:
                print(f"{beer.name} - Found in stores:")
                for store in beer.stores:
                    print(f"  {store.name}")
        else:
            print("Invalid brand ID.")

    def add_beer(self):
        beer_name = input("Enter the name of the beer: ")
        beer_style = input("Enter the style of the beer: ")
        brand_name = input("Enter the name of the brand: ")
        store_name = input("Enter the name of the store: ")

        brand = self.session.query(Brand).filter_by(name=brand_name).first()
        if not brand:
            brand = Brand(name=brand_name)
            self.session.add(brand)

        beer = Beers(name=beer_name, style=beer_style, brand=brand)
        store = Store(name=store_name, beer=beer, brand=brand)
        self.session.add_all([beer, store])
        self.session.commit()
        print(f"\nSuccessfully added '{beer_name}' of brand '{brand_name}' to store '{store_name}'.")

    def display_menu(self):
        while True:
            print("\nBeer Inventory App Menu:")
            print("1) Display All Stores")
            print("2) Display All Beers")
            print("3) Display All Brands")
            print("4) Add Beer")
            print("5) Quit program")

            choice = int(input("Enter your choice (1-5): "))

            if choice == 1:
                self.display_all_stores()
            elif choice == 2:
                self.display_all_beers()
            elif choice == 3:
                self.display_all_brands()
            elif choice == 4:
                self.add_beer()
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = BeerInventoryApp()
    app.display_menu()
import random
from faker import Faker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Store, Beer, Inventory

engine = create_engine("sqlite:///beer_inventory.db")
Session = sessionmaker(bind = engine)
session = Session()

store_list = ['7-Eleven', 'Ralphs', 'Costco', 'Walmart', 'Liquor Mart']

fake = Faker()

if __name__ == '__main__':
    session.query(Store).delete()
    session.query(Beer).delete()
    session.query(Inventory).delete()

    beer1 = Beer(name="Sculpin", brand="Ballast Point", style="IPA")
    beer2 = Beer(name="Longfin", brand="Ballast Point", style="Lager")
    beer3 = Beer(name="WestCoast IPA", brand="Green Flash", style="IPA")
    beer4 = Beer(name="Corona Extra", brand="Corona", style="Pale Lager")
    beer5 = Beer(name="Mango Cart", brand="Golden Road", style="Wheat Ale")
    beer6 = Beer(name="Michelob Ultra", brand="Michelob", style="Lager")
    beer7 = Beer(name="Grapefruit Solis", brand="Mike Hess", style="IPA")
    beer8 = Beer(name=".394", brand="Alesmith", style="IPA")
    beer9 = Beer(name="Kirin Ichiban", brand="Kirin", style="Pale Lager")

    session.add_all([beer1, beer2, beer3, beer4, beer5, beer6, beer7, beer8, beer9])
    session.commit()

    beer_store = []
    for store in store_list:
        stores = Store(
             name = store,        
        )
        session.add(stores)
        session.commit()
        beer_store.append(stores)

    all_beers = []
    all_beers.extend([beer1, beer2, beer3, beer4, beer5, beer6, beer7, beer8, beer9])
    for _ in range (9):
        beer = Beer(
             name = fake.word(),
             brand = fake.word(),
             style = fake.last_name()
            )

    session.add(beer)
    session.commit()
    all_beers.append(beer)

    store_inventory = []
    for store in beer_store:
            for _ in range(random.randint(10,15)):
                 item = Inventory(
                      beer_id = random.choice(all_beers).id,
                      store_id = store.id
                 )
                 session.add(item)
                 store_inventory.append(item)
    session.commit()




from db.models import Base, Store, Beer, Inventory
from prettytable import PrettyTable
import click

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///beer_inventory.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def stores_table(stores):
    table = PrettyTable()
    table.title = "Stores"
    table.field_names = ['id', 'Store Name']
    for store in stores:
        table.add_row([
            store.id,
            store.name
        ])

    print(table)

def create_inventory(store_id):
    store_list = ['7-Eleven', 'Ralphs', 'Costco', 'Walmart', 'Liquor Mart']
    store_name = store_list[int(store_id)-1]

    beer_list = session.query(Inventory).filter_by(store_id=store_id)

    store_inventory = [session.query(Beer).get(beer.beer_id) for beer in beer_list]
    
    table = PrettyTable()

    table.title = f"{store_name}"

    table.field_names = ['name', 'brand', 'style']
    for beer in store_inventory:
        table.add_row([
            beer.name,
            beer.brand,
            beer.style
        ])

    print(table)

def cli_start_menu():
    print('''
    1) Browse Store Inventories
    2) Search by Beer Name
    3) Search by Beer Brand
    4) Search by Beer Style
    5) Exit Program
          ''')
    
def cli_start():
    choice = 0
    cli_start_menu()
    while choice != 5:
        
        if choice == 1:
            browse_by_store()

        if choice == 2:
            search_by_beer()
        
        if choice == 3:
            search_by_brand()

        if choice == 4:
            search_by_style()
        
        choice = click.prompt('Enter your selection', type=int)
    print('Exiting program...')

def browse_by_store():
    stores = session.query(Store)
    stores_table(stores)

    choice = click.prompt('Enter store ID to view inventory or press \"X\" to return to the previous menu')
    try:
        if choice.lower() == 'x':
            cli_start_menu()
        else:
            store_id = int(choice) 
            if store_id in [store.id for store in stores]:
                    create_inventory(store_id)
                    cli_start_menu()
            else:
                print('Invalid Store ID. Please select a valid Store ID. ')
                browse_by_store()
    except ValueError:
        print('Invalid Input, please select a Store ID.')

def search_by_beer():
    name = click.prompt('Enter name of beer')
    beers = session.query(Beer).filter_by(name=name).all()
    if not beers:
        print(' * * No results matched search criteria... * *')
        print('* * Returning to main menu * *')
        
    else:
        table = PrettyTable()
        table.title = f'Search Results for "{name}"'
        table.field_names = ['name', 'brand', 'style', ]
        for beer in beers:
            table.add_row([
            beer.name,
            beer.brand,
            beer.style
        ])
        print(table)
        print('Search completed.')
        cli_start_menu()

def search_by_brand():
    brand_name = click.prompt('Enter name of brand/brewery')
    brand_search = session.query(Beer).filter_by(brand=brand_name).all()
    if not brand_search:
        print('* * No brands matched search criteria... * *')
        print('* * Returning to main menu * *')
        cli_start_menu()
    else:
        table = PrettyTable()
        table.title = f"Search Results for {brand_name}"
        table.field_names = ['brand', 'name', 'style']
        for brand in brand_search:
            table.add_row([
                brand.brand,
                brand.name,
                brand.style
            ])
        print(table)
        print('Search completed.')
        

def search_by_style():
    style_name = click.prompt('Enter style of beer')
    style_search = session.query(Beer).filter_by(style=style_name).all()
    if not style_search:
        print('* * No results matched search criteria... * *')
        print('* * Returning to main menu * *')
        cli_start_menu()
    else:
        table = PrettyTable()
        table.title = f"Search Results for {style_name}"
        table.field_names = ['style', 'name', 'brand']
        for style in style_search:
            table.add_row([
                style.style,
                style.name,
                style.brand
            ])
        print(table)
        print('Search completed.')
          

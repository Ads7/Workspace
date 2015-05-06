from flask import Flask, render_template, request, redirect, url_for,flash, jsonify 
app = Flask(__name__) 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Making an Api EndPoint (Get Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)
     
#Web app routing
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()   
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        
        return redirect('/')
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:id>/edit/', methods=['GET','POST'])
def editRestaurant(id):
    editRestaurant = session.query(Restaurant).filter_by(id = id).one()
    if request.method == 'POST':
       if request.form['name']:
           editRestaurant.name = request.form['name']
           session.add(editRestaurant)
           session.commit()
           return redirect('/')
           
    else:
        return render_template('editrestaurant.html', restaurant = editRestaurant)   

@app.route('/restaurants/<int:id>/delete/', methods=['GET','POST']) 
def deleteRestaurant(id):
    deletedItem = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
      
        return redirect('/')
    else:
        return render_template('deleterestaurant.html', item = deletedItem )

    
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenuItem = MenuItem(name = request.form['name'],restaurant_id = restaurant_id)
        session.add(newMenuItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id ))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id) 

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['POST', 'GET'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Menu Item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id ))           
    else:
        return render_template('editmenuitem.html', restaurant_id= restaurant_id, menu_id= menu_id, i=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Menu item deleted")
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', item = deletedItem )



if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

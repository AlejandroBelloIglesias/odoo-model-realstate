# Real state module
This module allows to register, edit and delete properties, owners and renters.
Properties can be rented or sold allowing to register the renters / new owner and the rent / sale itself.

Available features:
- Add, edit, delete properties
- Add, edit, delete owners
- Add, edit, delete renters
- Rent a property
- Sell a property

## Owner
The person who owns properties.
This model inherit from res.partner.
Owners can be created by their own without any relation to the properties yet.

## Renter
The person who rents properties.
This model inherit from res.partner.
Renters can only be created, updated and deleted when creating, updating or deleting a property.
A renter can only live in one property at a time.

## Property
The property that can be rented or sold.
Properties have their own attributes like address, area, owner, renter, price, etc.
All properties must have an owner and if they are for rent, it will have renters.

# Future possible features
New model 'Contract' to register the rent / sale of a property.
    - Rules for the rent like allowing pets, allowing smoking, etc.
    - Payment method like cash, credit card, etc.
    - Payment terms like monthly, yearly, etc.
    - Payment date, amount, etc.

More information about the property model:
    - Number of bedrooms, bathrooms, etc.
    - Balcony, garden, etc.



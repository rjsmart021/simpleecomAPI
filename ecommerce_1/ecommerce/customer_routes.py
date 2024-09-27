from flask import jsonify, request

from ecommerce import app
from ecommerce.models import Customer
from ecommerce import db
from ecommerce.schemas import CustomerSchema

customer_schema = CustomerSchema()


@app.route('/customers', methods=['POST'])
def add_customer():
    
    try:
        data = request.get_json()
        errors = customer_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        email = data.get("email")
        phone_number = data.get("phone_number")
        # Check if the customer already exists based on email or phone number
        existing_customer = Customer.query.filter(
            (Customer.email == email) | (Customer.phone_number == phone_number)
        ).first()

        if existing_customer:
            return jsonify({"message": f"Customer already existed"})
        customer = Customer(customer_name=data["customer_name"], email=data["email"],
                            phone_number=data["phone_number"])

        # Add the new customer to the database
        db.session.add(customer)
        db.session.commit()

        return jsonify({"message": "Customer added successfully"})
    except Exception as e:
        return jsonify({"Error": f"Customer not added. Error {e}"})


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
   
    try:
        customer = Customer.query.get(customer_id)

        if customer:
            customer_data = {
                "customer_id": customer.customer_id,
                "customer_name": customer.customer_name,
                "email": customer.email,
                "phone_number": customer.phone_number
            }
            return jsonify(customer_data)
        else:
            return jsonify({"message": "Customer not found"})

    except Exception as e:
        print(f"Error in getting customer. Error Message: {e}")
        return jsonify(
            {"message": f"Error while fetching customer with ID: {customer_id}. Error: {e}"})


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_user(customer_id):

    try:
        customer = Customer.query.get(customer_id)

        if customer:
            data = request.get_json()
            error = customer_schema.validate(data)
            if error:
                return jsonify(error), 400
            customer.customer_name = data.get('customer_name', customer.customer_name)
            customer.email = data.get('email', customer.email)
            customer.phone_number = data.get('phone_number', customer.phone_number)

            db.session.commit()
            return jsonify({"message": "Customer updated successfully"})
        else:
            return jsonify({"message": "Customer Not Found!!!"})
    except Exception as e:
        return jsonify({"message": f"error in updating customer. Error: {e}"})


@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_user(customer_id):
    try:
        customer = Customer.query.get(customer_id)

        if customer:
            # Delete the customer from the database
            db.session.delete(customer)
            db.session.commit()
            return jsonify({"message": "Customer deleted successfully"})
        else:
            return jsonify({"message": "Customer not found"})

    except Exception as e:
        return jsonify({"message": f"error in deleting customer. Error: {e}"})

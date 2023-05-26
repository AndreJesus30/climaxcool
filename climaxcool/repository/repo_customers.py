from climaxcool.models import Customers

class Repo_Customers():
    
    def save_customer():
        pass
    
    def get_customers_by_id(self, customer_id):
        customer = Customers.query.get(int(customer_id))
        return customer
    
    def get_customers_order_by_name(self):
        customers = Customers.query.order_by(Customers.name_customer).all();
        return customers

    def get_customers_filter_by(self, selected_customer):
        customer = Customers.query.filter_by(name_customer=selected_customer).first();
        return customer 

    def update_customer_by_id():
        pass

    def delete_customer_by_id():
        pass

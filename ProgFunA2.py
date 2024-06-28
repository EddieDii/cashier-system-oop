import sys 
import datetime

# Define custom exceptions
class InvalidReward(Exception):
    pass

class InvalidCustomer(Exception):
    pass

class InvalidProduct(Exception):
    pass

class Customer: #super class
    # Create a super class to define common attributes 
    # that are shared among different types of customers. 
    def __init__(self, ID, name, reward):
        #create a constructor to initialize the attributes of the object.   
        self.__ID = ID
        self.__name = name
        self.__reward = reward
        self.order_history = []

    @property # getter methods return the values of the attributes of this class
    def ID(self):
        return self.__ID
    
    @property
    def name(self):
        return self.__name 
    
    @property
    def reward(self):
        return self.__reward
    
    @reward.setter 
    # reward value is  a dynamic value that reflects a customer's purchases,
    # but ID and name cannot be changed in this case.
    def reward(self, reward):
        # if reward >= 0:
        self.__reward = reward
        # else:
        #     raise InvalidReward("Reward points cannot be negative.")

    # 4 empty super method: do nothing, intended to be overridden in subclasses
    def get_reward(self):
        pass

    def get_discount(self):
        pass

    def update_reward(self, reward):
        pass

    def display_info(self):
        pass

class BasicCustomer(Customer): #subclass for customer
    # By default, the flat reward rate is 100%, so create a class variable to share this rate with all object
    __reward_rate = 1.0
    def __init__(self, ID, name, reward):
        super().__init__(ID, name, reward)
        #self.order_history = []
    
    def get_reward(self, final_total_cost):
        # Calculate reward based on the total cost and the reward rate
        return round(final_total_cost * BasicCustomer.get_reward_rate())
    
    def update_reward(self, value):
        # Update the reward attribute by adding the given value
        self._Customer__reward += value 

    def display_info(self):
        # Display info about the BasicCustomer
        print(f"ID: {self.ID}, Name: {self.name}, Reward Rate: {round(BasicCustomer.get_reward_rate()*100,1)}%, Reward Points: {self.reward}.")

    @classmethod
    def set_reward_rate(cls,value):
        cls.__reward_rate = value
        return cls.__reward_rate
    
    @classmethod
    def get_reward_rate(cls):
        return cls.__reward_rate
    
class VIPCustomer(Customer): #subclass of customer
    __reward_rate = 1.0
    def __init__(self, ID, name, reward, discount_rate = 0.08):
        super().__init__(ID, name, reward)
        self.__discount_rate = discount_rate
        #self.order_history = []
    
    # getter method for the attributes of VIPCustomer
    @property
    def discount_rate(self):
        return self.__discount_rate

    @discount_rate.setter
    def discount_rate(self, value):
        # Ensure that the value cannot be negative and cannot exceed 100% 
        # if 0 <= value <= 1:
        self.__discount_rate = value
        # else:
        #     raise ValueError("Discount rate must be between 0% (0.0) and 100% (1.0).")
    
    def get_discount(self, original_total_cost):
        discount = original_total_cost * self.__discount_rate
        return round(discount)
    
    def get_reward(self, original_total_cost):
        discount = original_total_cost * self.__discount_rate
        final_total_cost = original_total_cost - discount
        reward = final_total_cost * VIPCustomer.get_reward_rate()
        return round(reward)
    
    def update_reward(self, value):
        self._Customer__reward += value

    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward Rate: {VIPCustomer.get_reward_rate() * 100}%, Discount Rate: {self.discount_rate * 100}%, Reward Points: {self.reward}")


    @classmethod
    def set_reward_rate(cls, value):
        cls.__reward_rate = value

    # getter method for the reward rate
    @classmethod
    def get_reward_rate(cls):
        return cls.__reward_rate

    # setter method for the discount rate   
    def set_discount_rate(self, value):
        self.__discount_rate = value
        
class Product:
    def __init__(self, product_ID, product_name, unit_price, dr_prescription = False): 
        self.__product_ID = product_ID
        self.__product_name = product_name
        self.__unit_price = unit_price
        self.__dr_prescription = dr_prescription 

    @property 
    def product_ID(self):
        return self.__product_ID
    @property
    def product_name(self):
        return self.__product_name
    @property
    def dr_prescription(self):
        return self.__dr_prescription
    
    @property
    def unit_price(self):
        return self.__unit_price
    
    
    def display_info(self):
        #  Prints the values of the Product attributes
        prescription_status = "Yes" if self.dr_prescription else "No"
        print(f"Product ID: {self.product_ID} Product Name: {self.product_name} Unit Price: {self.unit_price} Need_Prescription:{prescription_status}")

class Bundle(Product): #subclass of Product, have a list of components
    def __init__(self, product_ID, product_name, component, unit_price = 0, dr_prescription = False):
        super().__init__(product_ID,product_name,dr_prescription)
        self.__component = component
        self.__unit_price = unit_price
    
    @property
    def unit_price(self):
        return self.__unit_price

    @property
    def component(self):
        return self.__component
    
    @property
    def dr_prescription(self):
        return self.__dr_prescription
    
    # turn the list of components into a string
    def component_list(self):
            return ', '.join(self.component)
    
    # calculate the total price of the bundle
    def calculate_price(self, record):
        total_price = 0
        for comp in self.component:
            product = record.products.get(comp)
            if product:
                total_price += product.unit_price
        self.__unit_price = round(total_price * 0.8,2)

    # check if the bundle needs a prescription
    def bundle_prescription(self, record):
        need_prescription = False
        for comp in self.component:
            product = record.products.get(comp)
            if product:
                if product.dr_prescription:
                    need_prescription = True
                    continue
        self.__dr_prescription = need_prescription              

    
    def display_info(self):
        #  Prints the values of the Product attributes
        prescription_status = "Yes" if self.dr_prescription else "No"
        components = self.component_list()
        print(f"Product ID: {self.product_ID} Product Name: {self.product_name} Component:{components} Unit Price: {self.unit_price}  Need_Prescription:{prescription_status}")
    

class Order:
    def __init__(self, customer, product, quantity):
        self.__customer = customer
        self.__prodcut = product
        self.__quantity = quantity

    @property
    def product(self):
        return self.__prodcut
    @property
    def customer(self):
        return self.__customer
    @property
    def quantity(self):
        return self.__quantity
    
    def compute_cost(self):
        discount = 0
        original_total_cost = self.product.unit_price * self.quantity
        # Calculate discount if customer is VIPCustomer
        if isinstance(self.customer, VIPCustomer):
            discount = original_total_cost * self.customer.discount_rate
            final_total_cost = original_total_cost - discount
        else:
            final_total_cost = original_total_cost

        # Calculate reward based on the final total cost        
        if hasattr(self.customer, 'get_reward'):
            reward = self.customer.get_reward(original_total_cost)

        return (original_total_cost, discount, final_total_cost, reward)

class Records:
    def __init__(self):
        self.customers = []
        self.products = {}

    def read_customers(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0].startswith('B'): # B as "BasicCustomer: ID, name, rewad_rate, reward".... 
                        customer = BasicCustomer(data[0].strip(), data[1].strip(),int(data[3].strip()))
                    elif data[0].startswith('V'): # # V as "VIPCustomer: ID, name, reward_rate, discount_rate, reward".... 
                        customer = VIPCustomer(ID = data[0].strip(), name = data[1].strip(),reward = int(data[4].strip()),discount_rate=float(data[3].strip()))
                    self.customers.append(customer)
        except FileNotFoundError:
            print(f"Customer file {filename} not found.")
        
    def read_products(self, filename):
        try:
            with open(filename,'r') as file:
                for line in file:
                    data = [item.strip() for item in line.strip().split(",")] # to avoid the space in the string
                    if data[0].startswith('P'): # as a regular product
                        dr_prescription = True if data[3].strip().lower() == 'y' else False
                        product = Product(data[0].strip(), data[1].strip(), float(data[2].strip()),dr_prescription)
                        self.products[data[0]] = product
                    elif data[0].startswith('B'): # as a bundle
                        product = Bundle(data[0].strip(), data[1].strip(), data[2:])
                        product.calculate_price(self)
                        product.bundle_prescription(self)
                        self.products[data[0]] = product
        except FileNotFoundError:
            print(f"Product file {filename} not found.")
    
    # read orders from the file and update the customer's order history and reward points
    def read_orders(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(",")
                    customer_identifier = data[0].strip()
                    customer = self.find_customer(customer_identifier)
                    # assume that customer name in the file is existing in the customer list
                    if customer is not None:
                        products = []
                        for i in range(1, len(data)-3,2):
                            product_identifier = data[i].strip()
                            quantity = int(data[1+1].strip())
                            product = self.find_product(product_identifier)
                            if product is not None:
                                products.append((product.product_name, product.unit_price, quantity))
                        total_cost =float(data[-3].strip())
                        earned_rewards = int(data[-2].strip())
                        order_time = data[-1].strip()
                        order = {
                            'products': products,
                            'total_cost': total_cost,
                            'earned_rewards': earned_rewards,
                            'order_time': order_time
                        }
                        customer.order_history.append(order)
                        customer.update_reward(earned_rewards)
        except Exception:
            print("Cannot load the order file.")

    # check if the customer exists in the list
    def find_customer(self, search_value):
        search_value = search_value.strip()
        for customer in self.customers:
            if customer.name == search_value or customer.ID == search_value:
                return customer
        return None
    
    # check if the product exists in the list
    def find_product(self, search_value):
        search_value = search_value.strip()
        for product in self.products.values():
            if hasattr(product, 'product_name') and (product.product_name == search_value or product.product_ID == search_value):
                return product
        return None
    
    # display the information of all customers
    def list_customers(self):
        for customer in self.customers:
            customer.display_info()

    # display the information of all products
    def list_products(self):
        for product in self.products.values():
            product.display_info()

    # save the information of customers, products, and orders into the file
    def save_customers(self, filename):
        with open(filename, 'w') as file:
            for customer in self.customers:
                if isinstance(customer, BasicCustomer):
                    file.write(f"{customer.ID},{customer.name},{BasicCustomer.get_reward_rate()},{customer.reward}\n")
                elif isinstance(customer, VIPCustomer):
                    file.write(f"{customer.ID},{customer.name},{VIPCustomer.get_reward_rate()},{customer.discount_rate},{customer.reward}\n")
    
    def save_products(self, filename):
        with open(filename, 'w') as file:
            for product in self.products.values():
                # check if the product is a regular product or a bundle
                if type(product) == Product: # to aviod the bundle class be added into the regular product list
                    file.write(f"{product.product_ID},{product.product_name},{product.unit_price},{'y' if product.dr_prescription else 'n'}\n")
                elif isinstance(product, Bundle):
                    components = ','.join(product.component)
                    file.write(f"{product.product_ID},{product.product_name},{components}\n")

    def save_orders(self, filename):
        with open(filename, 'w') as file:
            for customer in self.customers:
                for order in customer.order_history:
                    products = ','.join([f"{product[0]},{product[2]}" for product in order['products']])
                    total_cost = order['total_cost']
                    earned_rewards = order['earned_rewards']
                    order_time = order['order_time']
                    file.write(f"{customer.ID},{products},{total_cost:.2f},{earned_rewards},{order_time}\n")

class Operations:
    def __init__(self, customer_file="customers.txt", product_file="products.txt", order_file="orders.txt"): #default file names
        self.records = Records()
        try:
            self.records.read_customers(customer_file)
            self.records.read_products(product_file)
            if order_file:
                self.records.read_orders(order_file)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1) 

    def main_menu(self):
        while True:
            print('Welcome to the RMIT pharmacy!'.center(60))
            print("#"*60)
            print(f"""
                You can choose from the following options:
                1. Make a purchase
                2. Display existing customers
                3. Display existing products
                4. Add/update information of products
                5. Adjust the reward rate of all Basic customers
                6. Adjust the discount rate of a VIP customer
                7. Display a customer order history
                8. Display all orders
                9. Exit the program
                """)
            print("#"*60)
            option = input("Please choose an option: ").strip()
            print(f"You choose option {option}.")
            if option == '1':
                self.make_purchase()
            elif option == '2':
                self.records.list_customers()
            elif option == '3':
                self.records.list_products()
            elif option =='4':
                self.add_update_products()
            elif option == '5':
                self.adjust_reward_rate()
            elif option == '6':
                self.adjust_vip_discount_rate()
            elif option =='7':
                self.display_customer_order_history()
            elif option =='8':
                self.display_all_orders()
            elif option == '9':
                self.save_and_exit()
                print("Exiting the program. Bye.")
                break
            else:
                print("Invalid option, please choose again.")
    
    # save the information of customers, products, and orders into the file
    def save_and_exit(self):
        self.records.save_customers(customer_file)
        self.records.save_products(product_file)
        self.records.save_orders(order_file)

    # add a new product or update an existing product
    def add_product(self, product_name, price, prescription_required):
        existing_ids = [int(product.product_ID[1:]) for product in self.records.products.values()]
        unique_number = 1
        while unique_number in existing_ids:
            unique_number +=1
        new_product_id = "P" + str(unique_number) # create a unique product number
        if float(price) <=0 or prescription_required.lower() not in ['y', 'n']:
            return None
        
        product = Product(new_product_id, product_name,float(price),prescription_required.lower() == 'y')
        self.records.products[new_product_id]=product
        print(f"New product:{product_name} has been successfully added.")
    
    def update_prodcut(self,product_name, price, prescription_required):
        product = self.records.find_product(product_name)
        if product is not None:
            if float(price) <=0 or prescription_required.lower() not in ['y', 'n']:
                return None
            product._Product__unit_price = float(price)
            product._Product__dr_prescription = prescription_required.lower() == 'y'  
            self.update_bundles(product.product_ID)
            print(f"{product.product_name} has been successfully updated.")  
    
    # if the product is updated, the bundles that contain this product should be updated as well
    def update_bundles(self, product_ID):
        for bundle in self.records.products.values():
            if isinstance(bundle, Bundle) and product_ID in bundle.component:
                bundle.calculate_price(self.records)
                bundle.bundle_prescription(self.records)

    def add_update_products(self):
        while True:
            try:
                product_info = input("Enter products information[e.g. vitaminC 12 n, vitaminC 19.5 y]:").split(",")
                valid_products = []
                for single_product in product_info:
                    single_product_info = single_product.strip().split()
                    if len(single_product_info) !=3:
                        raise ValueError('Invalid product information format. Ensure each product has name, price, and prescription.')
                    name_identifier, price, prescription_required = single_product_info
                    if float(price) <=0 or prescription_required.lower() not in ['y','n']:
                        raise ValueError("Price must be greater than 0 and prescription status must be 'y' or 'n'.")
                    product = self.records.find_product(name_identifier)
                    valid_products.append((product, name_identifier, price, prescription_required))
                for product, name_identifier, price, prescription_required in valid_products:
                    if product is None:
                        self.add_product(name_identifier, price,prescription_required)
                    else:
                        self.update_prodcut(name_identifier, price, prescription_required)
                break
            except Exception as e:
                print(e)
                print("Invalid information. Try again.")

    def adjust_reward_rate(self):
        while True:
            try:
                new_rate = float(input("Enter the new reward rate for all Basic customers (as a decimal, e.g., 1 for 100%):  "))
                if new_rate <=0:
                    raise ValueError("Reward rate must be a positive number.") 
                # update the reward rate for all Basic customers
                BasicCustomer.set_reward_rate(new_rate)
                print("Reward rate for all Basic customers has been updated successfully.")
                break
            except Exception as e:
                print(e)
                print("Invalid input. Please try again.")

    def adjust_vip_discount_rate(self):
        while True:
            try:
                customer_identifier = input("Enter the name or ID of a VIP customer: ")
                customer = self.records.find_customer(customer_identifier)
                # check if the customer is a VIP customer
                if customer is None or not isinstance(customer, VIPCustomer):
                    raise ValueError("Please enter a existing VIP customer.")
                print(f"Hello! VIP customer: {customer.name}!")
                while True:
                    try:
                        new_rate = float(input("Enter the new discount rate for the VIP customer (as a decimal, e.g., 0.2 for 20%): "))
                        if new_rate <=0:
                            raise ValueError("Discount rate must be a positive number.")
                        # update the discount rate for the VIP customer
                        customer.set_discount_rate(new_rate)
                        print(f"Discount rate for the VIP customer{customer.name} has been updated successfully to {round(new_rate*100,1)}%.")
                        break
                    except ValueError as e:
                        print(e)
                        print("Invalid input.Try again.")
                break        
            except ValueError as e:
                print(e)
                print("Invalid input.Try again.")


    def display_customer_order_history(self):
        while True:
            try:
                customer_name = input("Enter customer's name/ID: ").strip()
                customer = self.records.find_customer(customer_name)
                if customer is None:
                    print("The customer does not exit. Try a exit customer again.")
                    continue
                # if history list is empty, print this message, and ends the function.
                if not customer.order_history:
                    print(f"Sorry, {customer.name} has no order history.")
                else:
                    max_product_length = 0
                    for order in customer.order_history:
                        product_line = [f"{quantity}*{product_name}" for product_name, unit_price,quantity in order["products"]]
                        products_str = ", ".join(product_line)
                        # through comparing the length of each order's product list to find the max length of product list, add 3 to get more space
                        if len(products_str) + 2 * len(order["products"]) > max_product_length:
                            max_product_length = len(products_str) + 2 * len(order["products"])
                    
                    print(f"This is the order history of {customer.name}")
                    print(f"{'     '.ljust(10)} {'Products'.ljust(max_product_length)} {'Total Cost'.ljust(15)} {'Earned Rewards'.ljust(15)}")
                    for idx, order in enumerate(customer.order_history, start=1):
                        products_line = [f"{quantity} * {product_name}" for product_name, unit_price, quantity in order['products']]
                        products_str = ", ".join(products_line)
                        total_cost = order['total_cost']
                        earned_rewards = order['earned_rewards']
                        # create a table to display the order history
                        print(f"{f'Order {idx}'.ljust(10)} {products_str.ljust(max_product_length)} {format(total_cost,'.2f').ljust(15)} {str(earned_rewards).ljust(15)}")
                break
            except Exception as e:
                print(e)
                print("Invalid happens.")

    def display_all_orders(self):
        all_orders = []
        for customer in self.records.customers:
            for order in customer.order_history:
                all_orders.append({
                    'customer_name': customer.name,
                    'products': order['products'],
                    'total_cost' : order['total_cost'],
                    'earned_rewards': order['earned_rewards'],
                    'order_time': order['order_time']
                })
        if not all_orders:
            print("Order list is empty.")
            return
        
        # find the max length of the product list to create a table
        max_product_length = 0
        for order in all_orders:
            product_line = [f"{quantity} * {product_name}" for product_name, unit_price, quantity in order["products"]]
            products_str = ", ".join(product_line)
            if len(products_str) + 2 * len(order["products"]) > max_product_length:
                max_product_length = len(products_str) + 2 * len(order["products"])
        print(f"{'Customer'.ljust(15)} {'Products'.ljust(max_product_length)} {'Total Cost'.ljust(15)} {'Earned Rewards'.ljust(15)} {'Order Time'.ljust(20)}")
        for order in all_orders:
            products_line = [f"{quantity} * {product_name}" for product_name, unit_price, quantity in order['products']]
            products_str = ", ".join(products_line)
            total_cost = order['total_cost']
            earned_rewards = order['earned_rewards']
            order_time = order['order_time']
            print(f"{order['customer_name'].ljust(15)} {products_str.ljust(max_product_length)} {format(total_cost, '.2f').ljust(15)} {str(earned_rewards).ljust(15)} {order_time.ljust(20)}")

    def make_purchase(self):
        while True:
            try:
                customer_identifier = input("Enter the customer name or ID: ").strip() 
                customer = self.records.find_customer(customer_identifier)
                if customer is None:
                    # check if the customer is a new customer
                    if customer_identifier.startswith(('B', 'V')) and customer_identifier[1:].isdigit():
                        print("No such customer ID found.")
                        continue
                    elif not customer_identifier.isalpha():
                        print("Customer name must contain only alphabetic characters.")
                        continue
                    elif customer_identifier.isalpha():
                        existing_ids = [int(customer.ID[1:]) for customer in self.records.customers] 
                        unique_number = 1
                        # list all the existing customer IDs, find the unique number for the new customer
                        while unique_number in existing_ids:
                            unique_number += 1
                        new_customer_id = "B" + str(unique_number)
                        print(f"This is a new customer. Register as a Basic Customer: B{unique_number} {customer_identifier}.")
                        customer = BasicCustomer(new_customer_id, customer_identifier, 0)
                        self.records.customers.append(customer)
                    else:
                        print("Invalid customer identifier. Please try again.")
                        continue
                else:
                        customer_type = "Basic" if isinstance(customer, BasicCustomer) else "VIP"
                        print(f"Welcome back! {customer_type} customer: {customer.name}.") 
                
                while True:
                    try:
                        # get the product names and quantities
                        product_names = self.get_valid_product_name()
                        if not product_names:
                            continue
                        while True:
                            try:
                                quantities = self.get_valid_quantity(len(product_names))
                                break
                            except Exception as e:
                                print(e)
                                continue
                        prescription_needed = any(self.records.find_product(name).dr_prescription for name in product_names)
                        prescription_valid = self.get_valid_prescription() if prescription_needed else True

                        # filter out the products that require a prescription if the customer does not have one
                        if not prescription_valid:
                            product_names, quantities = self.filter_products_need_prescription(product_names, quantities)
                            if not product_names:
                                print("No eligible products to purchase after filtering out prescription-required items.")
                                break

                        self.purchase(customer, product_names, quantities)
                        break
                    except Exception as e:
                        print(e)
                        print("Invalid input. Try again.")
                        continue
                break
            except Exception as e:
                print(e)
                print("Invalid input. Try again.(The whole process)")
                continue
     
    def get_valid_product_name(self):
        # input product name and check product name whether it is in the product list
        while True:
            product_names_input = input("Enter the names of the products, separated by commas [e.g. vitaminC, vitaminE]: ").strip()
            product_names =[name.strip() for name in product_names_input.split(",") if name.strip()] 
            if all(self.records.find_product(name) is not None for name in product_names):
                return product_names
            else:
                print("Product not found. Please try again.")

    def get_valid_quantity(self, num_product):
        # input quantity
        while True:
                quantities_input = input("Enter the numbers of the products, separated by commas[e.g. 1, 2, 3]:  ").strip()
                quantities = [int(quantity.strip()) for quantity in quantities_input.split(",") if quantity.strip()]
                if len(quantities) == num_product and all(int(quantity)== quantity and int(quantity) >0 for quantity in quantities):
                    return quantities
                else:
                    print("Invalid quantity.Please try again.")

    def get_valid_prescription(self):
        while True:
            dr_prescription = input("Do you have a doctor's prescription? (y/n): ").strip().lower()
            if dr_prescription == 'y':
                return True
            elif dr_prescription == 'n':
                print ("A valid prescription is required for this purchase. Remove all invalid products.")
                return False
            else:
                print("Error: Please enter 'y' for yes or 'n' for no.")
    
    # filter out the products that require a prescription if the customer does not have one
    def filter_products_need_prescription(self, product_names, quantities):
        filtered_products = []
        filtered_quantities = []
        for name, quantity in zip(product_names,quantities):
            if not self.records.find_product(name).dr_prescription:
                filtered_products.append(name)
                filtered_quantities.append(quantity)
        return filtered_products, filtered_quantities
            
    def purchase(self, customer, product_names, quantities):
        original_total_cost = 0
        final_total_cost = 0
        discount = 0
        reward = 0
        detail=[]
        for name, quantity in zip(product_names, quantities):
            product = self.records.find_product(name)
            cost = product.unit_price * quantity
            original_total_cost += cost
            reward = customer.get_reward(cost)
            detail.append((product.product_name, product.unit_price, quantity))
        # Apply rewards if applicable
        if isinstance(customer, VIPCustomer):
            discount = original_total_cost * customer.discount_rate
            final_total_cost = original_total_cost-discount
            reward_deduction = min(customer.reward // 100 * 10, int(final_total_cost))
            print(f"Applying ${reward_deduction} discount from reward points.")
            final_total_cost -= reward_deduction
            reward = customer.get_reward(original_total_cost)
            new_reward = int(reward-reward_deduction*10)
        elif isinstance(customer, BasicCustomer):
            final_total_cost = original_total_cost
            discount = 0
            reward_deduction = min(customer.reward // 100 * 10, int(final_total_cost))
            print(f"Applying ${reward_deduction} discount from reward points.")
            final_total_cost -= reward_deduction
            reward = customer.get_reward(original_total_cost)
            new_reward = int(reward-reward_deduction*10)
        customer.update_reward(new_reward)
        if detail:
            self.display_receipt(customer, detail, original_total_cost, discount, final_total_cost, reward)      

        # Update the purchase into order history
        order = {
            'products':detail,
            'total_cost': final_total_cost,
            'earned_rewards': reward,
            'order_time': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }    
        customer.order_history.append(order)


    def display_receipt(self, customer, detail, original_total_cost, discount, final_total_cost, reward):
        print('-' * 45)
        print("Receipt".center(45, ' '))
        print('-' * 45)
        print("Name:".ljust(20),customer.name)
        for info in detail:
            product_name, unit_price, quantity = info
            print("Product:".ljust(20), product_name)
            print("Unit Price:".ljust(20), f"{unit_price:.2f} (AUD)")
            print("Quantity:".ljust(20), f"{quantity}")
            print('-' * 45)
        if isinstance(customer, VIPCustomer):
            print("Original cost:".ljust(20),f"{original_total_cost:.2f} (AUD)")
            print("Discount:".ljust(20),f"{discount:.2f} (AUD)")
        print("Total cost:".ljust(20), f"{final_total_cost:.2f} (AUD)")
        print("Earned reward:".ljust(20), f"{reward}")
        print('-' * 45)


if __name__ == '__main__':
    if len(sys.argv) not in [1, 3, 4]:
        # print the usage of the program
        print("Usage: python ProgFunA2_s4070702.py [customers.txt products.txt] [orders.txt]")
        sys.exit(1)
    
    customer_file = "customers.txt"
    product_file = "products.txt"
    order_file = "orders.txt" if len(sys.argv) == 1 else None
    
    # check if the user has provided the file names
    if len(sys.argv) >= 3:
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
    if len(sys.argv) == 4:
        order_file = sys.argv[3]
    
    app = Operations(customer_file, product_file, order_file)
    app.main_menu()







'''
Analysis/ Reflection:
By using oop, I learnt the meanings of inheritance, encapsulation deeply. 
Product class is the parent class of product and bundle.
Customer class is the parent class of BasicCustomer and VIPCustomer. 
The parent class has some common attributes and methods that can be 
shared by the subclasses. And it can be overridden by the subclasses.
The subclasses can have their own attributes and methods.
Although it can be done by using functions with loops and 
if-else statements, oop makes the code more maintainable.
Everytime I update the code, I just need to update or add some methods 
in the class, dont need to change the whole code logic.
But at the begining, I was confused about the getter and setter methods, 
I thought it is not necessary to use them. And the
super class, child class, class method, static method, I was confused about them. 
It took me a long time to understand them.
But now, I think I have a better understanding of them.
In CREDIT level, the most difficult part is to read the bundle components from the 
file and calculate the total price of the bundle and 
check if the bundle needs a prescription. And at the begining, I didn't realize that 
I need to use a child class to organize the bundle class,
many errors and bugs happened. But after I realized that, I created a child class to 
reorganize the bundle class, it became more clear.
In the read_products method, I didn't know how to aviod  the space in the string, 
although I've used the strip() method, it still didn't work.
I found this link: https://stackoverflow.com/questions/13808592/splitting-each-string
-in-a-list-at-spaces-in-python, 
it helped me to solve this problem.
In DI level, I think the most difficult part is to update the price and prescription 
status of the bundle when the product is updated. 
I tried many times, because at that time, I didn't have a clear understanding of the 
class and object, how to use the methods and variables in the different classes.
In the HD level, I found the similarities between the update products changes to the 
bundles and updating order history, so this part becomes easier.
I didn't understand the meaning of "indicating the correct usage of arguments and exit", 
this link helped me a lot: https://hplgit.github.io/primer.html/doc/pub/input/._input-solarized007.html
I also learnt a liitle bit about python debugger: https://docs.python.org/3/library/pdb.html 
to identify my code errors quickly.
'''
import os
import time

import shopify
import pyactiveresource.connection

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
SHOP_URL = f"https://{API_KEY}:{PASSWORD}@able-test1.myshopify.com/admin/api/2021-07/"

shopify.ShopifyResource.set_site(SHOP_URL)


"""
Instructions:


Create a python virtual environment, activate it and install packages

python3 -m venv env
source env/bin/activate
pip install shopifyapi


Create a .env file in the root folder

In the .env file create:
export API_KEY="xxx"
export PASSWORD="xxx"

export variables by running - source .env

Test functionality as shown at the end of the file
"""

def api_call_with_retry(func, *args, **kwargs):
    retry_count = kwargs.pop('retry_count', None)
    if retry_count:
        pass
    else:
        retry_count = 0
    
    try:
        return func(*args, **kwargs)
    except pyactiveresource.connection.Error as e:
        err = e
        while retry_count > 0 and err:
            try:
                time.sleep(0.55)
                print("retrying...")
                return func(*args, **kwargs)
            except pyactiveresource.connection.Error as e:
                err = e

            retry_count -= 1
        
        if int(err.response.code)//100 == 4:
            raise err
        elif int(err.response.code)//100 == 5:
            # if the caller handles 5xx errors we raise exception as below
            # raise pyactiveresource.connection.ServerError
            # otherwise return error message
            return f"The server encountered an Error with code: {err.response.code}."



def api_iterator(func, *args, **kwargs):
    try:
        product_list = func(*args, **kwargs)
        for product in product_list:
            yield product
    except pyactiveresource.connection.Error as e:
        code = e.response.code
        if int(code)//100 == 4:
            raise e
        elif int(code)//100 == 5:
            # if the caller handles 5xx errors we raise exception as below
            # raise pyactiveresource.connection.ServerError
            # otherwise return error message
            return f"The server encountered an Error with code: {code}."
    
    while product_list.has_next_page():
        time.sleep(0.55)
        try:
            product_list = product_list.next_page()
            for product in product_list:
                yield product
        except pyactiveresource.connection.Error as e:
            code = e.response.code
            if int(code)//100 == 4:
                raise e
            elif int(code)//100 == 5:
                # if the caller handles 5xx errors we raise exception as below
                # raise pyactiveresource.connection.ServerError
                # otherwise return error message
                return f"The server encountered an Error with code: {code}."


print(api_call_with_retry(shopify.Product.find, 4459014226001, retry_count=3))

# count = 0  
# for product in api_iterator(shopify.Product.find, limit=70):
#     print("Title: ", product.title)
#     count += 1
#     print("count is: ", count)
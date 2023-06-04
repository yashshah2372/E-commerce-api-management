# E-commerce-api-management
Welcome to E-commerce api management:
 - There are six different routes for this application, please follow along with me.
 - The application is deployed at 'https://loopr-assignment.yashshah42.repl.co'.

#1 - Let's start with first generating the JWT token by logging to url 'https://loopr-assignment.yashshah42.repl.co/login'
  - Send the post request via Postman, the username and passowrd is included in "login_info.json", the response is a JWT token which you        will have to include to access any route henceforth.
 
#2 - The cart information is available at https://loopr-assignment.yashshah42.repl.co/carts/1234567890?token=<jwt_token>.
  - Without the token you won't be able to access this route. It will give the cart information for a particular user
  - The route already contains userId,feel free to change it from carts.json.

#3 - To add a product, send a post request to https://loopr-assignment.yashshah42.repl.co/carts/1234567890/add-product?token=<jwt_token>.
   - Add product_id and quantity to json raw data from postman.
   - It will add the product and evaluat the total price to that specific user.

#4 - To update a quantity, send a post request to https://loopr-assignment.yashshah42.repl.co/cart/9876543210/update-quantity?token=<jwt-token>.
   - Add product_id and quantity to json raw data from postman.
   - It will check for that product id and update the quantity.
  
#5 - To delete a quantity, send a post request to https://loopr-assignment.yashshah42.repl.co/cart/9876543210/delete-product?token=<jwt-token>.
   - Add product_id to json raw data from postman.
   - It will delete that id from the particular user.

#6 - To fetch all the product information, send a get request from any browser to https://loopr-assignment.yashshah42.repl.co/products?token=<jwt-token>.
   - It will fetch all the products.

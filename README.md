Getting Started with eCommerce App
===============================

Run without docker
-------------------
1. install python
2. go to the project dir via cmd where requirement.txt is given 
3. write `pip install -r requirements.txt`
4. in your web browser go to `http://127.0.0.1:8000/`


Run with docker
----------------
1. go to the project dir via cmd where requirement.txt is given 
2. write `docker-compose build`
3. write `docker-compose up`
4. in your web browser go to `http://127.0.0.1:8000/`


Urls for user with view
-----------------------
1. `http://127.0.0.1:8000/login` : For user login
2. `http://127.0.0.1:8000/signup` : For user signup
3. `http://127.0.0.1:8000/home` : For user to see product list and choose item
4. `http://127.0.0.1:8000/cart` : For user to see selected product list 
5. `http://127.0.0.1:8000/checkout` : For user buy selected items
6. `http://127.0.0.1:8000/profile` : For user profile and update user settings
7. `http://127.0.0.1:8000/logout` : For user logout


Urls for third party user to retrive rest api json response
-----------------------------------------------------------
1. `http://127.0.0.1:8000/loginapi` : For third party user login
2. `http://127.0.0.1:8000/logout` : For third party user logout
3. `http://127.0.0.1:8000/register` : For third party user signup
4. `http://127.0.0.1:8000/productapi` : For third party user to see product list and purchase item


Urls for third party user to retrive graphql json response using jwt
--------------------------------------------------------------------
1. `http://127.0.0.1:8000/productsgraphqlapi` : For third party user to see product list and purchase item'
{
  products(first:2,skip:2){
    id,
    name,
    description,
    image,
    stockStatus
  }
}
2. `http://127.0.0.1:8000/thirdparty` : For third party user login, logout, change password, update user info

mutation{
  tokenAuth(username:"afrinjaman", password: "mail12"){
    success,
    errors,
    token,
    refreshToken,
    user{
      username
    }
  }
}


Urls for Admin with view
------------------------
1. `http://127.0.0.1:8000/admin` : For admin usage, add delete update product
  username: "admin"
  password: "admin"


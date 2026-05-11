
# redirect user to github for login
1. https://github.com/login/oauth/authorize
    ?client_id=GITHUB_CLIENT_ID
    &redirect_uri=https://yourapp.com/github/callback
    &scope=user:email


# github will send code to us
2. callback?code=abc123


# get access token using code
POST https://github.com/login/oauth/access_token

# get user details
Fetch user details from GitHub

Response:
{
   id: 101,
   name: "Anji",
   email: "test@gmail.com"
}





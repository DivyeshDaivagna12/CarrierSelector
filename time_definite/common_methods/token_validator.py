import os
import jwt
import time

from time_definite.common_methods.unauthorized_exception import UnauthorizedException

# Signature Verification
def access_token_decoder(access_token,issuer_url,issuer_url_m2m):
    try:
        decoded_token = jwt.decode(
            access_token,
            options={
                'verify_signature':False,
                'verify_exp':True 
            }
        )
        
        # Calculating duration of the token
        expiration_timestamp = decoded_token['exp']
        print("expiration_timestamp==",expiration_timestamp)
        current_timestamp=time.time()
        print(" current_timestamp==", current_timestamp)

        duration_seconds = expiration_timestamp - current_timestamp
        print("Duration of the token:",duration_seconds,"seconds")

        #Manual verification of issuer 
        print("Issuer Url from token is:",decoded_token.get('iss'))
        if decoded_token.get('iss') == issuer_url or decoded_token.get('iss') == issuer_url_m2m :

             email = decoded_token.get('email')
             return email
        else:
            raise UnauthorizedException("Invalid issuer")               
       
    
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has Expired")
    
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid Token")

def get_email_from_access_token(access_token :str) -> str:  

    issuer_url = os.environ['issuer_url']
    
    print("issuer_url=",issuer_url)

    issuer_url_m2m=os.environ['issuer_url_m2m']

    print("issuer_url_m2m",issuer_url_m2m)

    email = access_token_decoder(access_token,issuer_url,issuer_url_m2m)

    print("Decoded email", email)

    return email
import facebook

class Facebook:


    @staticmethod
    def validate(auth_token):

       try:

            graph= facebook.GraphAPI(access_token=auth_token)
           

            profile=graph.request('/me?fields=name,email')
            print(profile)
            return profile
       except:
          return 'tokendjddj is invalid or expired'

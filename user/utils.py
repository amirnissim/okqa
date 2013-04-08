def get_user_avatar(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    url = None
    if backend.__class__.__name__ == 'FacebookBackend':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    elif backend.__class__.__name__ == 'TwitterBackend':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if url:
        profile = user.get_profile()
        profile.avatar_uri = url
        profile.save()


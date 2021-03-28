import fbchat

def only_for_admin(admin_id, author_id):
    if admin_id == author_id:
        return True
    else:
        return False

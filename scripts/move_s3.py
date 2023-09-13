"""
Move S3 objects
"""

import re

from libdev.s3 import upload_file

from models.user import User
from models.category import Category
from models.post import Post


REPLACE = False


def replace_image(entity):
    """ Replace image of an entity """

    changed = False
    if not entity.image:
        return entity, changed, 0

    if REPLACE:
        new_image = upload_file(entity.image)
        if new_image:
            changed = True
            entity.image = new_image
        else:
            print(f"❌ {entity.image}")

    print(entity.image)
    return entity, changed, 1

def replace_data(entity):
    """ Replace all images of data container of an entity """

    changed = False
    count = 0

    for image in re.findall(r'<img [^>]*src="([^"]+)', entity.data):
        count += 1

        if REPLACE:
            new_image = upload_file(image)
            if new_image:
                changed = True
                entity.data = entity.data.replace(image, new_image)
            else:
                print(f"❌ {image}")
            print(new_image)
        else:
            print(image)

    return entity, changed, count

def main():
    """ Replace S3 objects in DB """

    # Users
    count = 0
    for user in User.get()[::-1]:
        user, changed, count_extra = replace_image(user)
        count += count_extra

        if changed:
            user.save()

    print(f"✅ {count} users")

    # Categories
    count = 0
    for category in Category.get()[::-1]:
        category, changed, count_extra = replace_image(category)
        count += count_extra

        category, changed_extra, count_extra = replace_data(category)
        changed = changed or changed_extra
        count += count_extra

        if changed:
            category.save()

    print(f"✅ {count} categories")

    # Posts
    count = 0
    for post in Post.get()[::-1]:
        post, changed, count_extra = replace_image(post)
        count += count_extra

        post, changed_extra, count_extra = replace_data(post)
        changed = changed or changed_extra
        count += count_extra

        if changed:
            post.save()

    print(f"✅ {count} posts")


if __name__ == '__main__':
    main()

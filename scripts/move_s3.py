import re

from libdev.s3 import upload_file

from models.user import User
from models.category import Category
from models.post import Post


REPLACE = False


if __name__ == '__main__':
    count = 0
    for user in User.get()[::-1]:
        if user.image:
            count += 1

            if REPLACE:
                new_image = upload_file(user.image)
                if not new_image:
                    print(f"❌ {user.image}")
                else:
                    user.image = new_image
            print(user.image)

            user.save()

    print(f"✅ {count} users")

    count = 0
    for category in Category.get()[::-1]:
        changed = False

        if category.image:
            count += 1
            changed = True

            if REPLACE:
                new_image = upload_file(category.image)
                if not new_image:
                    print(f"❌ {category.image}")
                else:
                    category.image = new_image
            print(category.image)

        for image in re.findall(r'<img [^>]*src="([^"]+)', category.data):
            count += 1
            changed = True

            if REPLACE:
                new_image = upload_file(image)
                if not new_image:
                    print(f"❌ {image}")
                else:
                    category.data = category.data.replace(image, new_image)
                print(new_image)
            else:
                print(image)

        if changed:
            category.save()

    print(f"✅ {count} categories")

    count = 0
    for post in Post.get()[::-1]:
        changed = False

        if post.image:
            count += 1
            changed = True

            if REPLACE:
                new_image = upload_file(post.image)
                if not new_image:
                    print(f"❌ {post.image}")
                else:
                    post.image = new_image
            print(post.image)

        for image in re.findall(r'<img [^>]*src="([^"]+)', post.data):
            count += 1
            changed = True

            if REPLACE:
                new_image = upload_file(image)
                if not new_image:
                    print(f"❌ {image}")
                else:
                    post.data = post.data.replace(image, new_image)
                print(new_image)
            else:
                print(image)

        if changed:
            post.save()

    print(f"✅ {count} posts")

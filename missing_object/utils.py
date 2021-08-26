import random
from missing_object.models import ImageObject


def random_picture_missing_obj(ids: [int]) -> tuple:
    """
    fungsi ini digunakan mengambil 4 data gambar.
    1 data yang benar dan 3 data yang salah.
    data diambil secara acak.
    params: ids adalah id dari ImageObject yang belum berhasil dijawab
    return: (picture_question, name_question)
            picture_question -> digunakan untuk dirender di html
            name_question -> digunakan untuk dirender di html
    """
    imgs = list(ImageObject.objects.filter(id__in=ids))
    for _ in range(0, random.randrange(5, 10)):
        random.shuffle(imgs)

    img_select = imgs.pop()
    picture_correct = [{'id': img_select.id, 'picture': img_select.picture.url}]
    name_correct = [{'id': img_select.id, 'name': img_select.name}]

    picture_list = [{'id': img.id, 'picture': img.picture.url} for img in imgs]
    name_list = [{'id': img.id, 'name': img.name} for img in imgs]

    for _ in range(0, random.randrange(3, 7)):
        random.shuffle(picture_list)
    picture_question = picture_correct + picture_list[0:3]
    random.shuffle(picture_question)

    for _ in range(0, random.randrange(3, 10)):
        random.shuffle(name_list)
    name_question = name_correct + name_list[0:3]
    random.shuffle(name_question)
    return picture_question, name_question

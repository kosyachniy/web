from libdev.gen import generate, generate_id

from models.user import User, process_lower


def test_repeated_login(client):
    login = generate(20)
    user_old = User(login=login)
    user_old.save()

    # Get token
    res = client.post('/account/token/', json={
        'token': 'test',
        'network': '',
    })

    assert res.status_code == 200
    token = res.json().get('token')

    # Request
    res = client.post('/account/bot/', json={
        'user': generate_id(),
        'login': login.upper(),
    }, headers={
        'Authorization': token,
    })

    assert res.status_code == 200
    data = res.json()

    assert data.get('id')
    assert data.get('new')

    user_new = User.get(data['id'], fields={'login'})

    assert user_new.login != process_lower(login)
    assert user_new.id != user_old.id

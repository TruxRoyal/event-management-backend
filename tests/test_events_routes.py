from app.utils import constants

def test_get_all_events_empty(client):
    """Debe retornar un mensaje cuando no hay eventos"""
    response = client.get('/api/events')
    assert response.status_code == 200
    assert response.json == {'message': constants.NO_EVENTS}

def test_create_event(client):
    """Debe crear un nuevo evento exitosamente"""
    new_event = {
        "title_event": "Evento de prueba",
        "date_event": "2025-12-31",
        "description_event": "Descripción de prueba",
        "location_event": "Bogotá"
    }

    response = client.post('/api/events', json=new_event)
    assert response.status_code == 201

    event = response.json
    assert event['title_event'] == new_event['title_event']
    assert event['date_event'] == new_event['date_event']
    assert event['description_event'] == new_event['description_event']
    assert event['location_event'] == new_event['location_event']

def test_get_existing_event(client):
    """Debe retornar un evento específico"""
    new_event = {
        "title_event": "Evento de prueba",
        "date_event": "2025-12-31",
        "description_event": "Descripción de prueba",
        "location_event": "Bogotá"
    }

    post_response = client.post('/api/events', json=new_event)
    event_id = post_response.json['id_event']

    response = client.get(f'/api/events/{event_id}')
    assert response.status_code == 200

    event = response.json
    assert event['title_event'] == new_event['title_event']
    assert event['date_event'] == new_event['date_event']
    assert event['description_event'] == new_event['description_event']
    assert event['location_event'] == new_event['location_event']

def test_update_event(client):
    """Debe actualizar un evento existente"""
    new_event = {
        "title_event": "Hackathon",
        "date_event": "2025-04-23",
        "description_event": "Competencia de programación",
        "location_event": "Medellin"
    }

    post_response = client.post('/api/events', json=new_event)
    event_id = post_response.json['id_event']

    updated_event = {
        "title_event": "Hackaton V2",
        "date_event": "2025-06-23",
        "description_event": "Competencia nueva convocatoria",
        "location_event": "Bogotá"
    }

    response = client.put(f'/api/events/{event_id}', json=updated_event)
    assert response.status_code == 200

    event = response.json
    assert event['title_event'] == updated_event['title_event']
    assert event['date_event'] == updated_event['date_event']
    assert event['description_event'] == updated_event['description_event']
    assert event['location_event'] == updated_event['location_event']

def test_delete_event(client):
    """Debe eliminar un evento existente"""
    new_event = {
        "title_event": "Taller de Python",
        "date_event": "2025-6-25",
        "description_event": "Desarrollo de aplicaciones con flask",
        "location_event": "Bogotá"
    }

    post_response = client.post('/api/events', json=new_event)
    event_id = post_response.json['id_event']

    response = client.delete(f'/api/events/{event_id}')
    assert response.status_code == 200
    assert response.json == {'message': constants.EVENT_DELETED, 'id_event': event_id}

    response = client.get(f'/api/events/{event_id}')
    assert response.status_code == 404
    assert response.json == {'error': constants.EVENT_NOT_FOUND}
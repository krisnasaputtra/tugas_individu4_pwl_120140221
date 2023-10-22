from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from sqlalchemy.orm import Session
from ..models import Movie

@view_config(route_name='movies', request_method='POST', renderer='json')
def create_movie(request):
    """ Create a new movie record in the database. """
    db = request.dbsession
    data = request.json_body

    # Validate input data
    if not all(key in data for key in ('title', 'language', 'status', 'rating')):
        raise HTTPBadRequest('Missing required fields')

    # Create a new Movie object with the input values
    movie = Movie(title=data['title'], language=data['language'], status=data['status'], rating=data['rating'])

    # Add the new movie to the database
    db.add(movie)
    db.flush()

    # Return the newly created movie as JSON
    return movie.to_dict()

@view_config(route_name='movies', request_method='GET', renderer='json')
def get_movies(request):
    """ Retrieve a list of movie records from the database. """
    db = request.dbsession
    skip = request.params.get('skip', 0)
    limit = request.params.get('limit', 100)

    # Retrieve a list of movies from the database
    movies = db.query(Movie).offset(skip).limit(limit).all()

    # Return the list of movies as JSON
    return [movie.to_dict() for movie in movies]

@view_config(route_name='movie', request_method='GET', renderer='json')
def get_movie(request):
    """ Retrieve a movie record from the database by ID. """
    db = request.dbsession
    movie_id = request.matchdict['id']

    # Retrieve the movie from the database
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    # Return the movie as JSON, or raise a 404 error if it doesn't exist
    if movie is not None:
        return movie.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='movie', request_method='PUT', renderer='json')
def update_movie(request):
    """ Update an existing movie record in the database. """
    db = request.dbsession
    movie_id = request.matchdict['id']
    data = request.json_body

    # Retrieve the movie from the database
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    # Update the movie with the input values
    if movie is not None:
        if 'title' in data:
            movie.title = data['title']
        if 'language' in data:
            movie.language = data['language']
        if 'status' in data:
            movie.status = data['status']
        if 'rating' in data:
            movie.rating = data['rating']

        # Commit the changes to the database
        db.commit()

        # Return the updated movie as JSON
        return movie.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='movie', request_method='DELETE', renderer='json')
def delete_movie(request):
    """ Delete a movie record from the database by ID. """
    db = request.dbsession
    movie_id = request.matchdict['id']

    # Retrieve the movie from the database
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    # Delete the movie from the database
    if movie is not None:
        db.delete(movie)
        db.commit()

        # Return a success message as JSON
        return {'message': 'Movie deleted'}
    else:
        raise HTTPNotFound()
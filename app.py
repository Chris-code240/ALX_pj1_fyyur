from models import *
migrate = Migrate(app,db)

# search_term = request.form.get('search_term','').lower()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
 
 keyList = list(set([d.city for d in Venue.query.all() if d.city != '']))
 venues = []
 data = []
 v_state = ''

 for i in keyList:
     for venue in Venue.query.filter(Venue.city == i).all():
      venues.append({
              "id":venue.id,"name":venue.name,"num_upcoming_shows":db.session.query(Shows,Venue).join(Venue).filter(Shows.venue_id == venue.id and Shows.start_time < datetime.today()).count()
        })
      print("venues-> " , venues)
      v_state = venue.state

     data.append({
        "city":i,"state":v_state,"venues":venues
      })
     venues = []

  
 data1=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }]
 return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term','').lower()
  count = 1
  results = {}
  found = False
  for word_row in Venue_search.query.all():
    if str(word_row.word) == search_term:
      word_row.count = word_row.count + count
      db.session.commit()
      found = True
      results ={
        "count":word_row.count,
        "data":[
          {
            "id":word_row.venue_id,
            "name":Venue.query.filter(Venue.id == word_row.venue_id).all()[0].name,
            "num_upcoming_shows":Shows.query.filter(Shows.venue_id ==word_row.venue_id).count()
          }
        ]
      }
  for venue in Venue.query.all():
        if str(venue.name).lower() == search_term and found == False:
          found = True
          results ={
        "count":count,
        "data":[
          {
            "id":venue.id,
            "name":venue.name,
            "num_upcoming_shows":Shows.query.filter(Shows.venue_id ==venue.id).count()
          }
        ]
      }
          
          new_word = Venue_search(word=search_term,venue_id=venue.id,count=count)
          db.session.add(new_word)
          db.session.commit()




  return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(int(venue_id))
  past_shows = []
  upcoming_shows =[]
  ven_show = db.session.query(Shows,Venue).join(Venue).all()
  art_show = db.session.query(Shows,Artist).join(Artist).all()
  for show,artis in art_show:
    if show.venue_id == venue_id and show.start_time.replace(tzinfo=utc) <= datetime.today().replace(tzinfo=utc):
      past_shows.append({
      "artist_id": show.artist_id,
      "artist_name": artis.name,
      "artist_image_link": artis.image_link,
      "start_time": str(show.start_time)
    })
    elif show.venue_id == venue_id and show.start_time > datetime.today().replace(tzinfo=utc):
      upcoming_shows.append({
      "artist_id": show.artist_id,
      "artist_name": artis.name,
      "artist_image_link": artis.image_link,
      "start_time": str(show.start_time)
    })
   

  data = {
    "id": str(venue_id),
    "name": str(venue.name),
    "genres": [venue.genres],
    "address": str(venue.address),
    "city": str(venue.city),
    "state": str(venue.state),
    "phone": str(venue.phone),
    "website": str(venue.website_link),
    "facebook_link": str(venue.facebook_link),
    "seeking_talent": str(venue.seeking_talent),
    "seeking_description": str(venue.seeking_description),
    "image_link": str(venue.image_link),
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count":str( len(past_shows)),
    "upcoming_shows_count": str(len(upcoming_shows))
    }
  # print(data)
 
  # data = list(filter(lambda d: d['id'] == venue_id, [data0]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  try:
    form = VenueForm()
    form.validate()
    venue = Venue(name=form.name.data,city=form.city.data,state=form.state.data,address=form.address.data,phone=form.phone.data,image_link=form.image_link.data,genres=form.genres.data,facebook_link=form.facebook_link.data,website_link=form.website_link.data,seeking_talent=form.seeking_talent.data,seeking_description=form.seeking_description.data)
    db.session.add(venue)
    db.session.commit()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()
    

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(int(venue_id))
    db.session.delete(venue)
    db.session.commit()
  except:
      db.session.rollback()


  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  query = Artist.query.all()
  data = []
  for artist in query:
    data.append({'id':artist.id,'name':artist.name})

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term','').lower()
  count = 1
  results = {}
  found = False
  for word_row in Artist_search.query.all():
    if str(word_row.word) == search_term:
      word_row.count = word_row.count + count
      db.session.commit()
      found = True
      results ={
        "count":word_row.count,
        "data":[
          {
            "id":word_row.artist_id,
            "name":Artist.query.filter(Artist.id == word_row.artist_id).all()[0].name,
            "num_upcoming_shows":Shows.query.filter(Shows.artist_id ==word_row.artist_id).count()
          }
        ]
      }
  for artist in Artist.query.all():
        if str(artist.name).lower() == search_term and found == False:
          found = True
          results ={
        "count":count,
        "data":[
          {
            "id":artist.id,
            "name":artist.name,
            "num_upcoming_shows":Shows.query.filter(Shows.artist_id ==artist.id).count()
          }
        ]
      }
          
          new_word = Artist_search(word=search_term,artist_id=artist.id,count=count)
          db.session.add(new_word)
          db.session.commit()

  return render_template('pages/search_artists.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = db.session.query(Artist,Shows).join(Shows).all()
  
  past_shows = []
  upcoming_shows = []
 
# show.start_time.replace(tzinfo=utc) < datetime.today().replace(tzinfo=utc)
  artist_main = Artist.query.filter(Artist.id == artist_id).first()
  show_joined = db.session.query(Shows,Venue).join(Venue).all()
  for past,venue in show_joined:
   if past.start_time.replace(tzinfo=utc) < datetime.today().replace(tzinfo=utc):
    past_shows.append({'venue_id':past.venue_id,'venue_image_link':venue.image_link,'start_time':str(past.start_time),'start_time':str(past.start_time)})
   else:
    upcoming_shows.append({'venue_id':past.venue_id,'venue_image_link':venue.image_link,'start_time':str(past.start_time),'start_time':str(past.start_time)})



  data0 = {
        "id": str(artist_id),
      "name": artist_main.name,
      "genres": [artist_main.genres],
      "city": artist_main.city,
      "state": artist_main.state,
      "phone": artist_main.phone,
      "website": artist_main.website_link,
      "facebook_link": artist_main.facebook_link,
      "seeking_venue": artist_main.seeking_venue,
      "seeking_description": artist_main.seeking_description,
      "image_link": artist_main.image_link,
      "past_shows":past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": Shows.query.filter(Shows.artist_id == artist_main.id,Shows.start_time > datetime.today()).count(),
      "upcoming_shows_count": Shows.query.filter(Shows.id == artist_main.id,Shows.start_time <= datetime.today()).count()
      }
 


  
  return render_template('pages/show_artist.html', artist=data0)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist_main = Artist.query.get(artist_id)
  artist={
    "id": artist_main.id,
    "name": artist_main.name,
    "genres": [artist_main.genres],
    "city": artist_main.city,
    "state": artist_main.state,
    "phone": artist_main.phone,
    "website": artist_main.website_link,
    "facebook_link": artist_main.facebook_link,
    "seeking_venue": artist_main.seeking_venue,
    "seeking_description": artist_main.seeking_description,
    "image_link": artist_main.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    form = ArtistForm()
    form.validate()
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    db.session.commit()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was edited successfully!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be edited.')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  artist_main = Venue.query.get(venue_id)
  venue={
    "id": artist_main.id,
    "name": artist_main.name,
    "genres": [artist_main.genres],
    "city": artist_main.city,
    "state": artist_main.state,
    "address": artist_main.address,
    "phone": artist_main.phone,
    "website": artist_main.website_link,
    "facebook_link": artist_main.facebook_link,
    "seeking_talent": artist_main.seeking_talent,
    "seeking_description": artist_main.seeking_description,
    "image_link": artist_main.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  try:
    form = VenueForm()
    form.validate()
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.address = form.address.data
    venue.genres = form.genres.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was edited successfully!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + form.name.data + ' could not be edited.')
  finally:
    db.session.close()
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  try:
    form = ArtistForm()
    form.validate()
    artist = Artist(name=form.name.data,city=form.city.data,state=form.state.data,phone=form.phone.data,
  image_link=form.image_link.data,genres=form.genres.data,facebook_link=form.facebook_link.data,website_link=form.website_link.data,seeking_venue=form.seeking_venue.data,seeking_description=form.seeking_description.data)
    db.session.add(artist)
    db.session.commit()
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    flash('Artist' + form.name.data + 'was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  try:
    query_artsit = db.session.query(Artist, Shows).join(Shows).all()
    query_venue = db.session.query(Venue, Shows).join(Shows).all()
    data = []
    dup =[]
    x = 0
    for artist,show in query_artsit:
      for venue,show_v in query_venue:
        data.append({

        "start_time": str(show.start_time),
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
      })
    for i in data:
      if i not in dup:
        dup.append(i)
  
    
      
        
      
  except:
    print(data)
    
  
  return render_template('pages/shows.html', shows=dup)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    form = ShowForm()
    form.validate()
    show = Shows(artist_id=form.artist_id.data,venue_id=form.venue_id.data,start_time=form.start_time.data)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
 
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

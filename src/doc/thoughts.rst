===================
Multimedia Database
===================

Tables
======


File
----

- file_id (pk)
- path
- metadata


FileMetadata
------------

metadata_id (pk)
file_id
title
size
length
container
codecs
genre
Front Cover (Book, Album, Single)
Back Cover (Book, Album, Single)
Inside Cover (Book, Album, Single)
Image
Thumbnail
Rating
Liner Notes
Added


Chapter
-------
chapter_id (pk)
Name
Start
End

Book
----
book_id (pk)


ImageFile
---------

image_file_id (pk)
file_id
Full Size
Thumbnail
Metadata


VideoFile
---------

video_file_id (pk)
Metadata


AudioFile
---------

- audio_file_id (pk)
- bitrate
- variable_bitrate
- type
    - Song
    - Spoken
        - Podcast
    - Percussion
    - Acapella
    - Nature

    
Lyrics
------

- lyric_id
- lyrics

    
Work
----

- work_id (pk)
- composer
- lyricist
- lyric_id


MusicRecording
--------------

- music_recording_id (pk)
- song_id
- performed_by - person or group
- arranged_by - person or group
- recorded_on
- language
- rating
- location
- duration


MusicAlbum
----------

- music_album_id (pk)
- artist
- rating

- musicbrainz_id


MusicAlbumTracks
----------------

- music_album_id
- music_recording_id
- last_played
- count_played


Person
------

* Actor:Person
* Director:Person
* Composer:Person
* Author:Person
* Performer:Person
* Producer:Person
* Remixer:Person

- person_id - alphnumeric p[0-9]+ (pk)
- name
- legal_name
- sort_name
- gender
- born
- died
- image
- biography

- imdb_id
- musicbrainz_id


Group
-----

* Cast:Group
* Band:Group

- group_id - alphnumeric g[0-9]+ (pk)
- name

- imdb_id
- musicbrainz_id


GroupMembership
---------------

- group_id (pk)
- person_id (pk)
- joined
- left
- skillset - Singer, Lead Guitar, Base Guitar, Composer etc.


Playlist
--------

Audio File, ... Audio File
Intro + Movie + Intermission + Outro


PhotoAlbum
----------

:see:`MusicAlbum`

- photo_album_id
- name


Functions
=========

Migrate between databases
Import
Export
FindTrack(Artist, Name)
FindTrack(Composer, Name)
FindTrack(Conductor, Name)
FindTrack(Author, Name)

Cover Art
---------

3 places cover art stored

In media file
Alongside media file - cover.png, cover.jpg, back-cover.jpg
Separate directory - qe7ewq76qwg-hdwbjdq877-cover.jpg





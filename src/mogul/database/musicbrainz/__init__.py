from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import CHAR, Text, UnicodeText, Boolean, DateTime, SmallInteger
from sqlalchemy import Enum, Interval
from sqlalchemy.schema import CheckConstraint
from guid import GUID

metadata = MetaData()

annotation = Table('annotation', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, nullable=True),
	Column('text', UnicodeText),
	Column('changelog', String(255)),
	Column('created', DateTime, default=datetime.now),
)

artist = Table('artist', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID, nullable=False),
	Column('name', Integer, ForeignKey('artist_name.id'), nullable=False),
	Column('sort_name', Integer, ForeignKey('artist_name.id'), nullable=False),
	Column('begin_date_year', SmallInteger),
	Column('begin_date_month', SmallInteger),
	Column('begin_date_day', SmallInteger),
	Column('end_date_year', SmallInteger),
	Column('end_date_month', SmallInteger),
	Column('end_date_day', SmallInteger),
	Column('type', Integer, ForeignKey('artist_type.id')),
	Column('country', Integer, ForeignKey('country.id')),
	Column('gender', Integer, ForeignKey('gender.id')),
	Column('comment', String(255), nullable=False, default=''),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	Column('ended', Boolean, nullable=False, default=False),
	CheckConstraint("""(end_date_year IS NOT NULL OR
	    end_date_month IS NOT NULL OR
        end_date_day IS NOT NULL) AND
        ended = TRUE"""),
	CheckConstraint("""(end_date_year IS NULL AND
           end_date_month IS NULL AND
           end_date_day IS NULL)"""),
)

artist_alias_type = Table('artist_alias_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String, nullable=False),
)

artist_alias = Table('artist_alias', metadata,
	Column('id', Integer, primary_key=True),
	Column('artist', Integer, ForeignKey('artist.id')),
	Column('name', UnicodeText),
	Column('locale', Integer),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	Column('type', Integer, ForeignKey('artist_type.id')),
	Column('sort_name', Integer, ForeignKey('artist_name.id'), nullable=False),
	Column('begin_date_year', SmallInteger),
	Column('begin_date_month', SmallInteger),
	Column('begin_date_day', SmallInteger),
	Column('end_date_year', SmallInteger),
	Column('end_date_month', SmallInteger),
	Column('end_date_day', SmallInteger),
	Column('primary_for_locale', Boolean, nullable=False, default=False),
	CheckConstraint('(locale IS NULL AND primary_for_locale IS FALSE) OR (locale IS NOT NULL)',
	    'primary_check'),
	CheckConstraint("""(type <> 3) OR (
          type = 3 AND sort_name = name AND
          begin_date_year IS NULL AND begin_date_month IS NULL AND begin_date_day IS NULL AND
          end_date_year IS NULL AND end_date_month IS NULL AND end_date_day IS NULL AND
          primary_for_locale IS FALSE AND locale IS NULL
        )""",
	    'search_hints_are_empty'),
)

artist_annotation = Table('artist_annotation', metadata,
	Column('artist', Integer, ForeignKey('artist.id')),
	Column('annotation', Integer, ForeignKey('annotation.id')),
)

artist_ipi = Table('artist_ipi', metadata,
	Column('artist', Integer, ForeignKey('artist.id')),
	Column('ipi', String(11), nullable=False),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('created', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

artist_credit = Table('artist_credit', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', Integer, ForeignKey('artist_name.id')),
	Column('artist_count', Integer),
	Column('refcount', Integer),
	Column('created', DateTime),
)

artist_credit_name = Table('artist_credit_name', metadata,
	Column('artist_credit', Integer, ForeignKey('artist_credit.id', ondelete='CASCADE'),
	    primary_key=True),
	Column('position', Integer, primary_key=True),
	Column('artist', Integer),
	Column('artist', Integer, ForeignKey('artist.id', ondelete='CASCADE')),
	Column('artist_name', Integer, ForeignKey('artist_name.id')),
	Column('join_phrase', String),
)

artist_meta = Table('artist_meta', metadata,
	Column('id', Integer, ForeignKey('artist.id', ondelete='CASCADE')),
	Column('rating', SmallInteger),
	Column('rating_count', Integer),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

artist_name = Table('artist_name', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', UnicodeText),
)
 
artist_rating_raw = Table('artist_rating_raw', metadata,
	Column('artist', Integer, ForeignKey('artist.id')),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('rating', SmallInteger, nullable=False),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

artist_tag = Table('artist_tag', metadata,
	Column('artist', Integer, ForeignKey('artist.id')),
	Column('tag', Integer, ForeignKey('tag.id')),
	Column('count', Integer),
	Column('last_updated', DateTime, default=datetime.now),
)

artist_tag_raw = Table('artist_tag_raw', metadata,
	Column('artist', Integer, ForeignKey('artist.id')),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('tag', Integer, ForeignKey('tag.id')),
)

artist_type = Table('artist_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', UnicodeText),
)

cdtoc = Table('cdtoc', metadata,
	Column('id', Integer, primary_key=True),
	Column('disc_id', String(28)),
	Column('freedb_id', String(8)),
	Column('track_count', Integer),
	Column('leadout_offset', Integer),
	Column('track_offset', Integer),
	Column('degraded', Boolean),
	Column('created', DateTime),
)

cdtoc_raw = Table('cdtoc_raw', metadata,
	Column('id', Integer, primary_key=True),
	Column('release', Integer, ForeignKey('release_raw.id')),
	Column('disc_id', String(11), nullable=False),
	Column('track_count', Integer, nullable=False),
	Column('leadout_offset', Integer, nullable=False),
	Column('track_offset', Integer, nullable=False),
)

client_version = Table('client_version', metadata,
	Column('id', Integer, primary_key=True),
	Column('version', String(64), nullable=False),
	Column('created', DateTime, default=datetime.now),
)

country = Table('country', metadata,
	Column('id', Integer, primary_key=True),
	Column('iso_code', String(2)),
	Column('name', String(255)),
)

edit = Table('edit', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('type', SmallInteger, nullable=False),
	Column('status', SmallInteger, nullable=False),
	Column('data', Text, nullable=False),
	Column('yes_votes', Integer, nullable=False, default=0),
	Column('no_votes', Integer, nullable=False, default=0),
	Column('autoedit', SmallInteger, nullable=False, default=0),
	Column('open_time', DateTime, default=datetime.now),
	Column('close_time', DateTime),
	Column('expire_time', DateTime, nullable=False),
	Column('language', Integer, ForeignKey('language.id')),
	Column('quality', SmallInteger, nullable=False, default=1),
)

edit_note = Table('edit_note', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('edit', Integer, ForeignKey('edit.id')),
	Column('text', Text, nullable=False),
	Column('post_time', DateTime, default=datetime.now),
)

edit_artist = Table('edit_artist', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('artist', Integer, ForeignKey('artist.id', ondelete='CASCADE'), primary_key=True),
	Column('status', SmallInteger, nullable=False),
)

edit_label = Table('edit_label', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('label', Integer, ForeignKey('label.id', ondelete='CASCADE'), primary_key=True),
	Column('status', SmallInteger, nullable=False),
)

edit_release = Table('edit_release', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('release', Integer, ForeignKey('release.id', ondelete='CASCADE'), primary_key=True),
)

edit_release_group = Table('edit_release_group', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('release_group', Integer, ForeignKey('release_group.id', ondelete='CASCADE'), primary_key=True),
)

edit_recording = Table('edit_recording', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('recording', Integer, ForeignKey('recording.id', ondelete='CASCADE'), primary_key=True),
)

edit_work = Table('edit_work', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('work', Integer, ForeignKey('work.id', ondelete='CASCADE'), primary_key=True),
)

edit_url = Table('edit_url', metadata,
	Column('edit', Integer, ForeignKey('edit.id'), primary_key=True),
	Column('url', Integer, ForeignKey('url.id', ondelete='CASCADE'), primary_key=True),
)

editor = Table('editor', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(64), nullable=False),
	Column('password', String(64), nullable=False),
	Column('privs', Integer, default=0),
	Column('email', String(64), nullable=False),
	Column('website', String(255), nullable=False),
	Column('bio', Text, default=None),
	Column('member_since', DateTime, default=datetime.now),
	Column('email_confirm_date', DateTime),
	Column('last_login_date', DateTime),
	Column('edits_accepted', Integer, default=0),
	Column('edits_rejected', Integer, default=0),
	Column('auto_edits_accepted', Integer, default=0),
	Column('edits_failed', Integer, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	Column('birth_date', DateTime),
	Column('gender', Integer, ForeignKey('gender.id')),
	Column('country', Integer, ForeignKey('country.id')),
)

editor_collection = Table('editor_collection', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID, nullable=False),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('name', String, nullable=False),
	Column('public', Boolean, nullable=False, default=False),
)

editor_collection_release = Table('editor_collection_release', metadata,
	Column('collection', Integer, ForeignKey('editor_collection.id'),
	    primary_key=True),
	Column('release', Integer, ForeignKey('release.id'),
	    primary_key=True),
)

fluency = Enum('basic', 'intermediate', 'advanced', 'native', name='FLUENCY')

editor_language = Table('editor_language', metadata,
	Column('editor', Integer, ForeignKey('editor.id'), primary_key=True),
	Column('language', Integer, ForeignKey('language.id'), primary_key=True),
	Column('fluency', fluency, nullable=False),
)

editor_preference = Table('editor_preference', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('name', String(50), nullable=False),
	Column('value', String(100), nullable=False),
)

editor_subscribe_artist = Table('editor_subscribe_artist', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('artist', Integer, nullable=False),
	Column('last_edit_sent', Integer, nullable=False),
	Column('deleted_by_edit', Integer, nullable=False, default=0),
	Column('merged_by_edit', Integer, nullable=False, default=0),
)

editor_subscribe_label = Table('editor_subscribe_label', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('label', Integer, nullable=False),
	Column('last_edit_sent', Integer, nullable=False),
	Column('deleted_by_edit', Integer, nullable=False, default=0),
	Column('merged_by_edit', Integer, nullable=False, default=0),
)

editor_subscribe_editor = Table('editor_subscribe_editor', metadata,
	Column('id', Integer, primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('subscribed_editor', Integer, ForeignKey('editor.id')),
	Column('last_edit_sent', Integer, nullable=False),
)

editor_watch_preferences = Table('editor_watch_preferences', metadata,
	Column('editor', Integer, ForeignKey('editor.id', ondelete='CASCADE')),
	Column('notify_via_email', Boolean, nullable=False, default=True),
	Column('notification_timeframe', Interval, nullable=False, default='1 week'),
	Column('last_checked', DateTime, nullable=False, default=datetime.now),
)

editor_watch_artist = Table('editor_watch_artist', metadata,
	Column('artist', Integer, ForeignKey('artist.id', ondelete='CASCADE')),
	Column('editor', Integer, ForeignKey('editor.id', ondelete='CASCADE')),
)

editor_watch_release_group_type = Table('editor_watch_release_group_type',
    metadata,
	Column('editor', Integer, ForeignKey('editor.id', ondelete='CASCADE'), primary_key=True),
	Column('release_group_type', Integer,
	    ForeignKey('release_group_primary_type.id'), primary_key=True),
)

editor_watch_release_status = Table('editor_watch_release_status',
    metadata,
	Column('editor', Integer, ForeignKey('editor.id', ondelete='CASCADE'), primary_key=True),
	Column('release_status', Integer, ForeignKey('release_status.id'),
	    primary_key=True),
)

gender = Table('gender', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(255), nullable=False),
)

isrc = Table('isrc', metadata,
	Column('id', Integer, primary_key=True),
	Column('recording', Integer, ForeignKey('recording.id')),
	Column('isrc', CHAR(12), nullable=False),
	Column('source', SmallInteger),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('created', DateTime, default=datetime.now),
	CheckConstraint("isrc ~ E'^[A-Z]{2}[A-Z0-9]{3}[0-9]{7}$'"),
	CheckConstraint('edits_pending >= 0'),
)

iswc = Table('iswc', metadata,
	Column('id', Integer, primary_key=True),
	Column('work', Integer, ForeignKey('work.id')),
	Column('iswc', CHAR(15), nullable=False),
	Column('source', SmallInteger),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('created', DateTime, default=datetime.now),
	CheckConstraint("iswc ~ E'^T-?\\\\d{3}.?\\\\d{3}.?\\\\d{3}[-.]?\\\\d$'"),
	CheckConstraint('edits_pending >= 0'),
)

# Generate all the link tables
link_tables = ['artist', 'label', 'recording', 'release', 'release_group',
'url', 'work']
from itertools import combinations_with_replacement
for combination in combinations_with_replacement(link_tables, 2):
    table_name = 'l_%s_%s' % combination
    
    table = Table(table_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('link', Integer, ForeignKey('link.id')),
        Column('entity0', Integer),
        Column('entity1', Integer),
        Column('edits_pending', Integer, nullable=False, default=0),
        Column('last_updated', DateTime, default=datetime.now),
        CheckConstraint('edits_pending >= 0'),
    )
    
    globals()[table_name] = table

label = Table('label', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID),
	Column('name', Integer, ForeignKey('label_name.id')),
	Column('sort_name', Integer, ForeignKey('label_name.id')),
	Column('begin_date_year', SmallInteger),
	Column('begin_date_month', SmallInteger),
	Column('begin_date_day', SmallInteger),
	Column('end_date_year', SmallInteger),
	Column('end_date_month', SmallInteger),
	Column('end_date_day', SmallInteger),
	Column('label_code', String),
	Column('type', Integer, ForeignKey('label_type.id')),
	Column('country', Integer, ForeignKey('country.id')),
	Column('comment', String(255), default=''),
	Column('ipi_code', String),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	Column('ended', Boolean, default=False),
	CheckConstraint("""(end_date_year IS NOT NULL OR
	    end_date_month IS NOT NULL OR
        end_date_day IS NOT NULL) AND
        ended = TRUE"""),
	CheckConstraint("""(end_date_year IS NULL AND
           end_date_month IS NULL AND
           end_date_day IS NULL)"""),
)
 
label_rating_raw = Table('label_rating_raw', metadata,
	Column('label', Integer, ForeignKey('label.id')),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('rating', SmallInteger, nullable=False),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

label_tag_raw = Table('label_tag_raw', metadata,
	Column('label', Integer, ForeignKey('label.id')),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('tag', Integer, ForeignKey('tag.id')),
)

label_alias_type = Table('label_alias_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String, nullable=False),
)

label_alias = Table('label_alias', metadata,
	Column('id', Integer, primary_key=True),
	Column('label', Integer, ForeignKey('label.id')),
	Column('locale', Integer),
	Column('name', Integer, ForeignKey('label_name.id')),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
)

label_annotation = Table('label_annotation', metadata,
	Column('label', Integer, ForeignKey('label.id')),
	Column('annotation', Integer, ForeignKey('annotation.id')),
)

label_ipi = Table('label_ipi', metadata,
	Column('label', Integer, ForeignKey('label.id')),
	Column('ipi', String(11), nullable=False),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('created', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

label_meta = Table('label_meta', metadata,
	Column('id', Integer, ForeignKey('label.id', ondelete='CASCADE')),
	Column('rating', SmallInteger),
	Column('rating_count', Integer),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

label_gid_redirect = Table('label_gid_redirect', metadata,
	Column('gid', GUID, primary_key=True),
	Column('new_id', Integer, ForeignKey('label.id')),
	Column('created', DateTime, default=datetime.now),
)

label_name = Table('label_name', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String),
)

label_tag = Table('label_tag', metadata,
	Column('label', Integer, ForeignKey('label.id')),
	Column('tag', Integer, ForeignKey('tag.id')),
	Column('count', Integer, nullable=False),
)

label_type = Table('label_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(255)),
)

language = Table('language', metadata,
	Column('editor', Integer, primary_key=True),
	Column('iso_code_3t', CHAR(3)),
	Column('iso_code_3b', CHAR(3)),
	Column('iso_code_2', CHAR(2)),
	Column('name', String(100)),
	Column('frequency', Integer, nullable=False, default=0),
	Column('iso_code_3', CHAR(3)),
	CheckConstraint('iso_code_2t IS NOT NULL OR iso_code_3  IS NOT NULL',
	    'iso_code_check'),
)

link = Table('link', metadata,
	Column('id', Integer, primary_key=True),
	Column('link_type', Integer, ForeignKey('link_type.id')),
	Column('begin_date_year', SmallInteger),
	Column('begin_date_month', SmallInteger),
	Column('begin_date_day', SmallInteger),
	Column('end_date_year', SmallInteger),
	Column('end_date_month', SmallInteger),
	Column('end_date_day', SmallInteger),
	Column('attribute_count', Integer, nullable=False, default=0),
	Column('created', DateTime, default=datetime.now),
	Column('ended', Boolean, nullable=False, default=False),
	CheckConstraint("""(end_date_year IS NOT NULL OR
	    end_date_month IS NOT NULL OR
        end_date_day IS NOT NULL) AND
        ended = TRUE"""),
	CheckConstraint("""(end_date_year IS NULL AND
           end_date_month IS NULL AND
           end_date_day IS NULL)"""),
)

link_attribute = Table('link_attribute', metadata,
	Column('link', Integer, ForeignKey('link.id'), primary_key=True),
	Column('attribute_type', Integer, ForeignKey('link_attribute_type.id'),
	    primary_key=True),
	Column('created', DateTime, default=datetime.now),
)

link_attribute_type = Table('link_attribute_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('parent', Integer, ForeignKey('link_attribute_type.id')),
	Column('root', Integer, ForeignKey('link_attribute_type.id')),
	Column('child_order', Integer, nullable=False, default=0),
	Column('gid', GUID, nullable=False),
	Column('name', String(255), nullable=False),
	Column('description', Text),
	Column('last_updated', DateTime, default=datetime.now),
)

link_type = Table('link_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('parent', Integer, ForeignKey('link_type.id')),
	Column('child_order', Integer, nullable=False, default=0),
	Column('gid', GUID, nullable=False),
	Column('entity_type0', String(50), nullable=False),
	Column('entity_type1', String(50), nullable=False),
	Column('name', String(255), nullable=False),
	Column('description', Text),
	Column('link_phrase', String(255), nullable=False),
	Column('reverse_link_phrase', String(255), nullable=False),
	Column('short_link_phrase', String(255), nullable=False),
	Column('priority', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
)

link_type_attribute_type = Table('link_type_attribute_type', metadata,
	Column('link_type', Integer, ForeignKey('link_type.id'), primary_key=True),
	Column('attribute_type', Integer, ForeignKey('link_attribute_type.id'),
	    primary_key=True),
	Column('min', SmallInteger),
	Column('max', SmallInteger),
	Column('last_updated', DateTime, default=datetime.now),
)

medium = Table('medium', metadata,
	Column('id', Integer, primary_key=True),
	Column('tracklist', Integer, ForeignKey('tracklist.id')),
	Column('release', Integer, ForeignKey('release.id')),
	Column('position', Integer),
	Column('format', Integer, ForeignKey('medium_format.id')),
	Column('name', UnicodeText),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

medium_cdtoc = Table('medium_cdtoc', metadata,
	Column('id', Integer, primary_key=True),
	Column('medium', Integer, ForeignKey('medium.id')),
	Column('cdtoc', Integer, ForeignKey('cdtoc.id')),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

medium_format = Table('medium_format', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', UnicodeText),
	Column('year', Integer),
)

puid = Table('puid', metadata,
	Column('id', Integer, primary_key=True),
	Column('puid', CHAR(36), nullable=False),
	Column('version', Integer, ForeignKey('clientversion.id')),
)

replication_control = Table('replication_control', metadata,
	Column('id', Integer, primary_key=True),
	Column('current_schema_sequence', Integer, nullable=False),
	Column('current_replication_sequence', Integer),
	Column('last_replication_date', DateTime),
)

recording = Table('recording', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID),
	Column('artist_credit', Integer, ForeignKey('artist_credit.id')),
	Column('name', Integer, ForeignKey('track_name.id')),
	Column('length', Integer),
	Column('comment', UnicodeText),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
)
 
recording_rating_raw = Table('recording_rating_raw', metadata,
	Column('recording', Integer, ForeignKey('recording.id'), primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id'), primary_key=True),
	Column('rating', SmallInteger, nullable=False),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

recording_tag_raw = Table('recording_tag_raw', metadata,
	Column('recording', Integer, ForeignKey('recording.id'), primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id'), primary_key=True),
	Column('tag', Integer, ForeignKey('tag.id'), primary_key=True),
)

recording_annotation = Table('recording_annotation', metadata,
	Column('recording', Integer, ForeignKey('recording.id'), primary_key=True),
	Column('annotation', Integer, ForeignKey('annotation.id'), primary_key=True),
)

recording_meta = Table('recording_meta', metadata,
	Column('id', Integer, ForeignKey('recording.id', ondelete='CASCADE'), primary_key=True),
	Column('rating', SmallInteger),
	Column('rating_count', Integer),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

recording_gid_redirect = Table('recording_gid_redirect', metadata,
	Column('gid', GUID, primary_key=True),
	Column('new_id', Integer, ForeignKey('recording.id')),
	Column('created', DateTime, default=datetime.now),
)

recording_puid = Table('recording_puid', metadata,
	Column('id', Integer, primary_key=True),
	Column('puid', Integer, ForeignKey('puid.id')),
	Column('recording', Integer, ForeignKey('recording.id')),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('created', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

recording_tag = Table('recording_tag', metadata,
	Column('recording', Integer, ForeignKey('recording.id'), primary_key=True),
	Column('tag', Integer, ForeignKey('tag.id'), primary_key=True),
	Column('count', Integer),
	Column('last_updated', DateTime, default=datetime.now),
)

release = Table('release', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID),
	Column('name', Integer, ForeignKey('release_name.id')),
	Column('artist_credit', Integer, ForeignKey('artist_credit.id')),
	Column('release_group', Integer, ForeignKey('release_group.id')),
	Column('status', Integer, ForeignKey('release_status.id')),
	Column('packaging', Integer, ForeignKey('release_packaging.id')),
	Column('country', Integer, ForeignKey('country.id')),
	Column('language', Integer, ForeignKey('language.id')),
	Column('script', Integer,  ForeignKey('script.id')),
	Column('date_year', SmallInteger),
	Column('date_month', SmallInteger),
	Column('date_day', SmallInteger),
	Column('barcode', String(255)),
	Column('comment', String(255), nullable=False, default=''),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('quality', SmallInteger, nullable=False, default=-1),
	Column('last_updated', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

release_raw = Table('release_raw', metadata,
	Column('id', Integer, primary_key=True),
	Column('title', String(255), nullable=False),
	Column('artist', String(255)),
	Column('added', DateTime, default=datetime.now),
	Column('last_modified', DateTime, default=datetime.now),
	Column('lookup_count', Integer, default=0),
	Column('modify_count', Integer, default=0),
	Column('source', Integer, default=0),
	Column('barcode', String(255)),
	Column('comment', String(255), nullable=False, default=''),
)

release_tag_raw = Table('release_tag_raw', metadata,
	Column('release', Integer, ForeignKey('release.id')),
	Column('editor', Integer, ForeignKey('editor.id')),
	Column('tag', Integer, ForeignKey('tag.id')),
)

release_annotation = Table('release_annotation', metadata,
	Column('release', Integer, ForeignKey('release.id')),
	Column('annotation', Integer, ForeignKey('annotation.id')),
)

release_gid_redirect = Table('release_gid_redirect', metadata,
	Column('gid', GUID, primary_key=True),
	Column('new_id', Integer, ForeignKey('release.id')),
	Column('created', DateTime, default=datetime.now),
)

cover_art_presence = Enum('absent', 'present', 'darkened', name='cover_art_presence')

release_meta = Table('release_meta', metadata,
	Column('id', Integer, ForeignKey('release.id', ondelete='CASCADE'), primary_key=True),
	Column('date_added', DateTime, default=datetime.now),
	Column('info_url', String(255)),
	Column('amazon_asin', String(10)),
	Column('amazon_store', String(20)),
	Column('cover_art_presence', cover_art_presence, nullable=False, default='absent'),
)

release_coverart = Table('release_coverart', metadata,
	Column('id', Integer, ForeignKey('release.id', ondelete='CASCADE'), primary_key=True),
	Column('last_updated', DateTime, default=datetime.now),
	Column('cover_art_url', String(255)),
)

release_label = Table('release_label', metadata,
	Column('id', Integer, primary_key=True),
	Column('release', Integer,  ForeignKey('release.id')),
	Column('label', Integer,  ForeignKey('label.id')),
	Column('catalog_number', String(255)),
	Column('last_updated', DateTime, default=datetime.now),
)

release_packaging = Table('release_packaging', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(255), nullable=False),
)

release_status = Table('release_status', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(255), nullable=False),
)

release_tag = Table('release_tag', metadata,
	Column('release', Integer, ForeignKey('release.id')),
	Column('tag', Integer, ForeignKey('tag.id')),
	Column('count', Integer, nullable=False),
	Column('last_updated', DateTime, default=datetime.now),
)

release_group = Table('release_group', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID),
	Column('name', Integer, ForeignKey('release_name.id')),
	Column('artist_credit', Integer, ForeignKey('artist_credit.id')),
	Column('type', Integer, ForeignKey('release_group_type.id')),
	Column('comment', UnicodeText),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
)

release_group_rating_raw = Table('release_group_rating_raw', metadata,
	Column('release_group', Integer, ForeignKey('release_group.id'), primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id'), primary_key=True),
	Column('rating', SmallInteger, nullable=False),
	CheckConstraint('rating >= 0 AND rating <= 100'),
)

release_group_tag_raw = Table('release_group_tag_raw', metadata,
	Column('release_group', Integer, ForeignKey('release_group.id'), primary_key=True),
	Column('editor', Integer, ForeignKey('editor.id'), primary_key=True),
	Column('tag', Integer, ForeignKey('tag.id'), primary_key=True),
)

release_group_annotation = Table('release_group_annotation', metadata,
	Column('release_group', Integer, ForeignKey('release_group.id'), primary_key=True),
	Column('annotation', Integer, ForeignKey('annotation.id'), primary_key=True),
)

release_group_gid_redirect = Table('release_group_gid_redirect', metadata,
	Column('gid', GUID, primary_key=True),
	Column('new_id', Integer, ForeignKey('release_group.id')),
	Column('created', DateTime, default=datetime.now),
)

release_group_meta = Table('release_group_meta', metadata,
	Column('id', Integer, ForeignKey('release_group.id', ondelete='CASCADE'), primary_key=True),
	Column('release_count', Integer, nullable=False, default=0),
	Column('first_release_date_year', SmallInteger),
	Column('first_release_date_month', SmallInteger),
	Column('first_release_date_day', SmallInteger),
	Column('rating', SmallInteger),
	Column('rating_count', Integer),
	CheckConstraint('rating >= 0 AND rating <= 100'), 
)

release_group_tag = Table('release_group_tag', metadata,
	Column('release_group', Integer, ForeignKey('release_group.id'), primary_key=True),
	Column('tag', Integer, ForeignKey('tag.id'), primary_key=True),
	Column('count', Integer, nullable=False),
	Column('last_updated', DateTime, default=datetime.now),
)

release_group_primary_type = Table('release_group_primary_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(255), nullable=False),
)

release_group_secondary_type = Table('release_group_secondary_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', Text, nullable=False),
)

release_group_secondary_type_join = Table('release_group_secondary_type_join', metadata,
	Column('release_group', Integer, ForeignKey('release_group.id'), primary_key=True),
	Column('secondary_type', Integer, ForeignKey('release_group_secondary_type.id'), primary_key=True),
	Column('created', DateTime, default=datetime.now),
)

release_name = Table('release_name', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String),
)

script = Table('script', metadata,
	Column('id', Integer, primary_key=True),
	Column('iso_code', Char(4), nullable=False),
	Column('iso_number', Char(3), nullable=False),
	Column('name', String(100), nullable=False),
	Column('frequency', Integer, nullable=False, default=0),
)

script_language = Table('script_language', metadata,
	Column('id', Integer, primary_key=True),
	Column('script', Integer, ForeignKey('script.id')),
	Column('language', Integer, ForeignKey('language.id')),
	Column('frequency', Integer, nullable=False, default=0),
)

tag = Table('tag', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(255), nullable=False),
	Column('ref_count', Integer, nullable=False, default=0),
)

tag_relation = Table('tag_relation', metadata,
	Column('tag1', Integer, ForeignKey('tag.id'), primary_key=True),
	Column('tag2', Integer, ForeignKey('tag.id'), primary_key=True),
	Column('weight', Integer, nullable=False),
	Column('last_updated', DateTime, default=datetime.now),
	CheckConstraint('tag1 < tag2'), 
)

track = Table('track', metadata,
	Column('id', Integer, primary_key=True),
	Column('recording', Integer, ForeignKey('recording.id')),
	Column('tracklist', Integer, ForeignKey('tracklist.id')),
	Column('position', Integer, nullable=False),
	Column('name', Integer, ForeignKey('track_name.id')),
	Column('artist_credit', Integer, ForeignKey('artist_credit.id')),
	Column('length', Integer, nullable=False),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	Column('number', String, nullable=False),
)

track_raw = Table('track_raw', metadata,
	Column('id', Integer),
	Column('release', Integer, ForeignKey('release_raw.id')),
	Column('title', String(255), nullable=False),
	Column('artist', String(255)),
	Column('sequence', Integer, nullable=False),
)

track_name = Table('track_name', metadata,
	Column('id', Integer, primary_key=True),
	Column('page', UnicodeText),
)

tracklist = Table('tracklist', metadata,
	Column('id', Integer, primary_key=True),
	Column('track_count', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now)
),

tracklist_index = Table('tracklist_index', metadata,
	Column('tracklist', Integer, ForeignKey('tracklist.id'), primary_key=True),
	# CUBE
	Column('toc', Integer),
)

url = Table('url', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID),
	Column('url', UnicodeText),
#	Column('description', UnicodeText),
#	Column('refcount', Integer),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
	CheckConstraint('edits_pending >= 0'), 
)

url_gid_redirect = Table('url_gid_redirect', metadata,
	Column('gid', GUID, primary_key=True),
	Column('new_id', Integer, ForeignKey('url.id')),
	Column('created', DateTime, default=datetime.now),
)

work_name = Table('work_name', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', UnicodeText),
)

work = Table('work', metadata,
	Column('id', Integer, primary_key=True),
	Column('gid', GUID),
	Column('type', Integer, ForeignKey('work_type.id')),
	Column('name', Integer, ForeignKey('work_name.id')),
	Column('iswc', String),
	Column('comment', UnicodeText),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
)

work_type = Table('work_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', UnicodeText),
)

work_alias = Table('work_alias', metadata,
	Column('id', Integer, primary_key=True),
	Column('work', Integer, ForeignKey('work.id')),
	Column('name', UnicodeText),
	Column('locale', Integer),
	Column('edits_pending', Integer, nullable=False, default=0),
	Column('last_updated', DateTime, default=datetime.now),
)

#--

release_group_type = Table('release_group_type', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', UnicodeText),
)

#--

#--

#--

#---


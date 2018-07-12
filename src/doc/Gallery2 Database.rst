Database Schema (G2)

This page details the purpose of each table created in a Gallery2 installation. A typical Gallery 2 installation will create over 50 tables in your database. The default installation will append g2_ in front of the table names.
Tables

    AccessMap
    AccessSubscriberMap
    AlbumItem - has three fields - sets up infromation for album items. Fields include an Item Id (refers to an Album), a theme , "order by" setting (Title, Name, last created, last modified, random etc), order direction (ascending or descending)
    AnimationItem
    CacheMap - Stores the cached HTML pages when caching is turned on in Site Maintenance (Under Performance tab). This table tends to be the largest in size depending on the length of acceleration enabled. It is safe to clear this table of all data before a database back up is taken
    ChildEntity - provides the linkage between a Album and a Sub Album, or an Album and its Sub items. Since all objects (albums, images, sub albums) are part of a single "Item" table, the ChildEntity table provides the hiearchy / parent-child linkage by providing a 'Parent Id' for every individual object
    DataItem - has three fields - each record is linked to an Item Id which is then described by type (PDF, Jpeg, Mpeg etc) and its file size.
    Derivative' - This table holds the information for Thumbnails for each of the main items (images or Albums). Each thumbnail is given an Item id, and the Main Image or Album is identified by the derivativeSourceId field. Other fields give infromation on file size, image type etc.
    DerivativeImage - Sets Thumbnail dimensions for Derivative Images (thumbnails). Fields are g_id (Item Id), g_width g_height
    DerivativePrefsMap
    DescendentCountsMap - Table stores 'Item counts' for each album. Every album has two records or more - one for showing number of items for Guests, others for users based on permissions. This is usually reflected in the "Number of Items" block in g-info on the album view.
    Entity - The Entity table is the master table that defines what type of an entity is represented by a unique gallery id. In G-2, all entitites (Users, Photos, Albums, Thumbnails, User Groups) have unique ids. Thus g_id 1 is always the "Gallery". 2, 3, 4 are always the User Groups (Registered Users, Site Administrators, Everyone). 5 and 6 are the default users created (guest and admin). 7 is always the root gallery. Subsequenly all galleries, photo albums, photos , users etc are generated a unique id and this table describes the type of entity each one is. The Item table gives the data for albums and photo images. Other tables like User, Group gives details for others.
    EventLogMap - table contains all error log messages - provides details of error message, link, referring IP, timestamp etc.
    ExifPropertiesMap
    ExternalIdMap
    FactoryMap
    FailedLoginsMap
    FileSystemEntity
    Group - Holds the various User group information as created by Site Admins. The default groups created at installation are with ids 2, 3 and 4. (Registered Users, Site Administrators, Everyone).
    ImageBlockCacheMap
    ImageBlockDisabledMap
    Item - This table is one of the main important data holders. The table stores information on each individual element - whether it is an album or an image. each record contains information on the item id, title, summary, description, owner, date of creation and whether it is an album (can contain children - value = 1) or not (value = 0). The item id is linked to the Item id in the FileSystemEntity table which stores the filename of the Image file.
    ItemAttributesMap
    ItemHiddenMap
    LinkItem - stores information on 'Links' created in Albums.
    Lock
    MaintenanceMap
    MimeTypeMap
    MovieItem
    PendingUser
    PermalinksMap
    PermissionSetMap
    PhotoItem
    PluginMap
    PluginPackageMap
    PluginParameterMap
    QuotasMap - If 'User Quota' plugin is enabled, G2 usses this table to store the disk quota for each individual user or user group.
    RatingCacheMap - Gallery uses this table to store the results from analyzing the raw ratings from the RatingMap table. Each item has a correpsonding record based on Item Id - and the total number of votes received and the average rating number is saved in this table
    RatingMap - Stores the Raw individual ratings if the Gallery allows User Ratings. This can become a very large table based on the number of ratings the installation attracts.
    RecoverPasswordMap - Used by gallery to store "Forgotten Password" Requests initiated by users.
    RssMap - G2 stores information on each individual RSS feed that has been created in this table.
    Schema - has records containing SQL statements to create each table in a Gallery Installation.
    SequenceEventLog
    SequenceId
    SequenceLock
    SessionMap - Current user sessions are stored in this table. Safe to clear before backup.
    ThumbnailImage
    TkOperatnMap
    TkOperatnMimeTypeMap
    TkOperatnParameterMap
    TkPropertyMap
    TkPropertyMimeTypeMap
    UnknownItem
    User - Stores User information - like Username, email, encrypted password etc. Installation creates Users with ids 5 (Guests) and 6 (admin). Subsequent users created get ids based on the unique gallery id available at that point of time.
    UserGroupMap - Links Users with User groups - with User Ids and Group Id numbers
    WatermarkImage - Stores information on various Watermarks and attributes. table gives information on watermark id, owner, and whether it is applied on Thumbnails, resizes, originals and approximate coordinates where the watermark is applied 

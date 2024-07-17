#mongoDB

-no sql query language
-nosql dbs include a lack of db schema, data clustering, replication support, eventual consistency, easily scalable
    RDBMS           MongoDB
    --------        --------
    database        Databse
    table           Collection
    row/record      Documents
    columns         Fields
    join            Embedded documents


-BASE
    -basically available
        -ensure availability of data by spreading and replicating data across nodes of the db cluster
    -soft state
        -Due to lack of immediate consitency, data values may change over time. Developers are more 
         responsible for enforcing consistency of data
    - Eventual consistency
        - Eventually, database will commit changes across the cluster to a consistent state

- In and RDBMS, we design our dbs using normalization
-In MongoDB, no rules for db design
    - ONly thing that matters is making something that works for our application
- sharding
    - utilizing multiple sysyems to increase the resources in a server/cluster
    - Example of "horizontal scaling"

-now mongo db sh commands
    -show dbs: shows databases
    -use databasename: uses the stated database, if none exists creates a new one
    -show collections: shows documents aka tables in the db
    -creating a new document, the insert part is in JSON!-> db.tablename.insert({"PersonID":1, "LastName":"Edwards","FirstName":"Anthony","City":"Minneapolis"})
    -see document(table) content: db.tablename.find()
    -finding fields(columns) in the documentL db.docname.find({Boats: {$exists:true}})
    -make format pretty: .pretty()
    -update, will update the first element found: db.docname.update({PersonID:3}, {$set: {City:"the update"}})
    -updateMany, will update all elements that match: db.docname.updateMany({City:"Mattawa"}, {$set: {City:"the update"}})
    -remove: db.persons.remove({MovieId:1})----db.persons.remove({Boats:{$exists:true}})
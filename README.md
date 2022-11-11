# MongoDB-University
MongoDB project for group University work

## Tests ran
### Identifying a unique ID
The following code snippet was ran to determine if the rs numbers for the variants were unique.
```
db.variants.aggregate([
    {"$group" : { "_id": "$name", "count": { "$sum": 1 } } },
    {"$match": {"_id" :{ "$ne" : null } , "count" : {"$gt": 1} } }, 
    {"$project": {"name" : "$_id", "_id" : 0} }
]);
[
  { name: 'rs758394755' }, { name: 'rs778712913' },
  { name: 'rs74378188' },  { name: 'rs184544118' },
  { name: 'rs142812704' }, { name: 'rs730881706' },
  { name: 'rs761381277' }, { name: 'rs751226166' },
  { name: 'rs750248363' }, { name: 'rs587781373' },
  { name: 'rs121908698' }, { name: 'rs17886319' },
  { name: 'rs398122652' }, { name: 'rs141070855' },
  { name: 'rs3092831' },   { name: 'rs758772714' },
  { name: 'rs536169158' }, { name: 'rs11212585' },
  { name: 'rs767820592' }, { name: 'rs63750903' }
]
```
As they were not all unique, variant urls were generated using the ObjectID which is a unique value for each variant
### Adding X or Y chromosomes
All the variants already in the database have numerical chromosomes. The chromosome field was edited to take both integers and strings, and list both alphanumerically. A check was added to ensure that the chromosome had a valid value (1-22, X and Y) before allowing the user to submit it.

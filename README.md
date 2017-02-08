# Database

## Opcodes for interfacing with database
Note - [0] is a null byte


0 - Request FoodItem : Request a returned foodItem from the database
#####Format
	0[0][hashcode - n bytes - TBD][padding to 100 bytes]

1 - FoodItem Returned : This packet contains the requested FoodItem
#####Format
	1[0][String FoodItem name][0][String lifetimeInDays]

2 - FoodItem not in Database : Sent when the database does not contain the requested hashcode
#####Format
	2[0][padding to 100 bytes]

3 - Update Database : Sent to the database to add this entry
#####Format
	3[0][String FoodItem name][0][String lifetimeInDays][0][Hashcode][padding to 100 bytes]

4 - ping : Pingee will respond to pinger with another '4' packet
#####Format
	4[0][padding to 100 bytes]
	
## Database name

BLABdb

## BLABdb Tables
####food_item_lookup:

	tag_hashcode varchar(64) primary_key
	item_name varchar(40)
	expiry int

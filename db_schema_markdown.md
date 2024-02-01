Table Profile {
  id integer [pk]
  user_id integer [unique]
  image varchar
  first_name varchar(100)
  last_name varchar(100)
  mobile_number varchar(100)
  token varchar(150)
  is_active boolean
  email varchar(100) [unique]
  date timestamp
  date_update timestamp
  type varchar(7) [note: 'Choices are USER, TECNICI, STAFF']
}

Table WorksitesProfile{
    id integer [pk]
    profile_id integer [ref: > Profile.id]
    worksite_id integer [ref: > Worksites.id]
}

Table Worksites {
  id integer [pk]
  image varchar
  name varchar(100)
  address varchar(100)
  lat decimal(10,6)
  lon decimal(10,6)
  is_open boolean
  net_worth float
  financier int [ref: > Financier.id]
  contractor_id int [ref: > Contractor.id]
  link varchar(100)
  date timestamp
  date_update timestamp
}

table CheckList{
  id integer [pk]
  name varchar(100)
}

table CheckListWorksites{
  id integer [pk]
  worksites_id int [ref: > Worksites.id]
  checklist_id int [ref: > CheckList.id]
  date timestamp
  order int
  is_done boolean
}


Table Apartments {
  id integer [pk]
  worksite_id integer [ref: > Worksites.id]
  foglio int
  particella int
  sub int
  surface varchar(100)
  note varchar(100)
  owner varchar(100)
  owner_phone varchar(100)
  owner_email varchar(100)
  owner_cf varchar(100)
  link varchar(100)
  date timestamp
  date_update timestamp
}

Table ClientApartments {
  id integer [pk]
  profile_id integer [ref: > Profile.id]
  apartment_id integer [ref: > Apartments.id]
  is_active boolean
}

Table BoardRead {
  id integer [pk]
  profile_id integer [ref: > Profile.id]
  board_id integer [ref: > Boards.id]
  date timestamp
}


Table BoardAttachments {
  id integer [pk]
  board_id integer [ref: > Boards.id]
  attachment_link varchar
  type varchar(7) [note: 'Choices are DOCUMENT, IMAGE']
  date timestamp
}

Table Boards {
  id integer [pk]
  worksite_id integer [ref: > Worksites.id]
  apartment_id integer [ref: > Apartments.id]
  image varchar
  title varchar(250)
  body text
  author varchar(150)
  date timestamp
  date_update timestamp
  recipients int
  type varchar(7) [note: 'Choices are MESSAGE, UPDATE']
}

Table CollabWorksites {
  id integer [pk]
  profile_id integer [ref: > Profile.id]
  worksite_id integer [ref: > Worksites.id]
  role varchar(150) 
  order integer
}

table Categories {
  id integer [pk]
  name varchar(150)
}

Table WorksitesCategories{
    id integer [pk]
    category_id integer [ref: > Categories.id]
    worksite_id integer [ref: > Worksites.id]
}

Table Financier {
  id integer [pk]
  name varchar(150)
}

Table Contractor {
  id integer [pk]
  name varchar(150)
}

This is a simple app that implements both authentication and authorization by allowing a user to login, register, create 'feedback', edit 'feedback', delete 'feedback', view 'feedback', and delete their own account. 

A user must be logged in, in order to view, create, edit, or delete their own feedback. They also must be authenticated in order to delete their own account. 

They can view the 'feedback' and information of other users but they will not be authorized to create, edit, or delete other user's feedback. They will also be unable to delete another user's account.

- Tools used:
  - Python
  - Flask
  - Flask-SQLAlchemy
  - Flask-WTForms
  - Flask-Bcrypt
  - PostgreSQL
  - Bootstrap 5
  - HTML
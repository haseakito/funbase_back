from prisma.models import User

# user response schema
User.create_partial('UserOut', exclude_relational_fields=True, exclude={'password', 'emailVerified'})

# get a user response schema
User.create_partial('UserGet', exclude={'password'})

# user login schema
User.create_partial('UserLogin', include={'email', 'password'})

# user create schema
User.create_partial('UserCreate', include={'username', 'email', 'password'})

# reset password schema
User.create_partial('ResetPassword', include={'email', 'password'})
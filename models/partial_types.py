from prisma.models import User, Profile

"""
User schema
"""
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

"""
Profile schema
"""
# update profile bio schema
Profile.create_partial('UpdateBio', include={'bio'})

# update profile profileImage schema
Profile.create_partial('UpdateProfile', include={'profileImage'})

# update profile coverImage schema
Profile.create_partial('UpdateCover', include={'coverImage'})
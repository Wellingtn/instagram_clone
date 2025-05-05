import os

# Create directories for templates
directories = [
    'templates/social_app/auth',
    'templates/social_app/post',
    'templates/social_app/reel',
    'templates/social_app/profile',
    'templates/social_app/search',
    'media/post_images',
    'media/reel_videos',
    'media/profile_pics',
    'static/css',
    'static/js',
    'static/img',
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

print("All directories created successfully!")

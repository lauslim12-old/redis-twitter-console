# Redis Twitter Console

Sample application to demonstrate the usage of Redis and Python Console to make a simple Twitter clone.

## Introduction

This application is a port from [Redis's official guidelines](https://redis.io/topics/twitter-clone). It was written in PHP and it used Redis on Linux. My version uses [Redis Labs](https://redislabs.com/), which is Redis database on cloud, similar to MongoDB Atlas. This application also supports Redis on Linux too, so you have no need to worry.

## Database Schema

Redis is not your usual database. It is a data-structure database used for caching, but with the right design, it could also be used as a conventional database (with the additional feature of being extremely fast). We use hashes to store data, and hashes/lists/sorted sets to store identifiers, according to Redis's guide. In this application, the notation `uid` means user-id and `tid` means the tweet-id.

Keys used here are as follows:

- `next_user_id`, a sequence used to auto-increment `user_id`, used in `user`, `users`, and `tweet_user`.
- `next_tweet_id`, a sequence used to auto-increment `tweet_id`, used in `tweets` and `tweet_user`.
- `users`, a hash to store all references of primary keys used to identify users (`uid`).
- `user:{uid}`, a hash used to store the user's data. Referenced by the `users` hash.
- `followers:{uid}`, a sorted set with the aim to store the latest followers of a user (`uid`).
- `following:{uid}`, a sorted set with the aim to store the latest followings of a user (`uid`).
- `tweets:{tid}`, a hash used to store all of the tweets.
- `tweet_user:{uid}`, a list to store all references to a user's tweet (`tid`).
- `timeline`, a list to store all references to the latest 1000 tweets (`tid`).

For further information, try all of the features, then check the condition of the database by using the 'Get All Data (Debug)' functionality in the application.

## Features

- User can sign up and login. **For the sake of simplicity, passwords are stored in plaintext.**
- User can get their own profile. They can see their personal data, their tweets, their followers, and their followings.
- User can post their own tweet.
- User can follow someone.
- User can see other users profile.
- User can unfollow someone.
- User can see the global timeline of the latest 1000 posts.
- User can update their own username.
- User can log out.
- User can exit the application.
- User can get all data available in the Redis database.
- User can flush the Redis database.
- Error handling exists in every module. Some edge test-cases are also covered in this application.
- Every function is documented properly.

## Requirements

- Python 3.5 and up
- Pipenv version 2020 and up
- Redis version 4.0 and up

## Installation

- Clone the repository.

```bash
git clone
```

- Switch to the repository.

```bash
cd redis-twitter-console
```

- Activate `pipenv` shell.

```bash
pipenv shell
```

- Install all dependencies.

```bash
pipenv install
```

- Setup environment variables in an `.env` file.

```bash
touch .env
nano .env

# fill the environment variables here
REDIS_HOST=YOUR_REDIS_HOST
REDIS_PORT=YOUR_REDIS_PORT
REDIS_PASSWORD=YOUR_REDIS_PASSWORD
```

- Run the application.

```bash
pipenv run start
```

## Development

After coding, do not forget to run the formatter, linter, and type-checker.

```bash
pipenv shell
pipenv run format
pipenv run lint
```

## Notes

Will be moved to [@lauslim12-old](https://github.com/lauslim12-old/) soon as this is only a temporary repository that I use to familiarize myself with Redis environment.

## License

MIT License. Feel free to use this as you see fit.

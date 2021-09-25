//docker run -d --name redis-test -p 6379:6379 redis

const redis = require('redis');
const client = redis.createClient();

client.on('connect', function() {
  console.log('Connected!');
});

const setData = (key, value) => {
  return new Promise((resolve, reject) => {
    client.set(key, JSON.stringify(value), function(err, reply) {
      if (err) return reject('Not Set')
      return resolve(reply)
    });
  })
}

const getData = (key) => {
  return new Promise((resolve, reject) => {
    client.get(key, function(err, reply) {
      if (err) return reject('Not Exist')
      return resolve(JSON.parse(reply))
    });
  })
}

module.exports = {
  client,
  setData,
  getData
}

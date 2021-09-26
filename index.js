const express = require('express')
const cors = require('cors')
const { getData } = require('./caching/redis_client')

const app = express()

app.get('/ping', (req, res) => {
  res.json({ status: 'working' })
})

app.get('/products', async (req, res) => {
  const data = await getData('products')
    .catch(err => { return err })
  res.json(data)
})

app.get('/categories', async (req, res) => {
  const data = await getData('categories')
    .catch(err => { return err })
  res.json(data)
})

app.get('/users', async (req, res) => {
  const data = await getData('users')
    .catch(err => { return err })
  res.json(data)
})

app.use(cors())

app.listen(3000, () => {
  console.log('running');
})

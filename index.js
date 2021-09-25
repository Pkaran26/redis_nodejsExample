const express = require('express')
const cors = require('cors')

const app = express()

app.get('/ping', (req, res) => {
  res.json({ status: 'working' })
})

app.use(cors())

app.listen(3000, () => {
  console.log('running');
})

const { setData, getData } = require('./redis_client')
const axios = require('axios')

const BASE_URL = 'https://fakestoreapi.com'

const getServerData = async (key) => {
  const result = await axios.get(`${BASE_URL}/${key}`)
    .catch(err => { return err.response })

  if (result) {
    if (result.data && result.data.length > 0) {
      console.log(key, ': ', result.data.length);
      const res = await setData(key, JSON.stringify(result.data))
        .catch(err => { return err })
      console.log(key, ' caching: ', res);
    }
  }
}

getServerData('products')
getServerData('categories')
getServerData('users')

setTimeout(async () => {
  // console.log(await getData('products'));
  process.exit()
}, 4000)

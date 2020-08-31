/* Dependencias */
const express = require('express')
/* Configuracion */
const app = express()

/* Endpoint */
app.get('/', (request, response) => {
  response.send('Hola Mundo!')
})

app.get('/posts', (request, response) => {
  const posts = [
    {
      caption: "Av San Martín",
      location: "Colonia Caroya, Argentina"
    },
    {
      caption: "Festival de Doma y Folclore",
      location: "Jesus Maria, Argentina"
    }
  ]
  response.send(posts)
})

/* Listen */
app.listen(3000)

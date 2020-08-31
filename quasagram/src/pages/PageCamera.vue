<template>
  <q-page class="constrain-more q-pa-md">
    <div class="camera-frame q-pa-md">
      <video
        v-show="!imageCaptured"
        ref="video"
        class="full-width"
        autoplay
      />
      <canvas
        v-show="imageCaptured"
        ref="canvas"
        class="full-width"
        height="240"
      />
    </div>
    <div class="text-center q-pa-md">
      <q-btn
        v-if="hasCameraSupport"
        round
        color="grey-10"
        icon="eva-camera"
        size="lg"
        :disable="imageCaptured"
        @click="captureImage"
      />
      <q-file
        v-else
        outlined
        label="Choose an image"
        accept="image/*"
        v-model="imageUpload"
        @input="captureImageFallback"
      >
        <template v-slot:prepend>
          <q-icon name="eva-attach-outline" />
        </template>
      </q-file>
      <div class="row justify-center q-ma-md">
        <q-input
          v-model="post.caption"
          class="col col-sm-6"
          label="Caption"
          dense
        />
      </div>
      <div class="row justify-center q-ma-md">
        <q-input
          v-model="post.location"
          :loading="locationLoading"
          class="col col-sm-6"
          label="Location"
          dense
        >
          <template v-slot:append>
            <q-btn
              v-if="!locationLoading && locationSupported"
              round
              dense
              flat
              icon="eva-navigation-2-outline"
              @click="getLocation"
            />
          </template>
        </q-input>
      </div>
      <div class="row justify-center q-mt-lg">
        <q-btn
          unelevated
          rounded
          color="primary"
          label="Post Image"
          :disabled="!post.caption || !post.photo"
          @click="addPost"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { uid } from 'quasar'

export default {
  name: 'PageCamera',
  data () {
    return {
      post: {
        id: uid(),
        caption: '',
        location: '',
        photo: null,
        date: Date.now()
      },
      imageCaptured: false,
      imageUpload: [],
      hasCameraSupport: true,
      locationLoading: false
    }
  },
  computed: {
    locationSupported () {
      // return 'geolocation' in navigator
      if ('geolocation' in navigator) {
        return true
      }
      return false
    },
    backgroundSyncSupported () {
      if ('serviceWorker' in navigator && 'SyncManager' in window) {
        return true
      }
      return false
    }
  },
  methods: {
    initCamera () {
      navigator.mediaDevices.getUserMedia({
        video: true
      }).then(stream => {
        this.$refs.video.srcObject = stream
      }).catch(err => {
        console.log(err)
        this.hasCameraSupport = false
      })
    },

    captureImage () {
      const video = this.$refs.video
      const canvas = this.$refs.canvas
      canvas.width = video.getBoundingClientRect().width
      canvas.height = video.getBoundingClientRect().height
      const context = canvas.getContext('2d')
      context.drawImage(video, 0, 0, canvas.width, canvas.height)
      this.imageCaptured = true
      this.post.photo = this.dataURItoBlob(canvas.toDataURL())
      this.disbleCamera()
    },

    captureImageFallback (file) {
      this.post.photo = file
      const canvas = this.$refs.canvas
      const context = canvas.getContext('2d')
      const render = new FileReader()

      render.onload = event => {
        var img = new Image()
        img.onload = () => {
          canvas.width = img.width
          canvas.height = img.height
          context.drawImage(img, 0, 0)
          this.imageCaptured = true
        }
        img.src = event.target.result
      }
      render.readAsDataURL(file)
    },

    disbleCamera () {
      this.$refs.video.srcObject.getVideoTracks().forEach(track => {
        track.stop()
      })
    },

    dataURItoBlob (dataURI) {
      // convert base64 to raw binary data held in a string
      // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
      var byteString = atob(dataURI.split(',')[1])

      // separate out the mime component
      var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

      // write the bytes of the string to an ArrayBuffer
      var ab = new ArrayBuffer(byteString.length)

      // create a view into the buffer
      var ia = new Uint8Array(ab)

      // set the bytes of the buffer to the correct values
      for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
      }

      // write the ArrayBuffer to a blob, and you're done
      var blob = new Blob([ab], { type: mimeString })
      return blob
    },
    getLocation () {
      this.locationLoading = true
      navigator.geolocation.getCurrentPosition(position => {
        this.getCityAndCountry(position)
      }, err => {
        this.locationError(err)
      }, { timeout: 7000 })
    },
    getCityAndCountry (position) {
      const apiUrl = `https://geocode.xyz/${position.coords.latitude},${position.coords.longitude}?json=1`
      this.$axios.get(apiUrl).then(result => {
        this.locationSuccess(result)
      }).catch(err => {
        this.locationError(err)
      })
    },
    locationSuccess (result) {
      this.post.location = result.data.city
      if (result.data.country) {
        this.post.location += `, ${result.data.country}`
      }
      // console.log(result.data.city)
      this.locationLoading = false
    },
    locationError (err) {
      // console.log(err.message)
      this.$q.dialog({
        title: 'Error',
        message: `No se pudo encontrar su localización (${err.message})`
      })
      this.locationLoading = false
    },
    addPost () {
      const formData = new FormData()
      this.$q.loading.show()
      formData.append('id', this.post.id)
      formData.append('caption', this.post.caption)
      formData.append('location', this.post.location)
      formData.append('date', this.post.date)
      formData.append('photo', this.post.photo, this.post.id + '.png')

      // this.$axios.post(`${process.env.API}/posts`, formData).then(response => {
      this.$axios.post('/api/v1/posts', formData).then(response => {
        console.log(response)
        this.$router.push('/')
        this.$q.notify({
          message: 'Post created!',
          actions: [
            { label: 'Dismiss', color: 'white' }
          ]
        })
        this.$q.loading.hide()
      }).catch(error => {
        if (!navigator.onLine && this.backgroundSyncSupported) {
          this.$q.notify('Post created offline')
          this.$q.loading.hide()
          this.$router.push('/')
        } else {
          this.$q.dialog({
            title: 'Error',
            message: `Sorry, could not create post. (${error.message})`
          })
        }
        this.$q.loading.hide()
        // this.loadingPosts = false
      })
    }
  },
  mounted () {
    this.initCamera()
  },
  beforeDestroy () {
    if (this.hasCameraSupport) {
      this.disbleCamera()
    }
  }
}
</script>
<style lang="sass">
  .camera-frame
    border: 2px solid $grey-10
    border-radius: 10px
</style>

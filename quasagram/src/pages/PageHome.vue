<template>
  <q-page class="constrain q-pa-md">
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <div
        v-if="showNotificationsBanner && pushNotificationsSupported"
        class="banner-container bg-primary"
      >
        <div class="constrain">
          <q-banner
            class="bg-grey-3 q-mb-md"
          >
            <template v-slot:avatar>
              <q-icon
                color="primary"
                name="eva-bell-outline"
              />
            </template>
            Would you like to enable notificatios?

            <template v-slot:action>
              <q-btn
                flat
                label="Yes"
                color="primary"
                class="q-px-sm"
                @click="enableNotifications"
              />
              <q-btn
                flat
                label="Later"
                color="primary"
                class="q-px-sm"
                @click="showNotificationsBanner = false"
              />
              <q-btn
                flat
                label="Never"
                color="primary"
                class="q-px-sm"
                @click="neverShowNotificationsBanner"
              />
            </template>
          </q-banner>
        </div>
      </div>
    </transition>
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-sm-8">
        <template v-if="!loadingPosts && posts.length">
          <q-card
            v-for="post in posts"
            :key="post.id"
            class="card-post q-mb-md"
            :class="{ 'bg-red-1' : post.offline }"
            flat
            bordered
          >
            <q-badge
              v-if="post.offline"
              color="red"
              class="badge-offline absolute-top-right"
            >
              Stored offline
            </q-badge>
            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label class="text-bold">
                  jose__jachuf
                </q-item-label>
                <q-item-label caption>
                  {{ post.location }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />
            <q-img
              :src="post.imageUrl"
            />
            <q-card-section>
              <div>{{ post.caption }}</div>
              <div class="text-caption text-grey">{{ post.date | niceDate }}</div>
            </q-card-section>

          </q-card>
        </template>
        <template v-else-if="!loadingPosts && !posts.length">
          <h5 class="text-center text-grey">
            No posts yet.
          </h5>
        </template>
        <template v-else>
          <q-card flat bordered>
            <q-item>
              <q-item-section avatar>
                <q-skeleton type="QAvatar" animation="fade" size="40px"/>
              </q-item-section>

              <q-item-section>
                <q-item-label>
                  <q-skeleton type="text" animation="fade" />
                </q-item-label>
                <q-item-label caption>
                  <q-skeleton type="text" animation="fade" />
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-skeleton height="200px" square animation="fade" />

            <q-card-section>
              <q-skeleton type="text" class="text-subtitle2" animation="fade" />
              <q-skeleton type="text" width="50%" class="text-subtitle2" animation="fade" />
            </q-card-section>
          </q-card>
        </template>
      </div>

      <div class="col-4 large-screen-only">
        <q-item class="fixed">
          <q-item-section avatar>
            <q-avatar size="48px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-bold">
              jose__jachuf
            </q-item-label>
            <q-item-label caption>
              Jose Jachuf
            </q-item-label>
          </q-item-section>
        </q-item>
      </div>
    </div>

  </q-page>
</template>

<script>
import { date } from 'quasar'
import { openDB } from 'idb'
const qs = require('qs')

export default {
  name: 'PageHome',
  data () {
    return {
      posts: [],
      loadingPosts: false,
      showNotificationsBanner: false
    }
  },
  filters: {
    niceDate (value) {
      return date.formatDate(value, 'MMM D h:mmA')
    }
  },
  computed: {
    serviceWorkerSupported () {
      return 'serviceWorker' in navigator
    },
    pushNotificationsSupported () {
      return 'PushManager' in window
    }
  },
  methods: {
    getPosts () {
      this.loadingPosts = true
      // this.$axios.get(`${process.env.API}/posts/?sort_by=-date`).then(response => {
      this.$axios.get('/api/v1/posts/?sort_by=-date').then(response => {
        this.posts = response.data.data
        this.loadingPosts = false
        if (!navigator.onLine) {
          this.getOfflinePosts()
        }
      }).catch(error => {
        this.$q.dialog({
          title: 'Error',
          message: `No se pudieron descargar los posts (${error.message})`
        })
        this.loadingPosts = false
      })
    },
    getOfflinePosts () {
      console.log('get Offline Posts')
      // const db = openDB('workbox-background-sync').then(db => {
      openDB('workbox-background-sync').then(db => {
        db.getAll('requests').then(failedRequests => {
          failedRequests.forEach(failedRequest => {
            if (failedRequest.queueName === 'createPostQueue') {
              const request = new Request(failedRequest.requestData.url, failedRequest.requestData)
              request.formData().then(formData => {
                const offLinePosts = {}
                offLinePosts.id = formData.get('id')
                offLinePosts.caption = formData.get('caption')
                offLinePosts.location = formData.get('location')
                offLinePosts.date = parseInt(formData.get('date'))
                offLinePosts.offline = true

                const reader = new FileReader()
                reader.readAsDataURL(formData.get('photo'))
                reader.onloadend = () => {
                  offLinePosts.imageUrl = reader.result
                  this.posts.unshift(offLinePosts)
                }
              })
            }
          })
        }).catch(err => {
          console.log('err', err)
        })
      })
      // console.log(db)
    },
    listenForOfflinePostUploaded () {
      console.log('listenForOfflinePostUploaded')
      if (this.serviceWorkerSupported) {
        const channel = new BroadcastChannel('sw-messages')
        channel.addEventListener('message', event => {
          const offlinePostCount = this.posts.filter(post => post.offline === true).length
          this.posts[offlinePostCount - 1].offline = false
        })
      }
    },
    initNotificationsBanner () {
      console.log('initNotificationsBanner')
      const neverShowNotificationsBanner = this.$q.localStorage.getItem('neverShowNotificationsBanner')
      if (!neverShowNotificationsBanner) {
        this.showNotificationsBanner = true
        // window.addEventListener('beforeinstallprompt', (e) => {
        //   // Prevent the mini-infobar from appearing on mobile
        //   e.preventDefault()
        //   // Stash the event so it can be triggered later.
        //   deferredPrompt = e
        //   // Update UI notify the user they can install the PWA
        //   this.showAppInstallBanner = true
        // })
      }
    },
    enableNotifications () {
      if (this.pushNotificationsSupported) {
        Notification.requestPermission(result => {
          console.log('result', result)
          this.neverShowNotificationsBanner()
          if (result === 'granted') {
            // this.displayGrantedNotification()
            this.checkForExistingPushSubscription()
          }
        })
      }
      // this.$q.localStorage.set('neverShowNotificationsBanner', true)
      // this.showNotificationsBanner = false
      // Hide the app provided install promotion
      // this.showAppInstallBanner = false
      // // Show the install prompt
      // deferredPrompt.prompt()
      // // Wait for the user to respond to the prompt
      // deferredPrompt.userChoice.then((choiceResult) => {
      //   if (choiceResult.outcome === 'accepted') {
      //     this.neverShowAppInstallBanner()
      //     console.log('User accepted the install prompt')
      //   } else {
      //     console.log('User dismissed the install prompt')
      //   }
      // })
    },
    checkForExistingPushSubscription () {
      if (this.serviceWorkerSupported && this.pushNotificationsSupported) {
        let reg
        navigator.serviceWorker.ready.then(swreg => {
          reg = swreg
          return swreg.pushManager.getSubscription()
        }).then(sub => {
          if (!sub) {
            console.log('create a new push subscription')
            this.createPushSubscription(reg)
          }
        })
      }
    },
    urlBase64ToUint8Array (base64String) {
      const padding = '='.repeat((4 - base64String.length % 4) % 4)
      const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/')

      const rawData = window.atob(base64)
      const outputArray = new Uint8Array(rawData.length)

      for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i)
      }
      return outputArray
    },
    createPushSubscription (reg) {
      const vapidPublicKey = 'BJF-lmpC9xBkSiKW3dHM8IZsnURMxbORkTbkceQfab_H7eIzOlotDA-T-sHshFfD-3QPhR0xiTFM9oCkScS0vAU'
      const convertedVapidKey = this.urlBase64ToUint8Array(vapidPublicKey)
      reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedVapidKey
      }).then(newSub => {
        const newSubData = newSub.toJSON()
        const newSubDataQS = qs.stringify(newSubData)
        console.log('newSubData', newSubData)
        console.log('newSubDataQS', newSubDataQS)
        const postSubscription = {
          subscription: newSubData,
          user_id: 5
        }
        // this.$axios.post(`${process.env.API}/subscriptions`, postSubscription).then(response => {
        this.$axios.post('/api/v1/subscriptions', postSubscription).then(response => {
          console.log(response)
        }).catch(error => {
          console.log(error)
        })
      }).then(response => {
        console.log('response', response)
      }).catch(err => {
        console.log('err', err)
      })
    },
    displayGrantedNotification () {
      // const notification = new Notification('You are subcribed to notifications!', {
      //   body: 'Thanks for subscribing',
      //   icon: 'icons/icon-128x128.png',
      //   image: 'icons/icon-128x128.png',
      //   badge: 'icons/icon-128x128.png',
      //   dir: 'ltr',
      //   lang: 'es',
      //   vibrate: [100, 50, 200],
      //   tag: 'confirm-notification',
      //   renotify: true
      // })
      if (this.serviceWorkerSupported && this.pushNotificationsSupported) {
        navigator.serviceWorker.ready.then(swreg => {
          swreg.showNotification('You are subcribed to notifications!', {
            body: 'Thanks for subscribing',
            icon: 'icons/icon-128x128.png',
            image: 'icons/icon-128x128.png',
            badge: 'icons/icon-128x128.png',
            dir: 'ltr',
            lang: 'es',
            vibrate: [100, 50, 200],
            tag: 'confirm-notification',
            renotify: true,
            actions: [
              {
                action: 'hello',
                title: 'Hello',
                icon: 'icons/icon-128x128.png'
              },
              {
                action: 'goodbye',
                title: 'Goodbye',
                icon: 'icons/icon-128x128.png'
              }
            ]
          })
        })
      }
      // console.log(notification)
    },
    neverShowNotificationsBanner () {
      this.showNotificationsBanner = false
      this.$q.localStorage.set('neverShowNotificationsBanner', true)
    }

  },
  activated () {
    this.getPosts()
  },
  created () {
    this.listenForOfflinePostUploaded()
    this.initNotificationsBanner()
  }
}
</script>

<style lang="sass">
  .card-post
    .badge-offline
      border-top-left-radius: 0 !important
    .q-img
      min-height: 200px
</style>

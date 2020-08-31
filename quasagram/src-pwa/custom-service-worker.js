/*
 * This file (which will be your service worker)
 * is picked up by the build system ONLY if
 * quasar.conf > pwa > workboxPluginMode is set to "InjectManifest"
 */

import { precacheAndRoute } from 'workbox-precaching'
import { registerRoute } from 'workbox-routing'
import { StaleWhileRevalidate, CacheFirst, NetworkFirst } from 'workbox-strategies'
import { ExpirationPlugin } from 'workbox-expiration'
import { CacheableResponsePlugin } from 'workbox-cacheable-response'
import { Queue } from 'workbox-background-sync'

// Config
precacheAndRoute(self.__WB_MANIFEST)

let createPostQueue = null
const backgroundSyncSupported = 'sync' in self.registration
if (backgroundSyncSupported) {
  createPostQueue = new Queue('createPostQueue', {
    onSync: async ({ queue }) => {
      let entry = true
      entry = await queue.shiftRequest()
      while (entry) {
        console.log('entry', entry)
        try {
          await fetch(entry.request)
          console.log('Replay successful for request', entry.request)
          const channel = new BroadcastChannel('sw-messages')
          channel.postMessage({ msg: 'offline-post-uploaded' })
        } catch (error) {
          console.log('Replay failed for request', entry.request, error)

          // Put the entry back in the queue and re-throw the error:
          await queue.unshiftRequest(entry)
          throw error
        }
        entry = await queue.shiftRequest()
      }
      console.log('Replay complete!')
    }
  })
}

// Cache strategies
registerRoute(
  ({ url }) => url.host.startsWith('fonts.g'),
  new CacheFirst({
    cacheName: 'google-fonts',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 30
      }),
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
)

registerRoute(
  ({ url }) => url.pathname.startsWith('/api/v1/'),
  new NetworkFirst()
)

registerRoute(
  ({ url }) => url.href.startsWith('http'),
  new StaleWhileRevalidate()
)

// Event fetch
if (backgroundSyncSupported) {
  console.log('backgroundSyncSupported', backgroundSyncSupported)
  self.addEventListener('fetch', event => {
    console.log('event.request.method', event.request.method)
    if (event.request.url.endsWith('/posts') && event.request.method === 'POST') {
      // Clone the request to ensure it's safe to read when
      // adding to the Queue.
      if (!self.navigator.onLine) {
        const promiseChain = fetch(event.request.clone()).catch((err) => {
          console.log(err)
          return createPostQueue.pushRequest({ request: event.request })
        })
        event.waitUntil(promiseChain)
      }
    }
  })
}

// Events push

self.addEventListener('push', event => {
  console.log('Push message recive', event)
  if (event.data) {
    const data = JSON.parse(event.data.text())
    event.waitUntil(
      self.registration.showNotification(
        data.title,
        {
          body: data.body,
          icon: 'icons/icon-128x128.png',
          badge: 'icons/icon-128x128.png',
          data: {
            openUrl: data.openUrl
          }
        }
      )
    )
  }
})

self.addEventListener('notificationclose', event => {
})

// Events notifications

self.addEventListener('notificationclick', event => {
  const notification = event.notification
  const action = event.action
  console.log('event', event)
  console.log('action', action)
  if (action === 'hello') {
    console.log('Hello button was clicked')
  } else if (action === 'goodbye') {
    console.log('Goodbye button was clicked')
  } else {
    event.waitUntil(
      self.clients.matchAll().then(clis => {
        const clientUsingApp = clis.find(cli => {
          return cli.visibilityState === 'visible'
        })
        if (clientUsingApp) {
          clientUsingApp.navigate(notification.data.openUrl)
          clientUsingApp.focus()
        } else {
          self.clients.openWindow(notification.data.openUrl)
        }
      })
    )
  }
  notification.close()
})

self.addEventListener('notificationclose', event => {
})

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header
      class="bg-white text-grey-10"
      bordered
    >
      <q-toolbar class="constrain">
        <q-btn
          to="/camera"
          class="large-screen-only q-mr-sm"
          flat
          round
          dense
          size="18px"
          icon="eva-camera-outline"
        />
        <q-separator
          class="large-screen-only q-mr-sm"
          vertical
          spaced
        />
        <q-toolbar-title class="text-grand-hotel text-bold">
          Quasagram
        </q-toolbar-title>
        <q-btn
          to="/"
          class="large-screen-only"
          flat
          round
          dense
          size="18px"
          icon="eva-home-outline"
        />
      </q-toolbar>
    </q-header>
    <q-footer
      class="bg-white"
      bordered
    >
      <transition
        appear
        enter-active-class="animated fadeIn"
        leave-active-class="animated fadeOut"
      >
        <div
          v-if="showAppInstallBanner"
          class="banner-container bg-primary"
        >
          <div class="constrain">
            <q-banner
              inline-actions
              dense
              class="bg-primary text-white"
            >
              <template v-slot:avatar>
                <q-avatar
                  color="white"
                  text-color="grey-10"
                  icon="eva-camera-outline"
                  font-size="22px"
                />
              </template>
              Install Quasagram?

              <template v-slot:action>
                <q-btn
                  flat
                  dense
                  label="Yes"
                  class="q-px-sm"
                  @click="installApp"
                />
                <q-btn
                  flat
                  dense
                  label="Later"
                  class="q-px-sm"
                  @click="showAppInstallBanner = false"
                />
                <q-btn
                  flat
                  dense
                  label="Never"
                  class="q-px-sm"
                  @click="neverShowAppInstallBanner"
                />
              </template>
            </q-banner>
          </div>
        </div>
      </transition>

      <q-tabs
        class="text-grey-10 small-screen-only"
        active-color="primary"
        indicator-color="transparent"
      >
        <q-route-tab
          to="/"
          exact
          icon="eva-home-outline"
        />
        <q-route-tab
          to="/camera"
          exact
          icon="eva-camera-outline"
        />
      </q-tabs>
    </q-footer>

    <q-page-container class="bg-grey-1">
      <keep-alive :include = "['PageHome']">
        <router-view />
      </keep-alive>
    </q-page-container>
  </q-layout>
</template>

<script>
let deferredPrompt

export default {
  name: 'MainLayout',
  data () {
    return {
      showAppInstallBanner: false
    }
  },
  methods: {
    installApp () {
      // Hide the app provided install promotion
      this.showAppInstallBanner = false
      // Show the install prompt
      deferredPrompt.prompt()
      // Wait for the user to respond to the prompt
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          this.neverShowAppInstallBanner()
          console.log('User accepted the install prompt')
        } else {
          console.log('User dismissed the install prompt')
        }
      })
    },
    neverShowAppInstallBanner () {
      this.showAppInstallBanner = false
      this.$q.localStorage.set('neverShowAppInstallBanner', true)
    }
  },
  mounted () {
    const neverShowAppInstallBanner = this.$q.localStorage.getItem('neverShowAppInstallBanner')
    if (!neverShowAppInstallBanner) {
      window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent the mini-infobar from appearing on mobile
        e.preventDefault()
        // Stash the event so it can be triggered later.
        deferredPrompt = e
        // Update UI notify the user they can install the PWA
        this.showAppInstallBanner = true
      })
    }
  }
}
</script>

<style lang="sass">
  .q-toolbar
    @media (min-width: $breakpoint-sm-min)
      height: 77px
  .q-toolbar__title
    font-size: 30px
    @media (max-width: $breakpoint-xs-max)
      text-align: center
  .q-footer
    .q-tab__icon
      font-size: 30px
</style>
